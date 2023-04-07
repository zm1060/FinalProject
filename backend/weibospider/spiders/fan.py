#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Spider
from scrapy.http import Request

from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_user_info


class FanSpider(Spider):
    """
    微博粉丝数据采集
    """
    name = "fan"
    base_url = 'https://weibo.com/ajax/friendships/friends'
    headers = []
    cookie = []
    user_ids = []
    task_id = ''

    def __init__(self, user_ids=None, cookie=None, task_id=None, *args, **kwargs):
        super(FanSpider, self).__init__(*args, **kwargs)
        self.user_ids = user_ids
        self.cookie = cookie
        self.task_id = task_id
        # Set cookie in default headers
        if self.cookie is not None:
            self.headers = DEFAULT_REQUEST_HEADERS
            self.headers['Cookie'] = self.cookie

    def _parse_cookie(self, cookie_str):
        # if cookie_str is None:
        #     return None
        # cookie_dict = {}
        # for cookie in cookie_str.split(';'):
        #     key, value = cookie.strip().split('=', 1)
        #     cookie_dict[key] = value
        # return cookie_dict
        if cookie_str is None:
            return None
        return {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_str.split('; ')}

    def start_requests(self):
        """
        爬虫入口
        """
        print(self.headers)
        for user_id in self.user_ids:
            url = self.base_url + f"?relate=fans&page=1&uid={user_id}&type=fans"
            print(url)
            yield Request(url, callback=self.parse, meta={'user': user_id, 'page_num': 1}, cookies=self.cookie,
                          headers=self.headers)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        print(response.body)
        data = json.loads(response.text)
        for user in data['users']:
            item = dict()
            item['follower_id'] = response.meta['user']
            item['fan_info'] = parse_user_info(user)
            item['_id'] = response.meta['user'] + '_' + item['fan_info']['_id']
            print(item)
            yield item
        if data['users']:
            response.meta['page_num'] += 1
            url = self.base_url + f"?relate=fans&page={response.meta['page_num']}&uid={response.meta['user']}&type=fans"
            yield Request(url, callback=self.parse, cookies=self.cookie, headers=self.headers, meta=response.meta)
