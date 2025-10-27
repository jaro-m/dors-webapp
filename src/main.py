import ssl

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .helpers import logger
from .routers import api, auth, default

logger = logger.getChild(__name__)

origins = [
    "http://localhost",
    "http://localhost:3080",
    "http://localhost:8080",
]

# keep the tags in the defined order
tags_metadata = [
    {"name": "reporter"},
    {"name": "patient"},
    {"name": "disease"},
    {"name": "reports"},
]

app = FastAPI(redirect_slashes=True, openapi_tags=tags_metadata)
app.include_router(api.router)
app.include_router(auth.router)
app.include_router(default.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    '/home/jar0/ukhsa/test/DORS/certs/cert.pem',
    keyfile='/home/jar0/ukhsa/test/DORS/certs/key.pem',
)
