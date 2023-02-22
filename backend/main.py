import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException


from model.User import User
from model.Task import Task

app = FastAPI()



def send_email(email, message):
    pass

@app.get("/")
async def ping(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "email@address.com", "Hi!")
    return {"message": "pong!"}


# Define API endpoints
@app.post("/spiders")
async def create_spider(url: str):
    task = crawl.delay(url)
    return {"task_id": task.id}

@app.get("/spiders/{task_id}")
async def get_spider(task_id: str):
    task = celery_app.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": "completed", "result": task.result}
    elif task.state == "PENDING":
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        raise HTTPException(status_code=500, detail="Task failed")

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