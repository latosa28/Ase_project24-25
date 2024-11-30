FROM python:3.12-slim

WORKDIR /service

COPY collection/requirements.txt .
RUN pip install -r requirements.txt

COPY collection/app .
COPY utils/src .

EXPOSE 5002

CMD flask run --host=0.0.0.0 --port=5002 --cert=/run/secrets/collection_cert --key=/run/secrets/collection_key