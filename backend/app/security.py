from jose import JWTError, jwt
from typing import Optional
import logging
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User

# 加载密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
# 建议自己使用generate_secret_key.py生成新的key
SECRET_KEY = "VrevATwNtvMnMV7MOO4ljlXPGfHmuZt4KPqv7yZ-xAo"

# 获取密码哈希值的函数
def hash_password(password: str):
    return pwd_context.hash(password)


# 验证密码的函数
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# 生成访问令牌的函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证 JWT token
def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get("sub")
        logging.debug("decoded_token: %s", decoded_token)
        logging.debug("username: %s", username)

        if username is None:
            raise JWTError
        token_data = {"username": username}
        return token_data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")


# 验证用户登录信息
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
