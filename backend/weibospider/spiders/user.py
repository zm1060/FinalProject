#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Spider
from scrapy.http import Request

from app.db.task_db import tasks_collection
from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_user_info


class UserSpider(Spider):
    """
    微博用户信息爬虫
    """
    name = "user_spider"
    base_url = "https://weibo.cn"
    user_ids = []
    user_id = ''
    cookie = []
    headers = []
    task_id = ''
    stats_info = {}

    def __init__(self, user_ids=None, user_id=None, cookie=None, task_id=None, *args, **kwargs):
        super(UserSpider, self).__init__(*args, **kwargs)
        self.user_ids = user_ids
        self.user_id = user_id
        self.cookie = cookie
        self.task_id = task_id
        # Set cookie in default headers
        if self.cookie is not None:
            self.headers = DEFAULT_REQUEST_HEADERS.copy()
            self.headers['Cookie'] = self.cookie

    # def closed(self, reason):
    #     self.stats_info = self.crawler.stats.get_stats()
    #     self.stats_info['task_id'] = self.task_id
    #     self.stats_info['user_id'] = self.user_id
    #     print(f"Spider closed, reason: {reason}")
    #     print(f"Stats info: {self.stats_info}")
    #     # tasks_collection.update_one({'task_id': self.task_id}, {'$set': {'stats': self.stats_info}}, upsert=True)

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
        urls = [f'https://weibo.com/ajax/profile/info?uid={user_id}' for user_id in self.user_ids]
        for url in urls:
            print(url)
            print(self.headers)
            yield Request(url, callback=self.parse, headers=self.headers, cookies=self.cookie)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        print(response.text)
        data = json.loads(response.text)
        item = parse_user_info(data['data']['user'])
        url = f"https://weibo.com/ajax/profile/detail?uid={item['_id']}"

        yield Request(url, callback=self.parse_detail, headers=self.headers, cookies=self.cookie, meta={'item': item})

    @staticmethod
    def parse_detail(response):
        """
        解析详细数据
        """
        item = response.meta['item']
        data = json.loads(response.text)['data']
        item['birthday'] = data.get('birthday', '')
        if 'created_at' not in item:
            item['created_at'] = data.get('created_at', '')
        item['desc_text'] = data.get('desc_text', '')
        item['ip_location'] = data.get('ip_location', '')
        item['sunshine_credit'] = data.get('sunshine_credit', {}).get('level', '')
        item['label_desc'] = [label['name'] for label in data.get('label_desc', [])]
        if 'company' in data:
            item['company'] = data['company']
        if 'education' in data:
            item['education'] = data['education']
        print(item)
        yield item
