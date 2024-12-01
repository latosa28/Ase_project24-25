FROM python:3.14.0a1-slim

WORKDIR /service

COPY admin_account/requirements.txt .
RUN pip install -r requirements.txt

COPY admin_account/app .
COPY utils/src .

EXPOSE 5006

CMD flask run --host=0.0.0.0 --port=5006 --cert=/run/secrets/admin_account_cert --key=/run/secrets/admin_account_key