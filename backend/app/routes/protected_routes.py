from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


# 需要登录才能访问的 API
@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


# 需要登录才能访问的 API
@router.get("/protected1")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


# 其他需要保护的 API
@router.get("/protected2")
def protected_route2(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello from protected route 2, {current_user.username}!"}
