FROM python:3.10
ENV PYTHONPATH=/backend/app

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt
RUN pip install -U pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade -r /backend/requirements.txt
# Copy the ./app directory inside the /backend directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
# So, it's important to put this near the end of the Dockerfile, to optimize the container image build times.
COPY ./app /backend/app

# This command will be run from the current working directory, the same /backend directory you set above with WORKDIR /backend.
# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# Start the Celery worker
CMD ["celery", "-A", "celery_task.tasks", "worker","-P","threads" ,"--loglevel=info", "-Q", "celery"]

EXPOSE 8080

