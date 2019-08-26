# -*- coding: utf-8 -*-

# Scrapy settings for dvwacrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'dvwacrawler'

SPIDER_MODULES = ['dvwacrawler.spiders']
NEWSPIDER_MODULE = 'dvwacrawler.spiders'

DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

ITEM_PIPELINES = {'dvwacrawler.pipelines.MongoDBPipeline': 300}

# MONGODB_SERVER = "mongodb://Lewis:********@192.168.0.119/dvwa"
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017

MONGODB_DB = "dvwa"

MONGODB_COLLECTION = "users"


ROBOTSTXT_OBEY = False
