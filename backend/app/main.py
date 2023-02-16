from fastapi import BackgroundTasks, FastAPI
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crawler.ChinaNews import run_china_news
app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(weibo, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

@app.post("/run-spider/ChinaNews")
async def crawler_china_new():
    out, err = run_scrapy_spider()
    json_response = jsonable_encoder(response)
    if err:
        response = {'status': 'error', 'message': err}
    else:
        response = {'status': 'success', 'output': out}
    return JSONResponse(content=json_response)