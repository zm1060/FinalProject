import scrapy
from bs4 import BeautifulSoup

class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['www.chinanews.com']
    start_urls = ['http://www.chinanews.com/']

    def parse(self, response):
        soup = BeautifulSoup(response.text)
        for item in soup.select('a'):
            print(item)
  