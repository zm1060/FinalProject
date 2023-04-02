import json
from scrapy import Spider
from scrapy.http import Request

from spiders.weibospider.settings import DEFAULT_REQUEST_HEADERS
from spiders.weibospider.spiders.common import parse_user_info


class UserSpider(Spider):
    """
    微博用户信息爬虫
    """
    name = "user_spider"
    base_url = "https://weibo.cn"

    user_ids = []

    def __init__(self, user_ids=None, cookie=None, *args, **kwargs):
        super(UserSpider, self).__init__(*args, **kwargs)
        self.user_ids = user_ids
        self.cookie = cookie

        # Set cookie in default headers
        if self.cookie is not None:
            headers = DEFAULT_REQUEST_HEADERS
            headers['Cookie'] = self.cookie
            self.headers = headers

    def start_requests(self):
        """
        爬虫入口
        """
        user_ids = ['1749127163']
        if self.user_ids is not None:
           user_ids = self.user_ids
        else:
            user_ids = ['1749127163']
        urls = [f'https://weibo.com/ajax/profile/info?uid={user_id}' for user_id in user_ids]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        item = parse_user_info(data['data']['user'])
        url = f"https://weibo.com/ajax/profile/detail?uid={item['_id']}"
        yield Request(url, callback=self.parse_detail, meta={'item': item})

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
        yield item
