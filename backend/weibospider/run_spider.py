#!/usr/bin/env python
# encoding: utf-8
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from weibospider.spiders import CommentSpider, FanSpider, FollowerSpider, TweetSpider, UserSpider, RepostSpider, \
    SearchSpider

import os

if __name__ == '__main__':
    mode = 'tweet'
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'comment': CommentSpider,
        'fan': FanSpider,
        'follow': FollowerSpider,
        'tweet': TweetSpider,
        'user': UserSpider,
        'repost': RepostSpider,
        'search': SearchSpider
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()
