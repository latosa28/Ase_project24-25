FROM python:3.14.0a1-slim

WORKDIR /app

COPY payment/requirements.txt .
RUN pip install -r requirements.txt

COPY payment/app .
COPY utils/src .

EXPOSE 5007

CMD flask run --host=0.0.0.0 --port=5007 --cert=/run/secrets/payment_cert --key=/run/secrets/payment_key



