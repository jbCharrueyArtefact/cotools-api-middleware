from fastapi import APIRouter, Depends, HTTPException
from app.clients.groupClient import GroupClient
from app.dependencies import get_group_client
from app.lib.utils.customRoute import CustomRoute
from app.lib.ressources import groups
from app.lib.utils.custom_error_handling import CustomGroupClientException
from app.models.groups import GroupDetails, GroupList, UsersGroup

router = APIRouter(prefix="/groups", tags=["group"], route_class=CustomRoute)


@router.post("/")
def create_group(
    request: GroupDetails,
    group_client: GroupClient = Depends(get_group_client),
):

    manager = request.manager
    name = request.name
    description = request.description
    mail = request.mail
    return group_client.create_group(manager, name, description, mail)


@router.get("/")
def list_groups(
    members: UsersGroup = None,
    group_client: GroupClient = Depends(get_group_client),
):
    try:
        if members:
            return groups.list_groups(users=members.users, client=group_client)
        else:
            return groups.list_groups(group_client)
    except CustomGroupClientException as e:
        raise HTTPException(e.status_code, e.message)


@router.get("/members/")
def get_group_members(
    group_list: GroupList = None,
    group_client: GroupClient = Depends(get_group_client),
):
    try:
        return groups.get_details_groups(group_list.groups, group_client)
    except CustomGroupClientException as e:
        raise HTTPException(e.status_code, e.message)
