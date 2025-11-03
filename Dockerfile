FROM python:3.13

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
COPY ./certs /code/certs
# this is only for development on a local machine
COPY ./database.db /code


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/code/certs/key.pem", "--ssl-certfile", "/code/certs/cert.pem", "--workers", "4"]