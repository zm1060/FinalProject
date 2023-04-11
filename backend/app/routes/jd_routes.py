from datetime import datetime

from fastapi import APIRouter, Body, Depends

from app.celery_task.tasks import celery
from app.db.task_db import task_db
from app.db.jd_db import db
from app.dependencies import get_current_user
from app.models.user import User

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
