from os import getenv
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.exc import ArgumentError

DB_URL = getenv("DB_URL")

try:
    engine = create_engine(DB_URL, echo=True)
except ArgumentError as err:
    raise HTTPException(
        status_code=500,
        detail=f"create_engine(DB_URL): {err}" if err else "DB_URL env var is not set(?)",
    ) from None


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
