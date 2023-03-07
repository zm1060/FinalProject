# -*- coding: utf-8 -*-

BOT_NAME = 'spider'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': ''
}


def from_crawler(cls, crawler):
    settings = crawler.settings

    # If user has passed a cookie, add it to the default headers
    if 'cookie' in settings:
        headers = settings.get('DEFAULT_REQUEST_HEADERS', {})
        headers['Cookie'] = settings.get('cookie')
        settings.set('DEFAULT_REQUEST_HEADERS', headers)
    else:
        with open('cookie.txt', 'rt', encoding='utf-8') as f:
            cookie = f.read().strip()
        headers = settings.get('DEFAULT_REQUEST_HEADERS', {})
        headers['Cookie'] = cookie
        settings.set('DEFAULT_REQUEST_HEADERS', headers)

    return cls(settings)


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
    #'pipelines.JsonWriterPipeline': 300,
}

# MONGO_URI = 'mongodb://localhost:27017/'
MONGO_URI = 'mongodb://mongodb:27017/'
MONGO_DATABASE = 'weibo'
