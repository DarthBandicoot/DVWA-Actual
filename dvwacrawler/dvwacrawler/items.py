# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class DvwacrawlerItem(Item):
    first_name = Field()
    surname = Field()
    database_name = Field()
    database_version = Field()
