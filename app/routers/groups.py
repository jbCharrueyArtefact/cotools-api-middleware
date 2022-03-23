from fastapi import APIRouter, Query
from app.lib.utils.customRoute import CustomRoute
from app.lib.ressources import groups
from app.models.groups import GroupDetails, GroupDetailsFromUsers
import json
import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account
from app.lib.utils.secret import get_sa_info_from_shared_data_vault, get_sa_old
from app.clients.bigqueryClient import BigQueryWrapper
from app import config
from typing import List

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


@router.get("/list_groups")
def list_groups():
    credentials = get_sa_info_from_shared_data_vault("google_groups_assets")
    response = groups.list_groups(credentials)
    return response


# example: http://127.0.0.1:8000/groups/group_members?group_list=cloud.sandbox@orange.com&group_list=dfy-dlice@orange.com
@router.get("/group_members")
async def get_group_members(group_list: List[str] = Query(None)):
    credentials_groups = get_sa_info_from_shared_data_vault(
        "google_groups_assets"
    )
    group_members = groups.get_details_groups(group_list, credentials_groups)
    return group_members


# remarque: très long ~2m30s -> à lire depuis BigQuery si besoin
@router.get("/members")
async def get_all_groups_members():
    credentials_groups = get_sa_info_from_shared_data_vault(
        "google_groups_assets"
    )
    allgroups = groups.list_groups(credentials_groups)
    group_members = groups.get_details_groups(allgroups, credentials_groups)
    return group_members


# example: http://127.0.0.1:8000/groups/from_users?user=mariem.mtibaa@orange.com
@router.get("/from_users")
async def get_groups_from_users(user: str):
    credentials_groups = get_sa_info_from_shared_data_vault(
        "google_groups_assets"
    )
    users = [user]
    return groups.get_groups_from_users(users, credentials_groups)
