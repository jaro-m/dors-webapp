from os import getenv

from fastapi import FastAPI

from .helpers import logger
from .routers import api, auth, default


SECRET_KEY = getenv("SECRET_KEY", "somethingR43IIyS1lley")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

logger = logger.getChild(__name__)

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
