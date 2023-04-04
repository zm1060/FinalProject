import os
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from celery import Celery

from weibospider.spiders import UserSpider
from weibospider.spiders import FanSpider
from weibospider.spiders import SearchSpider

from app.config.config import BROKER_URL, BACKEND_URL

celery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)
celery.conf.task_routes = {'celery_task.tasks.*': {'queue': 'celery'}}


@celery.task(name='tasks.run_weibo_user_spider')
def run_weibo_user_spider(user_ids: list = None, cookie: str = None):
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings'
    spider_cls = UserSpider

    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    print(settings)

    runner = CrawlerRunner(settings)
    runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    d = runner.join()
    d.addBoth(stop_reactor)

    reactor.run()
    return {'message': f'Spider user finished running.'}


@celery.task(name='tasks.run_weibo_search_spider')
def run_weibo_search_spider(keywords: str = None,
                            start_time: str = None, end_time: str = None,
                            is_sort_by_hot: bool = True,
                            is_search_with_specific_time_scope: bool = False,
                            cookie: str = None):
    spider_cls = SearchSpider
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

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    d = runner.join()
    d.addBoth(stop_reactor)

    reactor.run()
    return {'message': f'Spider search finished running.'}


@celery.task(name='tasks.run_weibo_fan_spider')
def run_weibo_fan_spider(user_ids: list = None,
                         cookie: str = None):
    spider_cls = FanSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    d = runner.join()
    d.addBoth(stop_reactor)

    reactor.run()
    return {'message': f'Spider fan finished running.'}
