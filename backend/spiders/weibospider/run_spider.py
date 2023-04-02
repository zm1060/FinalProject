import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.weibospider.spiders.tweet import TweetSpider
from spiders.weibospider.spiders import CommentSpider
from spiders.weibospider.spiders import FollowerSpider
from spiders.weibospider.spiders import UserSpider
from spiders.weibospider.spiders import FanSpider
from spiders.weibospider.spiders import RepostSpider
from spiders.weibospider.spiders import SearchSpider

if __name__ == '__main__':
    mode = 'follow'
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'comment': CommentSpider,
        'fan': FanSpider,
        'follow': FollowerSpider,
        'tweet': TweetSpider,
        'user': UserSpider,
        'repost': RepostSpider,
        'search': SearchSpider
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()
