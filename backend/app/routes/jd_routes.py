from datetime import datetime

from fastapi import APIRouter, Body, Depends

from app.celery_task.tasks import celery
from app.db.task_db import task_db
from app.db.jd_db import db
from app.dependencies import get_current_user
from app.es_client import es
from app.models.user import User
from app.redis_client import redis_client

router = APIRouter()


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
