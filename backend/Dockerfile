FROM python:3.10
ENV PYTHONPATH=/backend/app
ENV PYTHONPATH=/backend/jdspider
ENV PYTHONPATH=/backend/weibospider
ENV PYTHONPATH=/backend/pre_process

WORKDIR /backend

#RUN apt-get update && apt-get install -y \
#    default-jre \
#    default-jdk \
#    git \
#    build-essential \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*



COPY ./requirements.txt /backend/requirements.txt
# Copy the SimHei font file to the container
COPY SimHei.ttf /usr/share/fonts/truetype/
# Update the font cache
RUN fc-cache -f -v
RUN pip install -U pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade -r /backend/requirements.txt

# Copy the ./app directory inside the /backend directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.
# So, it's important to put this near the end of the Dockerfile, to optimize the container image build times.
COPY ./app /backend/app
COPY ./jdspider /backend/jdspider
COPY ./weibospider /backend/weibospider
COPY ./pre_process /backend/pre_process
# This command will be run from the current working directory, the same /backend directory you set above with WORKDIR /backend.
# Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]


EXPOSE 8080

