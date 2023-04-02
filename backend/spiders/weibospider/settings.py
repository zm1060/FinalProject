# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': ''
}

TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

REQUEST_FINGERPRINTER_IMPLEMENTATION = 'scrapy.resolver.CachingThreadedResolver'

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.MongoDBPipeline': 300,
    # 'pipelines.JsonWriterPipeline': 300,
}

MONGO_URI = 'mongodb://localhost:27017/'
# MONGO_URI = 'mongodb://mongodb:27017/'
MONGO_DATABASE = 'weibo'
