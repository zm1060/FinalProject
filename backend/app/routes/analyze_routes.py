from datetime import datetime

from fastapi import APIRouter, Depends

from app.celery_task.tasks import celery
from app.db.jd_db import db as jd_db
from app.db.weibo_db import db as weibo_db
from app.db.task_db import tasks_collection, task_db

router = APIRouter()

# 定义令牌过期时间和令牌加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 180


@router.post('/analyze/weibo/comment/{task_id}')
async def run_analyze_weibo_comment_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_comment_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/weibo/tweet/{task_id}')
async def run_analyze_weibo_tweet_spider(task_id: str):

    task = celery.send_task('tasks.run_analyze_weibo_tweet_spider', kwargs={
        'task_id': task_id,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/weibo/repost/{task_id}')
async def run_analyze_weibo_repost_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_repost_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/weibo/search/{task_id}')
async def run_analyze_weibo_search_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_search_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/weibo/fan/{task_id}')
async def run_analyze_weibo_fan_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_fan_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/weibo/follower/{task_id}')
async def run_analyze_weibo_follower_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_follower_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/weibo/user/{task_id}')
async def run_analyze_weibo_user_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_user_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/jd/comment/{task_id}')
async def run_analyze_jd_comment_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_jd_comment_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/analyze/jd/product/{task_id}')
async def run_analyze_jd_product_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_jd_product_spider', kwargs={
        'task_id': task_id,
        'task_type': task_type,
        'data': data,
    })

    # user_id = current_user.id
    # task_time = datetime.now()
    # new_task = {
    #     "task_id": task.id,
    #     "user_id": user_id,
    #     "task_type": "analyze_jd_comment",
    #     "task_time": task_time,
    # }
    # task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}
