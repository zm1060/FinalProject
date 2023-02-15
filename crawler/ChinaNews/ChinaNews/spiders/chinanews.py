import scrapy


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/']

    def parse(self, response):
        pass
