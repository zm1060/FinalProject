# -*- coding: utf-8 -*-

BOT_NAME = 'weibospider'

SPIDER_MODULES = ['weibospider.spiders']
NEWSPIDER_MODULE = 'weibospider.spiders'

ROBOTSTXT_OBEY = False
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

import logging

LOG_LEVEL = logging.DEBUG
LOG_FILE = "scrapy.log"

REDIRECT_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': 'SINAGLOBAL=8252028727715.401.1680441598475; ULV=1680581502666:3:3:3:2790934677259.962.1680581502664:1680539175868; XSRF-TOKEN=01m6lrt_NABY1myBXbnv1SDF; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFpiKTAU84zZdgbTJsxkMpL5JpX5KMhUgL.FoMc1Kn0So-4Sh22dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSo.Re0qf1KBp; ALF=1683288665; SSOLoginState=1680696666; SCF=Al8ZfJLvSv9Oaq3LuqOGIi8SeV-z8VbOcOjZmC0bsqj5QPTakJmgxH9C4oiL0JdCi8ONrkTAtXuXI6uFs05KrJk.; SUB=_2A25JKRULDeRhGeFI4loS9ivFzz2IHXVqXwHDrDV8PUNbmtAbLUnjkW9NfKoiQTdAxQFJxdXGdp-5EFMEDei_9-Fu; WBPSESS=_BtcVNwO9mu_wNTnWfVSOdL_SRdOhwFGjUMOy2GhHtoK9I9OTFY5aPcwpXl8A6hpRyt-vH6azQYbTnOzRyYUatHHmxZtxzPmgLHFKuy2VChTPMSmQ0wnAPQmmT4dZAzErSHB1Bx4WEzvnKoviIWhew=='
}

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'scrapy.extensions.telnet.TelnetConsole': 500,
    'weibospider.middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'weibospider.pipelines.MongoDBPipeline': 300,
}
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'weibo'
