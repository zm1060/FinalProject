FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "spacy", "download", "en_core_web_sm"]
