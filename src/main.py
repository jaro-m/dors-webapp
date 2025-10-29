
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .helpers import logger
from .routers import api, auth, default

logger = logger.getChild(__name__)

description = """
This is a simple API, created as a test.

The purpose was to find out how much I can get done in a short period of time.

The aim was to build a fully functional production-ready webapp using the best practices.

As the time was really limited for me, and even the technologies I chose to build the app
were not used by me for some time, I couldn't finish, what, at first, seemed to be
a simple task.
"""

# These values are only for development
# Using the app in production,
# these values could be provided in env vars and read from them
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

app = FastAPI(
    redirect_slashes=True,
    openapi_tags=tags_metadata,
    title="Disease Outbreak Reporting System API",
    description=description,
    version="0.1",
    contact={
        "name": "Jaroslaw Michalski",
        "url": "https://github.com/jaro-m",
        "email": "jaro.m@hotmail.co.uk",
    },
    license_info= {
        "name": "MIT License",
    },
)
app.include_router(api.router)
app.include_router(auth.router)
app.include_router(default.router)

app.add_middleware(
    CORSMiddleware,
    # TODO: Fix this security issue
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def generic_api_exception_handler(request: Request, ex: HTTPException):
    """
    Generic API exception handler.
    """
    return JSONResponse(
        status_code=ex.status_code,
        content=ex.detail
    )
