from typing import Optional

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.db.task_db import task_db
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
        task['_id'] = str(task['_id']) # Convert ObjectId to string
        tasks.append(task)
    return tasks
