import os
import signal

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from celery import Celery

from jdspider.spiders.JDcomment import JDcommentspider
from jdspider.spiders.JDspider import JDspider
from weibospider.spiders import UserSpider, TweetSpider, FollowerSpider, CommentSpider, RepostSpider, FanSpider, \
    SearchSpider
from app.config.config import BROKER_URL, BACKEND_URL

celery = Celery('tasks', broker=BROKER_URL, backend=BACKEND_URL)
celery.conf.task_routes = {'celery_task.tasks.*': {'queue': 'celery'}}

import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()],
)


@celery.task(name='tasks.run_weibo_user_spider', bind=True)
def run_weibo_user_spider(self, user_ids: list = None, cookie: str = None):
    task_id = self.request.id
    task_type = 'weibo_user'
    spider_cls = UserSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings'  # set the settings module for weibospider
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider_cls, **spider_kwargs)

    def stop_reactor():
        reactor.stop()

    deferred.addBoth(stop_reactor)

    def stop_task(signum, frame):
        reactor.callFromThread(reactor.stop)

    signal.signal(signal.SIGTERM, stop_task)

    try:
        reactor.run()
    except Exception as e:
        return {'message': f'Spider {task_type} failed to run.'}

    # stats = runner.stats.get_stats()
    # tasks_collection.update_one({'task_id': task_id}, {'$set': {'stats': stats}}, upsert=True)

    return {'message': f'Spider {task_type} finished running.'}


@celery.task(name='tasks.run_weibo_search_spider', bind=True)
def run_weibo_search_spider(self, keywords: str = None,
                            start_time: str = None, end_time: str = None,
                            is_sort_by_hot: bool = True,
                            is_search_with_specific_time_scope: bool = False,
                            cookie: str = None):
    task_id = self.request.id
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
    if task_id:
        spider_kwargs['task_id'] = task_id

    spider_kwargs['is_sort_by_hot'] = is_sort_by_hot
    spider_kwargs['is_search_with_specific_time_scope'] = is_search_with_specific_time_scope
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings' # set the settings module for weibospider
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


@celery.task(name='tasks.run_weibo_fan_spider', bind=True)
def run_weibo_fan_spider(self, user_ids: list = None,
                         cookie: str = None):
    task_id = self.request.id
    spider_cls = FanSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings' # set the settings module for weibospider
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


@celery.task(name='tasks.run_weibo_tweet_spider', bind=True)
def run_weibo_tweet_spider(self, user_ids: list = None, cookie: str = None):
    task_id = self.request.id
    spider_cls = TweetSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings' # set the settings module for weibospider
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


@celery.task(name='tasks.run_weibo_follower_spider', bind=True)
def run_weibo_follower_spider(self, user_ids: list = None,
                              cookie: str = None):
    task_id = self.request.id
    spider_cls = FollowerSpider
    spider_kwargs = {}
    if user_ids:
        spider_kwargs['user_ids'] = user_ids
    if cookie:
        spider_kwargs['cookie'] = cookie
    if task_id:
        spider_kwargs['task_Id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings' # set the settings module for weibospider
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


@celery.task(name='tasks.run_weibo_comment_spider', bind=True)
def run_weibo_comment_spider(self, tweet_ids: list = None, cookie: str = None):
    task_id = self.request.id
    spider_cls = CommentSpider
    spider_kwargs = {}
    if tweet_ids:
        spider_kwargs['tweet_ids'] = tweet_ids
    if cookie:
        spider_kwargs['cookie'] = cookie
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings' # set the settings module for weibospider
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


@celery.task(name='tasks.run_weibo_repost_spider', bind=True)
def run_weibo_repost_spider(self, tweet_ids=None, cookie=None):
    task_id = self.request.id
    spider_cls = RepostSpider
    spider_kwargs = {}
    if tweet_ids:
        spider_kwargs['tweet_ids'] = tweet_ids
    if cookie:
        spider_kwargs['cookie'] = cookie
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'weibospider.settings' # set the settings module for weibospider
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


@celery.task(name='tasks.run_jd_product_spider', bind=True)
def run_jd_product_spider(self, search_name=None):
    task_id = self.request.id
    spider_cls = JDspider
    spider_kwargs = {}
    if search_name:
        spider_kwargs['search_name'] = search_name
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'jdspider.settings' # set the settings module for jdspider
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
    return {'message': f'Spider JD Product finished running.'}


@celery.task(name='tasks.run_jd_comment_spider', bind=True)
def run_jd_comment_spider(self, urls=None, pages=None):
    task_id = self.request.id
    spider_cls = JDcommentspider
    spider_kwargs = {}
    if urls:
        spider_kwargs['urls'] = urls
    if pages:
        spider_kwargs['pages'] = pages
    if task_id:
        spider_kwargs['task_id'] = task_id
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'jdspider.settings' # set the settings module for jdspider
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
    return {'message': f'Spider JD Comment Spider finished running.'}
