from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from .constants import ALGORITHM, SECRET_KEY
from .db import engine
from .helpers import logger
from .models import (
    Reporter,
    ReporterBase,
    TokenData,
    # User,
    # UserBase,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(username: str):
    with Session(engine) as session:
        statement = select(Reporter).where(Reporter.username == username)
        user = session.exec(statement).first()

        if not user:
            logger.error("Incorrect credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.username == username:
            return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception from None

    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return Reporter(**user.dict())


async def get_current_active_user(
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

