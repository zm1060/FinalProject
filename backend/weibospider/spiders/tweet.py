#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Spider
from scrapy.http import Request

from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_tweet_info, parse_long_tweet


class TweetSpider(Spider):
    """
    用户推文数据采集
    """
    name = "tweet_spider"
    base_url = "https://weibo.cn"
    user_ids = []
    cookie = []
    headers = []
    task_id = ''
    stats_info = {}

    def __init__(self, user_ids=None, cookie=None, task_id=None, *args, **kwargs):
        super(TweetSpider, self).__init__(*args, **kwargs)
        self.user_ids = user_ids
        # self.cookie = self._parse_cookie(cookie)
        self.cookie = cookie
        self.task_id = task_id
        # Set cookie in default headers
        if self.cookie is not None:
            self.headers = DEFAULT_REQUEST_HEADERS
            self.headers['Cookie'] = self.cookie

    def _parse_cookie(self, cookie_str):
        if cookie_str is None:
            return None
        return {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_str.split('; ')}

    def start_requests(self):
        """
        爬虫入口
        """
        for user_id in self.user_ids:
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page=1"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': 1}, headers=self.headers,
                          cookies=self.cookie)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        tweets = data['data']['list']
        for tweet in tweets:
            item = parse_tweet_info(tweet)
            del item['user']
            if item['isLongText']:
                url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
                yield Request(url, callback=parse_long_tweet, meta={'item': item}, headers=self.headers,
                              cookies=self.cookie)
            else:
                yield item
        if tweets:
            user_id, page_num = response.meta['user_id'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page={page_num}"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num},
                          headers=self.headers, cookies=self.cookie)
