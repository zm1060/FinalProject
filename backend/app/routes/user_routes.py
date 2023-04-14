from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.db.task_db import task_db
from app.db.jd_db import db as jd_db
from app.db.weibo_db import db as weibo_db
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.security import hash_password

router = APIRouter()


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


# 更新用户
@router.put("/me")
async def update_user_info(
        new_username: Optional[str] = Body(None),
        new_email: Optional[str] = Body(None),
        new_password: Optional[str] = Body(None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if new_username:
        current_user.username = new_username
    if new_email:
        current_user.email = new_email
    if new_password:
        current_user.password = hash_password(new_password)
    db.commit()
    db.refresh(current_user)
    return current_user


# 删除用户
@router.delete("/me")
async def delete_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get("/user/tasks")
async def get_current_user_tasks(current_user: User = Depends(get_current_user)):
    tasks_collection = task_db['tasks']
    tasks = []
    for task in tasks_collection.find({"user_id": current_user.id}):
        task['_id'] = str(task['_id'])  # Convert ObjectId to string
        tasks.append(task)
    return tasks


@router.delete("/user/tasks/{task_id}")
async def delete_task(task_id: str, current_user: User = Depends(get_current_user)):
    tasks_collection = task_db['tasks']
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if task["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this delete action.")

    if task:
        task_type = task['task_type']
        if task_type.startswith('weibo'):
            weibo_collection = weibo_db[str(task_id)]
            weibo_collection.delete_one({'_id': ObjectId(task_id)})
        elif task_type.startswith('jd'):
            jd_collection = jd_db[str(task_id)]
            jd_collection.delete_one({'_id': ObjectId(task_id)})
        result = await tasks_collection.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count == 1:
        return {"message": "Task deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Task not found.")
