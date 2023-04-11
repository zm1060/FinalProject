# -*- coding: utf-8 -*-
import re

import lxml
import lxml.etree
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jdspider.items import JdspiderItem


# 提取一种类别商品信息
class JDspider(CrawlSpider):
    name = 'JDspider'
    allowed_domains = ['jd.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            'jdspider.pipelines.JDspiderPipeline': 300,
        },
        'DEPTH_PRIORITY': 1,
        'DEPTH_LIMIT': 3,
    }

    linkExtractor = LinkExtractor(allow=(r'jd\.com/\d+\.html',))
    rules = [
        Rule(linkExtractor, callback='JDparse', follow=True),
    ]

    def __init__(self, serach_name=None):
        super(JDspider, self).__init__()
        self.start_urls = [
            'https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=bjb&pvid=39022e74e5c345b5955e121fdca849b7' % serach_name]

    def JDparse(self, response):

        namelist = []
        contentlist = []

        item = JdspiderItem()
        html = lxml.etree.HTML(response.body)

        infolist = html.xpath("//*[@id=\"detail\"]/div[2]/div//dl")

        name = html.xpath("//div[@class='item ellipsis']/text()")[0].strip()

        # print("商品名称：", name)
        namelist.append("商品名称")
        contentlist.append(name)
        # item['name'] = name

        try:
            baozhuang = html.xpath("//div[@class='package-list']/p/text()")[0].strip().replace("\n", '、')
        except:
            baozhuang = "未列明"
        # print("包装清单：", baozhuang)
        namelist.append("包装清单")
        contentlist.append(baozhuang)

        # jieshao = html.xpath("//div[@class='item hide']/text()")[0]
        # print("商品简介：",jieshao)

        # 京东的价格采用ajax动态加载，而且同一IP请求过于频繁可能触发验证码，这里很坑
        # 如果触发验证码则获取不到价格信息，暂时没找到好的解决办法，添加异常处理
        try:
            number = re.findall(r"com/(\d+)\.html", url)[0]
            # print(number)

            ajaxUrl = r"https://p.3.cn/prices/mgets?pdtk=&skuIds=J_" + number

            ajaxResponse = requests.get(ajaxUrl)
            # print(ajaxResponse.text)
            prices = re.findall('"p":"(.*?)"', ajaxResponse.text)[0].strip()
            # print("价格：", prices)

        except:
            prices = "获取失败"

        namelist.append("价格")
        contentlist.append(prices)

        for info in infolist:
            titles = info.xpath("./dt/text()")
            contents = info.xpath("./dd/text()")
            for title, content in zip(titles, contents):
                # print(title, ':', content)
                namelist.append(title.strip())
                contentlist.append(content.strip())

        item['name'] = namelist
        item['content'] = contentlist
        item['url'] = response.url

        yield item
