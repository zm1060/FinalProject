import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI

from model.User import User
from model.Task import Task

app = FastAPI()

@app.post("/task/create")
async def create_task(task: Task):
    crawler_url = task.url
    crawler_keywords = task.keywords
    crawler_status = task.status
    crawler_type = task.type

    run_para = "/search?"
    for keyword in crawler_keywords:
        run_para = run_para+"keyword="+keyword
    run_url = crawler_url + run_para
    return {"url":crawler_url+run_para}

@app.post("/login")
async def login(user: User):
    # check if user exists
    if True:
        return {"result": "success",
                "token": "None"}
    else:
        return {"result": "error"}

@app.post("/register")
async def register(user: User):
    # check if user exists
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)