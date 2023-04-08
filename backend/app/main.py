import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routes.auth_routes import router as auth_router
from app.routes.protected_routes import router as protected_router
from app.routes.weibo_routes import router as weibo_router

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(weibo_router)
# 跨域资源共享中间件设置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Authorization"],
)

ignore_dirs = ["mongodb/data", "static/images"]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload_dirs=[ignore_dirs])
