from datetime import datetime

from fastapi import APIRouter, Body, Depends
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from app.celery_task.tasks import celery
from app.db.task_db import task_db
from app.db.weibo_db import db
from app.dependencies import get_current_user
from app.models.user import User
from weibospider.spiders import UserSpider

router = APIRouter()


# 微博用户
@router.post('/weibo/run_weibo_user_spider')
async def run_weibo_user_spider(user_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    user_ids = user_data.get('user_ids')
    cookie = user_data.get('cookie')
    task = celery.send_task('tasks.run_weibo_user_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/weibo/simple_run_weibo_user_spider')
async def simple_run_weibo_user_spider(user_data: dict = Body(...)):
    user_ids = user_data.get('user_ids')
    cookie = user_data.get('cookie')
    spider_cls = UserSpider
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
    return {'message': f'Spider user finished running.'}


@router.post('/weibo/run_weibo_search_spider')
async def run_weibo_search_spider(search_data: dict = Body(...)):
    keywords = search_data.get('keywords')
    start_time = search_data.get('start_time')
    end_time = search_data.get('end_time')
    is_sort_by_hot = search_data.get('is_sort_by_hot')
    is_search_with_specific_time_scope = search_data.get('is_search_with_specific_time_scope')
    cookie = search_data.get('cookie')
    print(is_sort_by_hot)
    task = celery.send_task('tasks.run_weibo_search_spider', kwargs={
        'keywords': keywords,
        'start_time': start_time,
        'end_time': end_time,
        'is_sort_by_hot': is_sort_by_hot,
        'is_search_with_specific_time_scope': is_search_with_specific_time_scope,
        'cookie': cookie
    })
    return {'task_id': task.id}


@router.post('/weibo/run_weibo_fan_spider')
async def run_weibo_fan_spider(fan_data: dict = Body(...)):
    user_ids = fan_data.get('user_ids')
    cookie = fan_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_fan_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })
    return {'task_id': task.id}


@router.post('/weibo/run_weibo_tweet_spider')
async def run_weibo_tweet_spider(tweet_data: dict = Body(...)):
    user_ids = tweet_data.get('user_ids')
    cookie = tweet_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_tweet_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })
    return {'task_id': task.id}


@router.post('/weibo/run_weibo_follower_spider')
async def run_weibo_follower_spider(follower_data: dict = Body(...)):
    user_ids = follower_data.get('user_ids')
    cookie = follower_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_follower_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })
    return {'task_id': task.id}


@router.post('/weibo/run_weibo_comment_spider')
async def run_weibo_comment_spider(comment_data: dict = Body(...)):
    tweet_ids = comment_data.get('tweet_ids')
    cookie = comment_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_comment_spider', kwargs={
        'tweet_ids': tweet_ids,
        'cookie': cookie
    })
    return {'task_id': task.id}


@router.post('/weibo/run_weibo_repost_spider')
async def run_weibo_repost_spider(repost_data: dict = Body(...)):
    tweet_ids = repost_data.get('tweet_ids')
    cookie = repost_data.get('cookie')
    task = celery.send_task('tasks.run_weibo_repost_spider', kwargs={
        'tweet_ids': tweet_ids,
        'cookie': cookie
    })

    return {'task_id': task.id}


@router.get("/weibo/data/user/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/search/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/comment/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/repost/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/fan/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/follower/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/tweet/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results