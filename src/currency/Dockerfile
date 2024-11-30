FROM python:3.12-slim

WORKDIR /service

COPY currency/requirements.txt .
RUN pip install -r requirements.txt

COPY currency/app .
COPY utils/src .


EXPOSE 5005

CMD flask run --host=0.0.0.0 --port=5005