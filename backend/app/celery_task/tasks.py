
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from celery import Celery
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

from app.config.config import BROKER_URL, BACKEND_URL


celery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)
celery.conf.task_routes = {'celery_task.tasks.*': {'queue': 'celery'}}


@celery.task(name='tasks.run_weibo_user_spider')
def run_weibo_user_spider(run_mode: str, user_ids: list = None, cookie: str = None):
    process = CrawlerProcess(get_project_settings())

    mode_to_spider = {
        'comment': CommentSpider,
        'fan': FanSpider,
        'follow': FollowerSpider,
        'tweet': TweetSpider,
        'user': UserSpider,
        'repost': RepostSpider,
        'search': SearchSpider
    }

    spider_cls = mode_to_spider[run_mode]
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    process.crawl(spider_cls, **spider_kwargs)
    process.start()
    # Wait for the process to finish
    process.join()
    return {'message': f'Spider {run_mode} finished running.'}


@celery.task(name='tasks.run_weibo_search_spider')
def run_weibo_search_spider(run_mode: str, keywords: str = None,
                            start_time: str = None, end_time: str = None,
                            is_sort_by_hot: bool = True,
                            is_search_with_specific_time_scope: bool = False,
                            cookie: str = None):
    process = CrawlerProcess(get_project_settings())

    mode_to_spider = {
        'comment': CommentSpider,
        'fan': FanSpider,
        'follow': FollowerSpider,
        'tweet': TweetSpider,
        'user': UserSpider,
        'repost': RepostSpider,
        'search': SearchSpider
    }

    spider_cls = mode_to_spider[run_mode]
    spider_kwargs = {}
    if keywords:
        spider_kwargs['keywords'] = keywords
    if start_time:
        spider_kwargs['start_time'] = start_time
    if end_time:
        spider_kwargs['end_time'] = end_time
    if cookie:
        spider_kwargs['cookie'] = cookie
    spider_kwargs['is_sort_by_hot'] = is_sort_by_hot
    spider_kwargs['is_search_with_specific_time_scope'] = is_search_with_specific_time_scope

    process.crawl(spider_cls, **spider_kwargs)
    process.start()
    # Wait for the process to finish
    process.join()
    return {'message': f'Spider {run_mode} finished running.'}
