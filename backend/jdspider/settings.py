SCRAPYD_PROJECT_NAME = 'jd'
BOT_NAME = 'jdspider'


SPIDER_MODULES = ['jdspider.spiders']
NEWSPIDER_MODULE = 'jdspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'jd (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

import logging

LOG_LEVEL = logging.DEBUG
LOG_FILE = "scrapy.log"

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:

# CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2
AUTOTHROTTLE_ENABLED= True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.5
AUTOTHROTTLE_MAX_DELAY = 60
DOWNLOAD_DELAY = 0.5
# CONCURRENT_REQUESTS_PER_IP = 0
#Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'jdspider.middlewares.JdspiderSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'jdspiders.middlewares.MyCustomDownloaderMiddleware': 543,
    # 'jdspider.middlewares.EmailNotificationMiddleware': 999,
    ## 'jdspider.middlewares.ProxyDownloaderMiddleware': 100,
    'jdspider.middlewares.UserAgentmiddleware': 400,
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

SCRAPEOPS_API_KEY = 'f2a6e395-b730-498d-a642-ae125870cf32'

EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
    'scrapy.extensions.telnet.TelnetConsole': None,
}


ITEM_PIPELINES = {
    'jdspider.pipelines.JDspiderPipeline': 290,
    'jdspider.pipelines.JDcommentPipeline': 290,
}


# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
import os

MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
# MONGO_URI = 'mongodb://localhost:27017/'
# MONGO_URI = 'mongodb://mongodb:27017/'
MONGODB_DATABASE = 'jd'

MAIL_FROM = '1575098153@qq.com'
MAIL_HOST = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USER = '1575098153@qq.com'
MAIL_PASS = 'gfwoermfghvwfjgf'
MAIL_TLS = True
MAIL_SSL = False
MAIL_SUBJECT = 'Scrapy notification'
MAIL_TO = ['1575098153@qq.com', '248334369@qq.com']