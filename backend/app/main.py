from fastapi import BackgroundTasks, FastAPI
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from crawler.ChinaNews import run_china_news

app = FastAPI()


@app.post("/run-spider/ChinaNews")
async def crawler_china_new():
    out, err = run_china_news.run_scrapy_spider()
    if err:
        response = {'status': 'error', 'message': err}
    else:
        response = {'status': 'success', 'output': out}
    return response