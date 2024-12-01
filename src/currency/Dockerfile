FROM python:3.14.0a1-slim

WORKDIR /service

COPY currency/requirements.txt .
RUN pip install -r requirements.txt

COPY currency/app .
COPY utils/src .

EXPOSE 5005

CMD flask run --host=0.0.0.0 --port=5005 --cert=/run/secrets/currency_cert --key=/run/secrets/currency_key
