#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Spider
from scrapy.http import Request

from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_user_info


class FollowerSpider(Spider):
    """
    微博关注数据采集
    """
    name = "follower_spider"
    base_url = 'https://weibo.com/ajax/friendships/friends'
    user_ids = []
    cookie = []
    headers = []
    task_id = ''
    stats_info = {}

    def __init__(self, user_ids=None, cookie=None, task_id=None, *args, **kwargs):
        super(FollowerSpider, self).__init__(*args, **kwargs)
        self.user_ids = user_ids
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
            url = self.base_url + f"?page=1&uid={user_id}"
            yield Request(url, callback=self.parse, meta={'user': user_id, 'page_num': 1}, headers=self.headers,
                          cookies=self.cookie)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        for user in data['users']:
            item = dict()
            item['fan_id'] = response.meta['user']
            item['follower_info'] = parse_user_info(user)
            item['_id'] = response.meta['user'] + '_' + item['follower_info']['_id']
            yield item
        if data['users']:
            response.meta['page_num'] += 1
            url = self.base_url + f"?page={response.meta['page_num']}&uid={response.meta['user']}"
            yield Request(url, callback=self.parse, meta=response.meta, headers=self.headers, cookies=self.cookie)
