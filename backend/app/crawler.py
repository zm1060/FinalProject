from celery import Celery

# Initialize celery
celery_app = Celery("crawler", backend='redis://localhost', broker="pyamqp://guest@localhost//")

# Define task function
@celery_app.task
def crawl(url):
    # Perform crawling logic here
    return {"url": url, "data": {"title": "Example Title", "body": "Example Body"}}
