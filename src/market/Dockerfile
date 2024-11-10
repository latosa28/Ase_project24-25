FROM python:3.12-slim

WORKDIR /service

COPY requirements.txt .
COPY app/ .

RUN pip install -r requirements.txt

EXPOSE 5004

CMD flask run --host=0.0.0.0 --port=5004