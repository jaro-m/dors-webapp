from pydantic import BaseModel, EmailStr
from typing import Annotated

from fastapi import Depends, FastAPI


app = FastAPI(redirect_slashes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None


async def get_current_user():
    return User(**{
        "username": "mikewazowski",
        "password": "???"
    })


@app.get("/things/", summary="Reads items for the current user")
async def read_own_things(current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
