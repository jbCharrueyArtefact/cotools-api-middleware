from fastapi import APIRouter
from app.lib.utils.customRoute import CustomRoute

from app.models.groups import GroupDetails
import json
import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account
from app.lib.utils.secret import get_sa_old
from app import config


router = APIRouter(prefix="/groups", tags=["group"], route_class=CustomRoute)


@router.post("/")
def create_group(request: GroupDetails):

    sa_info = get_sa_old(sa="create_group")
    creds = service_account.IDTokenCredentials.from_service_account_info(
        sa_info, target_audience=config.GROUP_CREATION_CLIENT_ID
    )
    creds.refresh(GoogleRequest())
    token = creds.token

    data = request.dict()

    manager = data.pop("manager")
    params = {"my_manager": manager}
    header = {
        "Authorization": "Bearer {}".format(token),
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    resp = requests.request(
        "PUT",
        url=f"{config.URL_GROUP_CREATION}/createGroup/test",
        headers=header,
        params=params,
        data=json.dumps(data),
    )
    return resp.json()
