import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routes.auth_routes import router as auth_router
from app.routes.protected_routes import router as protected_router
from app.routes.weibo_routes import router as weibo_router
from app.routes.user_routes import router as user_router
from app.routes.jd_routes import router as jd_router

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(weibo_router)
app.include_router(user_router)
app.include_router(jd_router)
# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ignore_dirs = ["mongodb/data", "static/images"]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload_dirs=[ignore_dirs])
