from datetime import datetime

from celery.worker.control import revoke
from fastapi import APIRouter, Body, Depends

from app.celery_task.tasks import celery
from app.db.task_db import task_db
from app.db.jd_db import db
from app.dependencies import get_current_user
from app.es_client import es
from app.models.user import User
from app.redis_client import redis_client

router = APIRouter()


@router.post('/jd/stop_spider')
async def stop_spider(task_id: str, current_user: User = Depends(get_current_user)):
    # Check if the task belongs to the current user
    task = task_db["tasks"].find_one({"task_id": task_id, "user_id": current_user.id})
    if task is None:
        return {"message": "Task not found or not owned by the user."}

    # Revoke the task
    revoke(task_id, terminate=True)
    task_db["tasks"].delete_one({"task_id": task_id})

    return {"message": "Task has been stopped."}

@router.post('/jd/restart_spider')
async def restart_spider(task_id: str, current_user: User = Depends(get_current_user)):
    # Check if the task belongs to the current user
    task = task_db["tasks"].find_one({"task_id": task_id, "user_id": current_user.id})
    if task is None:
        return {"message": "Task not found or not owned by the user."}

    # Get the task information
    task_kwargs = task_db["task_kwargs"].find_one({"task_id": task_id})
    task_type = task.get("task_type")

    # Send the task
    task = None
    if task_type == "jd_product":
        task = celery.send_task('tasks.run_jd_product_spider', kwargs=task_kwargs)
    elif task_type == "jd_comment":
        task = celery.send_task('tasks.run_jd_comment_spider', kwargs=task_kwargs)

    # Update the task information
    task_time = datetime.now()
    task_db["tasks"].update_one({"task_id": task_id}, {"$set": {"task_time": task_time}})

    return {"message": "Task has been restarted."}


@router.post('/jd/run_jd_product_spider')
async def run_jd_product_spider(search_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    search_name = search_data.get('search_name')
    task = celery.send_task('tasks.run_jd_product_spider', kwargs={
        'search_name': search_name
    })

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "jd_product",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


@router.post('/jd/run_jd_comment_spider')
async def run_jd_comment_spider(comment_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    urls = comment_data.get('urls')
    pages = comment_data.get('pages')
    task = celery.send_task('tasks.run_jd_comment_spider', kwargs={
        'urls': urls,
        'pages': pages
    })

    user_id = current_user.id
    task_time = datetime.now()
    new_task = {
        "task_id": task.id,
        "user_id": user_id,
        "task_type": "jd_comment",
        "task_time": task_time,
    }
    task_db["tasks"].insert_one(new_task)
    return {'task_id': task.id}


import json


@router.get("/jd/data/product/{task_id}")
async def get_jd_product(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"jd_product:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="jd_products"):
        results = es.search(index="jd_products", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="jd_products", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            result['_id'] = str(result['_id'])  # convert ObjectId to string
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="jd_products"):
            es.index(index="jd_products", body=results)
    return results


@router.get("/jd/data/comment/{task_id}")
async def get_jd_comments(task_id: str, current_user: User = Depends(get_current_user)):
    cache_key = f"jd_comment:{task_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        results = json.loads(cached_data)
    elif es.indices.exists(index="jd_comments"):
        results = es.search(index="jd_comments", body={"query": {"match": {"task_id": task_id}}})['hits']['hits']
        if results:
            results = [result['_source'] for result in results]
            redis_client.set(cache_key, json.dumps(results))
            es.index(index="jd_comments", body=results)
    else:
        collection = db[task_id]
        results = []
        for result in collection.find():
            result['_id'] = str(result['_id'])  # convert ObjectId to string
            results.append(result)
        redis_client.set(cache_key, json.dumps(results))
        if es.indices.exists(index="jd_comments"):
            es.index(index="jd_comments", body=results)
    return results



# @router.get("/jd/data/product/{task_id}")
# async def get_jd_product(task_id: str, current_user: User = Depends(get_current_user)):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         result['_id'] = str(result['_id'])  # convert ObjectId to string
#         results.append(result)
#     return results
#
#
# @router.get("/jd/data/comment/{task_id}")
# async def get_jd_comments(task_id: str, current_user: User = Depends(get_current_user)):
#     collection = db[task_id]
#     results = []
#     for result in collection.find():
#         result['_id'] = str(result['_id'])  # convert ObjectId to string
#         results.append(result)
#     return results

# @router.get('/jd/run_jd_product_direct')
# async def run_jd_product_direct():
#     settings = get_project_settings()
#     process = CrawlerProcess(settings=settings)
#     process.crawl(JDspider, 'iphone', '123123-213123')
#
#     process.start()
