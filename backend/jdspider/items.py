# -*- coding: utf-8 -*-
import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class JdcommentItem(scrapy.Item):
    id = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    isDelete = scrapy.Field()
    isTop = scrapy.Field()
    topped = scrapy.Field()
    replyCount = scrapy.Field()
    score = scrapy.Field()
    usefulVoteCount = scrapy.Field()
    mobileVersion = scrapy.Field()
    productColor = scrapy.Field()
    productSize = scrapy.Field()
    location = scrapy.Field()
    referenceName = scrapy.Field()
    referenceTime = scrapy.Field()
    nickname = scrapy.Field()
    days = scrapy.Field()
    afterDays = scrapy.Field()