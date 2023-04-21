import io
from urllib.parse import unquote

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from app.celery_task.tasks import celery
from app.db.weibo_db import db as weibo_db
from app.db.task_db import tasks_collection
from app.redis_client import redis_client

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

    task = celery.send_task('tasks.run_analyze_weibo_comment', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/weibo/tweet/{task_id}')
async def run_analyze_weibo_tweet_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_tweet', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/weibo/repost/{task_id}')
async def run_analyze_weibo_repost_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_repost', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/weibo/search/{task_id}')
async def run_analyze_weibo_search_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_search', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/weibo/fan/{task_id}')
async def run_analyze_weibo_fan_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_fan', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/weibo/follower/{task_id}')
async def run_analyze_weibo_follower_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_follower', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/weibo/user/{task_id}')
async def run_analyze_weibo_user_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_weibo_user', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/jd/comment/{task_id}')
async def run_analyze_jd_comment_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_jd_comment', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


@router.post('/analyze/jd/product/{task_id}')
async def run_analyze_jd_product_spider(task_id: str):
    # Use the task_id to get the task_type
    task_type = tasks_collection.find_one({"task_id": task_id})['task_type']
    collection = weibo_db[task_id]

    # Find the data that matches the query
    data = list(collection.find())

    task = celery.send_task('tasks.run_analyze_jd_product', kwargs={
        'task_id': task_id,
    })

    return {'task_id': task.id}


# @router.get("/analyze/result/{task_id}/{tab_key}")
# async def get_image(task_id: str, tab_key: str):
#     # construct the Redis key
#     print(task_id+'_'+tab_key)
#     redis_key = f"{task_id}:{tab_key}"
#
#     # check if the key exists in Redis
#     if not redis_client.exists(redis_key):
#         return {"error": "Image data not found."}
#
#     # retrieve the image data from Redis
#     image_data = redis_client.get(redis_key)
#     print(image_data)
#     # create a streaming response for the image data
#     return StreamingResponse(io.BytesIO(image_data), media_type="image/png")

@router.get("/analyze/result/{task_id}/{chart_type}")
async def get_analyze_result(task_id: str, chart_type: str):
    chart_type = unquote(chart_type)
    redis_key = f"{task_id}_{chart_type}"
    print(redis_key)
    # Check if the key exists in Redis
    if not redis_client.exists(redis_key):
        return {"error": "Image data not found."}

    # Retrieve the image data from Redis
    image_data = redis_client.get(redis_key)

    # Return the image data as a response with the appropriate media type
    return Response(content=image_data, media_type="image/png")