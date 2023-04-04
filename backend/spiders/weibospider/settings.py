# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_FILE = 'scrapy.log'


DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': 'SINAGLOBAL=8252028727715.401.1680441598475; ULV=1680441598477:1:1:1:8252028727715.401.1680441598475:; ALF=1683117165; SSOLoginState=1680525169; SCF=Al8ZfJLvSv9Oaq3LuqOGIi8SeV-z8VbOcOjZmC0bsqj57hssQVNDPISZQF9AuyZRQEM-Cx7rHzRDyIp33rVwieo.; XSRF-TOKEN=PrdkIzZQREECo5bDKiUuKhZ2; SUB=_2AkMTdkaUdcPxrARSkfgSxGPhaIVH-jygoy9iAn7uJhIyOhhq7lImqSVutBF-XEGkrXpVc_P94Vc8_mgUc6_KFwgY; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5shDzPXr8DRKPNvuCBnVCV5JpX5KMhUgL.FoM01K5N1hn0Shn2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNe0.7S0nRe0BR; WBPSESS=Dt2hbAUaXfkVprjyrAZT_JfAHG3fD9kls2hEBPFRn9UFyMIyr-qW4gagP0IiSLb45waGWp_HuuTedvblD9-CIhOR6lHNFq5yXZbflQE1QkcLPIrjcLUgZ77Qn7IuMkjVXS95p_q4U4nV8qzVeGPa1w=='
}

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'scrapy.extensions.telnet.TelnetConsole': 500,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}
#
# ITEM_PIPELINES = {
#     'pipelines.JsonWriterPipeline': 300,
# }
ITEM_PIPELINES = {
    'pipelines.MongoDBPipeline': 300,
}
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'weibo'
