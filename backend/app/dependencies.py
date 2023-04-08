from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 获取用户信息
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# 获取数据库会话的函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 创建一个用于路由保护的依赖项函数，用于检查用户是否已登录并具有访问所需资源的权限
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    username = token_data["username"]
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user
