#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Spider
from scrapy.http import Request

from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_tweet_info, url_to_mid


class RepostSpider(Spider):
    """
    微博转发数据采集
    """
    name = "repost_spider"
    tweet_ids = []
    cookie = []
    headers = []
    task_id = ''
    stats_info = {}

    def __init__(self, tweet_ids=None, cookie=None, task_id=None, *args, **kwargs):
        super(RepostSpider, self).__init__(*args, **kwargs)
        self.tweet_ids = tweet_ids
        self.cookie = cookie
        self.task_id = task_id
        # Set cookie in default headers
        if self.cookie is not None:
            self.headers = DEFAULT_REQUEST_HEADERS
            self.headers['Cookie'] = self.cookie

    def start_requests(self):
        """
        爬虫入口
        """
        # 这里tweet_ids可替换成实际待采集的数据
        for tweet_id in self.tweet_ids:
            mid = url_to_mid(tweet_id)
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page=1&moduleID=feed&count=10"
            yield Request(url, callback=self.parse, meta={'page_num': 1, 'mid': mid}, headers=self.headers,
                          cookies=self.cookie)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        for tweet in data['data']:
            item = parse_tweet_info(tweet)
            yield item
        if data['data']:
            mid, page_num = response.meta['mid'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page_num}&moduleID=feed&count=10"
            yield Request(url, callback=self.parse, meta={'page_num': page_num, 'mid': mid}, headers=self.headers,
                          cookies=self.cookie)
