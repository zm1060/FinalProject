from datetime import datetime

from fastapi import APIRouter, Body, Depends

from app.celery_task.tasks import celery
from app.db.task_db import task_db
from app.db.weibo_db import db
from app.dependencies import get_current_user
from app.models.user import User

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
        "task_type": "weibo_search",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/weibo/run_weibo_search_spider')
async def run_weibo_search_spider(search_data: dict = Body(...), current_user: User = Depends(get_current_user)):
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

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_search",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


@router.post('/weibo/run_weibo_fan_spider')
async def run_weibo_fan_spider(fan_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    user_ids = fan_data.get('user_ids')
    cookie = fan_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_fan_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_fan",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


@router.post('/weibo/run_weibo_tweet_spider')
async def run_weibo_tweet_spider(tweet_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    user_ids = tweet_data.get('user_ids')
    cookie = tweet_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_tweet_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })
    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_tweet",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


@router.post('/weibo/run_weibo_follower_spider')
async def run_weibo_follower_spider(follower_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    user_ids = follower_data.get('user_ids')
    cookie = follower_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_follower_spider', kwargs={
        'user_ids': user_ids,
        'cookie': cookie
    })

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_follower",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


@router.post('/weibo/run_weibo_comment_spider')
async def run_weibo_comment_spider(comment_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    tweet_ids = comment_data.get('tweet_ids')
    cookie = comment_data.get('cookie')

    task = celery.send_task('tasks.run_weibo_comment_spider', kwargs={
        'tweet_ids': tweet_ids,
        'cookie': cookie
    })
    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_comment",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


@router.post('/weibo/run_weibo_repost_spider')
async def run_weibo_repost_spider(repost_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    tweet_ids = repost_data.get('tweet_ids')
    cookie = repost_data.get('cookie')
    task = celery.send_task('tasks.run_weibo_repost_spider', kwargs={
        'tweet_ids': tweet_ids,
        'cookie': cookie
    })
    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_repost",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


@router.get("/weibo/data/user/{task_id}")
async def get_users(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/search/{task_id}")
async def get_search(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/comment/{task_id}")
async def get_comments(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/repost/{task_id}")
async def get_reposts(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/fan/{task_id}")
async def get_fans(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/follower/{task_id}")
async def get_followers(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results


@router.get("/weibo/data/tweet/{task_id}")
async def get_tweets(task_id: str):
    collection = db[task_id]
    results = []
    for result in collection.find():
        results.append(result)
    return results
