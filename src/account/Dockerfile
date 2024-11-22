FROM python:3.12-slim

WORKDIR /service

COPY account/requirements.txt .
RUN pip install -r requirements.txt

COPY account/app .
COPY utils/ ./utils

EXPOSE 5003

CMD flask --app app run --host=0.0.0.0 --port=5003