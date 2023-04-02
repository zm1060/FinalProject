import json
from scrapy import Spider
from scrapy.http import Request
from spiders.weibospider.spiders.common import parse_user_info


class FanSpider(Spider):
    """
    微博粉丝数据采集
    """
    name = "fan"
    base_url = 'https://weibo.com/ajax/friendships/friends'

    def __init__(self, user_ids=None, *args, **kwargs):
        super(FanSpider, self).__init__(*args, **kwargs)
        self.user_ids = user_ids

    def start_requests(self):
        """
        爬虫入口
        """
        if self.user_ids is not None:
            self.user_ids = self.user_ids
        else:
            self.user_ids = ['1749127163']
        for user_id in self.user_ids:
            url = self.base_url + f"?relate=fans&page=1&uid={user_id}&type=fans"
            yield Request(url, callback=self.parse, meta={'user': user_id, 'page_num': 1})


    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     """
    #     工厂方法，用于创建爬虫实例
    #     """
    #     user_ids = crawler.settings.get('USER_IDS', [])
    #     spider = cls(user_ids=user_ids, *args, **kwargs)
    #     spider._set_crawler(crawler)
    #     return spider

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        for user in data['users']:
            item = dict()
            item['follower_id'] = response.meta['user']
            item['fan_info'] = parse_user_info(user)
            item['_id'] = response.meta['user'] + '_' + item['fan_info']['_id']
            yield item
        if data['users']:
            response.meta['page_num'] += 1
            url = self.base_url + f"?relate=fans&page={response.meta['page_num']}&uid={response.meta['user']}&type=fans"
            yield Request(url, callback=self.parse, meta=response.meta)
