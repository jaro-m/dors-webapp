from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_current_active_user
from ..models import (
    # UserBase,
    ReporterBase,
)


router = APIRouter(prefix="")



@router.get(
    "/test/",
    summary="Just a check, during the development, if the authorization is working"
)
async def read_own_items(
    current_user: Annotated[ReporterBase, Depends(get_current_active_user)]
):
    return [{"result": "OK", "current_user": current_user.username}]


@router.get("/healthcheck", response_model=dict, summary="Healthcheck")
async def healthy():

    return {"status": "OK"}
