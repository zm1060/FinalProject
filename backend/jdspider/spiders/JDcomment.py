# -*- coding: utf-8 -*-
import json
import re

import requests
import scrapy

from jdspider.items import JdcommentItem


# 评论抓取
class JDcommentspider(scrapy.Spider):
    name = 'JDcommentspider'
    allowed_domains = ['jd.com']
    start_urls = []
    task_id = ''
    pages = ''
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
        number = re.findall(r"com/(\d+)\.html", self.start_urls[0])[0]
        # 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=' + number +'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        self.comment_page_baseurl = 'https://sclub.jd.com/comment/productPageComments.action?productId=' + number + '&score=0&sortType=5&page={0}&pageSize=10'

    def parse(self, response):

        comlist = response.xpath("//div[@id='hidcomment']/div[@class='item']//div[@class='o-topic']")
        name = response.xpath("//div[@class='item ellipsis']/text()").extract()[0].strip()

        for com in comlist:
            item = JdcommentItem()
            item['content'] = com.xpath(".//a/text()").extract()[0]
            item['date'] = com.xpath(".//span[@class='date-comment']/text()").extract()[0]
            item['url'] = response.url
            item['name'] = name

            yield item
        #     self.parseCom(response)
        page = 0
        while True:
            if self.pages == page:
                break
            page += 1
            requset_url = self.comment_page_baseurl.format(str(page))
            try:
                comment_response_str = requests.get(requset_url).text
                response_json = json.loads(comment_response_str)

                comments = response_json['comments']
                # 获取不到数据结束循环
                if not comments:
                    break
                for comment in comments:
                    item = JdcommentItem()
                    item['date'] = comment['creationTime']
                    item['content'] = comment['content']
                    item['url'] = response.url
                    item['name'] = name

                    yield item
            except:
                # 请求失败结束循环
                break

            # def parseCom(self,response):