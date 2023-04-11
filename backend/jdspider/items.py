# -*- coding: utf-8 -*-
import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class JdcommentItem(scrapy.Item):
    content = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
