from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from models import user
from db.database import SessionLocal
from models.user import User, UserCreate

import logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# 加载密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 跨域资源共享中间件设置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义令牌过期时间和令牌加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 180
ALGORITHM = "HS256"
# 建议自己使用generate_secret_key.py生成新的key
SECRET_KEY = "VrevATwNtvMnMV7MOO4ljlXPGfHmuZt4KPqv7yZ-xAo"


# 获取数据库会话的函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取密码哈希值的函数
def hash_password(password: str):
    return pwd_context.hash(password)


# 验证密码的函数
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# 获取用户信息
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# 验证用户登录信息
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 创建一个用于路由保护的依赖项函数，用于检查用户是否已登录并具有访问所需资源的权限
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    username = token_data["username"]
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user


# 定义登录路由
@app.post("/login")
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
@app.post("/register")
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

# 需要登录才能访问的 API
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


# 需要登录才能访问的 API
@app.get("/protected1")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}


# 其他需要保护的 API
@app.get("/protected2")
def protected_route2(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello from protected route 2, {current_user.username}!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
