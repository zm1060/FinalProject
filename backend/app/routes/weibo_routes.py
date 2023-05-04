from datetime import datetime
import json

from celery.worker.control import revoke
from fastapi import APIRouter, Body, Depends

from app.celery_task.tasks import celery
from app.db.task_db import task_db
from app.db.weibo_db import db
from app.dependencies import get_current_user
from app.es_client import es
from app.models.user import User
from app.redis_client import redis_client
from app.scrapyd import deploy_spider
from weibospider.settings import SCRAPYD_PROJECT_NAME

router = APIRouter()


@router.get('/weibo/stop_spider/{task_id}')
async def stop_spider(task_id: str, current_user: User = Depends(get_current_user)):
    # Check if the task belongs to the current user
    task = task_db["tasks"].find_one({"task_id": task_id, "user_id": current_user.id})
    if task is None:
        return {"message": "Task not found or not owned by the user."}

    # Revoke the task
    celery.control.revoke(task_id, terminate=True)
    task_db["tasks"].update_one({"task_id": task_id, "user_id": current_user.id}, {"$set": {"status": "stopped"}})

    return {"message": "Task has been stopped."}


@router.get('/weibo/resume_spider/{task_id}')
async def resume_spider(task_id: str, current_user: User = Depends(get_current_user)):
    # Check if the task belongs to the current user
    task = task_db["tasks"].find_one({"task_id": task_id, "user_id": current_user.id})
    if task is None:
        return {"message": "Task not found or not owned by the user."}

    # Get the task information
    task_kwargs = task_db["task_kwargs"].find_one({"task_id": task_id})
    task_type = task.get("task_type")

    # Send the task
    if task_type == "weibo_user":
        task = celery.send_task('tasks.run_weibo_user_spider', task_id=task_id, kwargs=task_kwargs)
    elif task_type == "weibo_search":
        task = celery.send_task('tasks.run_weibo_search_spider', task_id=task_id, kwargs=task_kwargs)
    elif task_type == "weibo_fan":
        task = celery.send_task('tasks.run_weibo_fan_spider', task_id=task_id, kwargs=task_kwargs)
    elif task_type == "weibo_tweet":
        task = celery.send_task('tasks.run_weibo_tweet_spider', task_id=task_id, kwargs=task_kwargs)
    elif task_type == "weibo_follower":
        task = celery.send_task('tasks.run_weibo_follower_spider', task_id=task_id, kwargs=task_kwargs)
    elif task_type == "weibo_comment":
        task = celery.send_task('tasks.run_weibo_comment_spider', task_id=task_id, kwargs=task_kwargs)
    elif task_type == "weibo_repost":
        task = celery.send_task('tasks.run_weibo_repost_spider', task_id=task_id, kwargs=task_kwargs)

    # Update the task information
    task_time = datetime.now()
    task_db["tasks"].update_one({"task_id": task_id, "user_id": current_user.id},
                                {"$set": {"task_time": task_time, "status": "running"}})
    return {"message": "Task has been restarted."}


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
        "task_type": "weibo_user",
        "task_time": task_time,
        "status": "running",
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
        'cookie': cookie,
        "status": "running",
    })

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "weibo_search",
        "task_time": task_time,
        "status": "running",
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
        "status": "running",
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
        "status": "running",
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
        "status": "running",
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
        "status": "running",
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
        "status": "running",
    }
    task_db["tasks"].insert_one(new_task)

    return {'task_id': task.id}


#
# @router.get("/weibo/data/user/{task_id}")
# async def get_users(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results
#
#
# @router.get("/weibo/data/search/{task_id}")
# async def get_search(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results
#
#
# @router.get("/weibo/data/comment/{task_id}")
# async def get_comments(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results
#
#
# @router.get("/weibo/data/repost/{task_id}")
# async def get_reposts(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results
#
#
# @router.get("/weibo/data/fan/{task_id}")
# async def get_fans(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results
#
#
# @router.get("/weibo/data/follower/{task_id}")
# async def get_followers(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results
#
#
# @router.get("/weibo/data/tweet/{task_id}")
# async def get_tweets(task_id: str):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         results.append(result)
#     return results


@router.post('/weibo/run_cmoplex_weibo_user_spider')
async def run_complex_weibo_user_spider(user_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    user_ids = user_data.get('user_ids')
    cookie = user_data.get('cookie')
    spider_name = 'weibo_user_spider'

    result = deploy_spider(SCRAPYD_PROJECT_NAME, spider_name)

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": result['jobid'],
        "user_id": user_id,
        "task_type": "weibo_user",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)
    return {'task_id': result['jobid']}


@router.get("/weibo/data/user/{task_id}")
async def get_weibo_users(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_user:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
    return results


@router.get("/weibo/data/search/{task_id}")
async def get_weibo_search(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_search:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
    return results


@router.get("/weibo/data/comment/{task_id}")
async def get_weibo_comments(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_comment:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="weibo_comments"):
        results = es.search(index="weibo_comments", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="weibo_comments", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="weibo_comments"):
            es.index(index="weibo_comments", body=results)
    return results


@router.get("/weibo/data/repost/{task_id}")
async def get_weibo_reposts(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_repost:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="weibo_reposts"):
        results = es.search(index="weibo_reposts", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="weibo_reposts", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="weibo_reposts"):
            es.index(index="weibo_reposts", body=results)
    return results


@router.get("/weibo/data/fan/{task_id}")
async def get_weibo_fans(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_fan:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="weibo_fans"):
        results = es.search(index="weibo_fans", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="weibo_fans", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="weibo_fans"):
            es.index(index="weibo_fans", body=results)
    return results


@router.get("/weibo/data/follower/{task_id}")
async def get_weibo_followers(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_follower:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="weibo_followers"):
        results = es.search(index="weibo_followers", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="weibo_followers", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="weibo_followers"):
            es.index(index="weibo_followers", body=results)
    return results


@router.get("/weibo/data/tweet/{task_id}")
async def get_weibo_tweets(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"weibo_tweet:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="weibo_tweets"):
        results = es.search(index="weibo_tweets", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="weibo_tweets", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="weibo_tweets"):
            es.index(index="weibo_tweets", body=results)
    return results
