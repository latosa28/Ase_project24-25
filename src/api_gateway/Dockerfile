FROM python:3.12-slim

WORKDIR /service

COPY api_gateway/requirements.txt .
RUN pip install -r requirements.txt

COPY api_gateway/app/ .
COPY utils/src .

EXPOSE 5000

CMD flask run --host=0.0.0.0 --port=5000 --cert=/run/secrets/api_gateway_cert --key=/run/secrets/api_gateway_key