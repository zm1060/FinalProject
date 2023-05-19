# -*- coding: utf-8 -*-
import json
import re

import requests
import scrapy
import time

from scrapy.loader import ItemLoader

from jdspider.items import JdcommentItem


# 评论抓取
class JDcommentspider(scrapy.Spider):
    name = 'JDcommentspider'
    allowed_domains = ['jd.com']
    start_urls = []
    task_id = ''
    pages = ''
    number = ''
    custom_settings = {
        'ITEM_PIPELINES': {
            'jdspider.pipelines.JDcommentPipeline': 300,
        }
    }

    def __init__(self, urls, pages, task_id):
        super(JDcommentspider, self).__init__()
        self.pages = int(pages)
        self.task_id = task_id
        if type(urls) == str:
            self.start_urls = [urls]
            print(self.start_urls)
        elif type(urls) == list:
            self.start_urls = urls
            print(self.start_urls)
        else:
            raise RuntimeError("参数必须为字符串或者列表")
        self.number = re.findall(r"com/(\d+)\.html", self.start_urls[0])[0]
        print(self.number)
        # 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=' + number +'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        self.comment_page_baseurl = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=' + self.number + '&score=0&sortType=5&page=' + pages + '&pageSize=10&isShadowSku=0&rid=0&fold=1'

    # def parse(self, response):
    #
    #     comlist = response.xpath("//div[@id='hidcomment']/div[@class='item']//div[@class='o-topic']")
    #     name = response.xpath("//div[@class='item ellipsis']/text()").extract()[0].strip()
    #
    #     for com in comlist:
    #         item = JdcommentItem()
    #         item['content'] = com.xpath(".//a/text()").extract()[0]
    #         item['date'] = com.xpath(".//span[@class='date-comment']/text()").extract()[0]
    #         item['url'] = response.url
    #         item['name'] = name
    #
    #         yield item
    #     #     self.parseCom(response)
    #     page = 0
    #     while True:
    #         if self.pages == page:
    #             break
    #         page += 1
    #         requset_url = self.comment_page_baseurl.format(str(page))
    #         try:
    #             comment_response_str = requests.get(requset_url).text
    #             response_json = json.loads(comment_response_str)
    #
    #             comments = response_json['comments']
    #             # 获取不到数据结束循环
    #             if not comments:
    #                 break
    #             for comment in comments:
    #                 item = JdcommentItem()
    #                 item['date'] = comment['creationTime']
    #                 item['content'] = comment['content']
    #                 item['url'] = response.url
    #                 item['name'] = name
    #
    #                 yield item
    #         except:
    #             # 请求失败结束循环
    #             break
    #
    #         # def parseCom(self,response):

    def start_requests(self):
        headers = {
            'authority': 'club.jd.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://item.jd.com/',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        # url模板
        url_template = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&" \
                       "productId={}&score=0&sortType=5" \
                       "&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1"

        for page in range(self.pages):  # 页数从0开始，最多爬到99页（也就是第100页）
            url = url_template.format(self.number, page)
            meta = {'productId': self.number, 'page': page}
            yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse, encoding='gbk')

    def parse(self, response):
        data_str = response.text.lstrip('fetchJSON_comment98(').rstrip(');')  # 删除前后不必要的字符，使其可被json解析
        data = json.loads(data_str)
        comments = data.get('comments')

        for comment in comments:
            loader = ItemLoader(item=JdcommentItem(), response=response)
            loader.add_value('id', comment['id'])
            loader.add_value('content', comment['content'])
            loader.add_value('date', comment['creationTime'])
            loader.add_value('name', self.name)
            loader.add_value('url', response.request.url)
            loader.add_value('isDelete', comment['isDelete'])
            loader.add_value('isTop', comment['isTop'])
            loader.add_value('topped', comment['topped'])
            loader.add_value('replyCount', comment['replyCount'])
            loader.add_value('score', comment['score'])
            loader.add_value('usefulVoteCount', comment['usefulVoteCount'])
            loader.add_value('mobileVersion', comment['mobileVersion'])
            loader.add_value('productColor', comment['productColor'])
            loader.add_value('productSize', comment['productSize'])
            loader.add_value('location', comment['location'])
            loader.add_value('referenceName', comment['referenceName'])
            loader.add_value('referenceTime', comment['referenceTime'])
            loader.add_value('nickname', comment['nickname'])
            loader.add_value('days', comment['days'])
            loader.add_value('afterDays', comment['afterDays'])
            yield loader.load_item()