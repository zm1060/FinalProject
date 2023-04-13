#!/usr/bin/env python
# encoding: utf-8
import json
import re
from scrapy import Spider, Request

from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_tweet_info, parse_long_tweet


class SearchSpider(Spider):
    """
    关键词搜索采集
    """
    name = "search_spider"
    base_url = "https://s.weibo.com/"
    keywords = []
    cookie = []
    headers = []
    start_time = "2023-04-04-0"
    end_time = "2023-04-05-23"
    is_sort_by_hot = True
    is_search_with_specific_time_scope = False
    task_id = ''
    stats_info = {}

    def __init__(self, keywords=None, start_time=None, end_time=None,
                 is_sort_by_hot=False, is_search_with_specific_time_scope=False,
                 cookie=None, task_id=None, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords
        self.start_time = start_time
        self.end_time = end_time
        if is_sort_by_hot is not None:
            self.is_sort_by_hot = is_sort_by_hot
        else:
            self.is_sort_by_hot = True
        if is_search_with_specific_time_scope is not None:
            self.is_search_with_specific_time_scope = is_search_with_specific_time_scope
        else:
            self.is_search_with_specific_time_scope = False
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

        for keyword in self.keywords:
            if self.is_search_with_specific_time_scope:
                url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{self.start_time}%3A{self.end_time}&page=1"
            else:
                url = f"https://s.weibo.com/weibo?q={keyword}&page=1"
            if self.is_sort_by_hot:
                url += "&xsort=hot"
            print(url)
            print(self.headers)
            print(self.cookie)
            yield Request(url, callback=self.parse, headers=self.headers, cookies=self.cookie,
                          meta={'keyword': keyword})

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        html = response.text
        tweet_ids = re.findall(r'\d+/(.*?)\?refer_flag=1001030103_" ', html)
        for tweet_id in tweet_ids:
            url = f"https://weibo.com/ajax/statuses/show?id={tweet_id}"
            yield Request(url, callback=self.parse_tweet, meta=response.meta, headers=self.headers, cookies=self.cookie)
        next_page = re.search('<a href="(.*?)" class="next">下一页</a>', html)
        if next_page:
            url = "https://s.weibo.com" + next_page.group(1)
            yield Request(url, callback=self.parse, meta=response.meta, headers=self.headers, cookies=self.cookie)

    @staticmethod
    def parse_tweet(response):
        """
        解析推文
        """
        data = json.loads(response.text)
        item = parse_tweet_info(data)
        item['keyword'] = response.meta['keyword']
        if item['isLongText']:
            url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
            yield Request(url, callback=parse_long_tweet, meta={'item': item})
        else:
            yield item
