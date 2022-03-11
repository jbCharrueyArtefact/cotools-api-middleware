from fastapi import APIRouter, Depends, Response, status
from app.dependencies import get_bq_client, get_essential_contact_client
from app.lib.utils.customRoute import CustomRoute

from app.models.essentialContacts import (
    EssentialContactList,
    EssentialContactListOut,
)

from app.lib.utils.secret import get_sa_info

from app import config
from app.lib.ressources.essentialContacts import (
    modify_essentialContacts,
)

subrouter = APIRouter(route_class=CustomRoute)


@subrouter.get(
    "/",
    response_model=EssentialContactListOut,
    status_code=200,
)
def get_essential_contacts(
    project_id: str,
    response: Response,
    essentialContactsClient=Depends(get_essential_contact_client),
):
    try:
        a = essentialContactsClient.get_essentialContacts(project_id)
        return a
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return EssentialContactListOut(**{})


@subrouter.patch("/", status_code=200)
def modify_essential_contacts(
    project_id: str,
    data: EssentialContactList,
    response: Response,
    bqclient=Depends(get_bq_client),
    essentialContactsClient=Depends(get_essential_contact_client),
):

    current_table_id = config.ESSENTIAL_CONTACTS_CURRENT_TABLE
    try:
        modify_essentialContacts(
            project_id=project_id,
            essConClient=essentialContactsClient,
            data=data,
            db_client=bqclient,
            current_table_id=current_table_id,
        )
        return {"message": "success"}
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "failed"}
