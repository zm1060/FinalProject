#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Spider
from scrapy.http import Request

from weibospider.settings import DEFAULT_REQUEST_HEADERS
from weibospider.spiders.common import parse_user_info, parse_time, url_to_mid


class CommentSpider(Spider):
    """
    微博评论数据采集
    """
    name = "comment_spider"
    tweet_ids = []
    cookie = []
    headers = []
    task_id = ''
    stats_info = {}

    def __init__(self, tweet_ids=None, cookie=None, task_id=None, *args, **kwargs):
        super(CommentSpider, self).__init__(*args, **kwargs)
        self.tweet_ids = tweet_ids
        self.cookie = cookie
        self.task_id = task_id
        # Set cookie in default headers
        if self.cookie is not None:
            self.headers = DEFAULT_REQUEST_HEADERS.copy()
            self.headers['Cookie'] = self.cookie

    def start_requests(self):
        """
        爬虫入口
        """
        for tweet_id in self.tweet_ids:
            mid = url_to_mid(tweet_id)
            url = f"https://weibo.com/ajax/statuses/buildComments?" \
                  f"is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=20"
            # https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=N0o83vU51&is_show_bulletin=2&is_mix=0&count=20
            yield Request(url, callback=self.parse, meta={'source_url': url}, headers=self.headers, cookies=self.cookie)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        for comment_info in data['data']:
            item = self.parse_comment(comment_info)
            yield item
        if data.get('max_id', 0) != 0:
            url = response.meta['source_url'] + '&max_id=' + str(data['max_id'])
            yield Request(url, callback=self.parse, meta=response.meta, headers=self.headers, cookies=self.cookie)

    @staticmethod
    def parse_comment(data):
        """
        解析comment
        """
        item = dict()
        item['created_at'] = parse_time(data['created_at'])
        item['_id'] = data['id']
        item['like_counts'] = data['like_counts']
        item['ip_location'] = data['source']
        item['content'] = data['text_raw']
        item['comment_user'] = parse_user_info(data['user'])
        return item
