import os
import signal

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from celery import Celery

from weibospider.spiders import UserSpider, TweetSpider, FollowerSpider, CommentSpider, RepostSpider, FanSpider, \
    SearchSpider
from app.config.config import BROKER_URL, BACKEND_URL

celery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)
celery.conf.task_routes = {'celery_task.tasks.*': {'queue': 'celery'}}
os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings'

import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()],
)


@celery.task(name='tasks.run_weibo_user_spider')
def run_weibo_user_spider(user_ids: list = None, cookie: str = None):
    spider_cls = UserSpider

    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()

    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

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
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

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
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    reactor.run()
    return {'message': f'Spider fan finished running.'}


@celery.task(name='tasks.run_weibo_search_spider')
def run_weibo_search_spider(keywords: str = None,
                            start_time: str = None, end_time: str = None,
                            is_sort_by_hot: bool = True,
                            is_search_with_specific_time_scope: bool = False,
                            cookie: str = None):
    spider_cls = SearchSpider
    spider_kwargs = {}
    if keywords:
        spider_kwargs['keywords'] = keywords.split(',')
    if start_time:
        spider_kwargs['start_time'] = start_time
    if end_time:
        spider_kwargs['end_time'] = end_time
    if is_sort_by_hot is False:
        spider_kwargs['is_sort_by_hot'] = is_sort_by_hot
    if is_search_with_specific_time_scope:
        spider_kwargs['is_search_with_specific_time_scope'] = is_search_with_specific_time_scope
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    reactor.run()
    return {'message': f'Spider search finished running.'}


@celery.task(name='tasks.run_weibo_tweet_spider')
def run_weibo_tweet_spider(user_ids: list = None, cookie: str = None):
    spider_cls = TweetSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    reactor.run()
    return {'message': f'Spider tweet finished running.'}


@celery.task(name='tasks.run_weibo_follower_spider')
def run_weibo_follower_spider(user_ids: list = None,
                              cookie: str = None):
    spider_cls = FollowerSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    reactor.run()
    return {'message': f'Spider follower finished running.'}


@celery.task(name='tasks.run_weibo_comment_spider')
def run_weibo_comment_spider(tweet_ids: list = None, cookie: str = None):
    spider_cls = CommentSpider
    spider_kwargs = {}
    if tweet_ids:
        spider_kwargs['tweet_ids'] = tweet_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    reactor.run()
    return {'message': f'Spider comment finished running.'}


@celery.task(name='tasks.run_weibo_repost_spider')
def run_weibo_repost_spider(tweet_ids=None, cookie=None):
    spider_cls = RepostSpider
    spider_kwargs = {}
    if tweet_ids:
        spider_kwargs['tweet_ids'] = tweet_ids
    if cookie:
        spider_kwargs['cookie'] = cookie

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    # Add signal handler to stop the reactor when the Celery worker is terminated
    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    reactor.run()
    return {'message': f'Spider repost finished running.'}
