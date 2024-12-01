FROM python:3.12-slim

WORKDIR /service

COPY market/requirements.txt .
RUN pip install -r requirements.txt

COPY market/app .
COPY utils/src .

EXPOSE 5004

CMD flask run --host=0.0.0.0 --port=5004 --cert=/run/secrets/market_cert --key=/run/secrets/market_key
