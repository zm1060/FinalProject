# auth_routes.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user import User, UserCreate
from app.security import hash_password, create_access_token, verify_password

router = APIRouter()

# 定义令牌过期时间和令牌加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 180


# 定义登录路由
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# 定义注册路由
@router.post("/register")
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_create.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user_create.password)
    new_user = User(username=user_create.username, email=user_create.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
