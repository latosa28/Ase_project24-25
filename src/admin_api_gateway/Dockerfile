FROM python:3.14.0a1-slim

WORKDIR /app

COPY admin_api_gateway/requirements.txt .
RUN pip install -r requirements.txt

COPY admin_api_gateway/app/ .
COPY utils/src .

EXPOSE 5010

CMD flask run --host=0.0.0.0 --port=5010 --cert=/run/secrets/admin_api_gateway_cert --key=/run/secrets/admin_api_gateway_key