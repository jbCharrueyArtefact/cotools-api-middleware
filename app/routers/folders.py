from fastapi import APIRouter


import requests

from app import config
from app.lib.utils.customRoute import CustomRoute
from app.lib.utils.secret import get_secrets

router = APIRouter(
    prefix="/folders", tags=["folders"], route_class=CustomRoute
)


@router.get("/")
def get_folder_hierarchy():
    bearer = get_secrets(secret="api_hierarchy")["token"]
    r = requests.get(
        url=config.HIERARCHY_URL,
        headers={"Authorization": f"Bearer {bearer}"},
        verify=False,
    )
    return r.json()
