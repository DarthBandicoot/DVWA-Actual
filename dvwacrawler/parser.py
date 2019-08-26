from bs4 import BeautifulSoup


def html_parser(response):
    results = response.body
    soup = BeautifulSoup(results, features="lxml")
    for tag in soup.findAll('pre'):
        _, firstname_field, surname_field = tag.prettify().split('<br/>')
        firstname = firstname_field.replace('First name: ', '')
        surname = surname_field.replace('Surname: ', ''.replace('</pre>', '').strip())

        return firstname, surname

