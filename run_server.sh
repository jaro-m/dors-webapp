#!/usr/bin/env sh

. ./.env
./ve/bin/uvicorn src.main:app --reload --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem