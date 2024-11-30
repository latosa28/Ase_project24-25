FROM python:3.12-slim

WORKDIR /app

COPY auth/requirements.txt .
RUN pip install -r requirements.txt

COPY auth/app/ .
COPY utils/src .

EXPOSE 5011

CMD flask run --host=0.0.0.0 --port=5011 --cert=/run/secrets/auth_cert --key=/run/secrets/auth_key