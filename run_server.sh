#!/usr/bin/env sh

./ve/bin/uvicorn src.main:app --reload --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem