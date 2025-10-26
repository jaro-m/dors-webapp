from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_current_active_user, get_current_user
from ..models import (
    UserBase,
)


router = APIRouter(prefix="")


@router.get("/users/me", response_model=UserBase)
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user


@router.get("/items/", summary="Reads items for the current user")
async def read_own_items(
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
