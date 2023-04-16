from typing import Optional, List

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.celery_task.tasks import celery
from app.db.task_db import task_db, tasks_collection
from app.db.jd_db import db as jd_db
from app.db.weibo_db import db as weibo_db
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.security import hash_password

router = APIRouter()


@router.post("/analyze")
async def analyze_weibo_comments(comments: List[str]):
    tasks = [celery.send_task("tasks.analyze_weibo_comment", args=[comment]) for comment in comments]
    return {"task_ids": [task.id for task in tasks]}
