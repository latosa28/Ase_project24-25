FROM python:3.12-slim

WORKDIR /service

COPY account/requirements.txt .
RUN pip install -r requirements.txt

COPY account/app .
COPY utils/src .

EXPOSE 5003

CMD flask run --host=0.0.0.0 --port=5003 --cert=/run/secrets/account_cert --key=/run/secrets/account_key