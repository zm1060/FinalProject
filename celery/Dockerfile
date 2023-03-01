FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY celery_task/ .

CMD ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
