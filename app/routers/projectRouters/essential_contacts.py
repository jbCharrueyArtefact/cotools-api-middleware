from fastapi import HTTPException
from fastapi import APIRouter, Depends, Response
from app.dependencies import get_bq_client, get_essential_contact_client
from app.lib.utils.customRoute import CustomRoute

from app.models.essentialContacts import (
    EssentialContactList,
    EssentialContactListOut,
)
from app.lib.utils.custom_error_handling import (
    CustomEssentialContactException,
)

from app import config
from app.lib.ressources.essentialContacts import (
    modify_essential_contacts as modify_contact,
)

subrouter = APIRouter(route_class=CustomRoute)


@subrouter.get("/", response_model=EssentialContactListOut, status_code=200)
def get_essential_contacts(
    project_id: str,
    response: Response,
    essentialContactsClient=Depends(get_essential_contact_client),
):
    try:
        return essentialContactsClient.get_essential_contacts_client(
            project_id
        )
    except CustomEssentialContactException as e:
        response.status_code = e.status_code
        raise HTTPException(status_code=e.status_code, detail=e.message)


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
        modify_contact(
            project_id=project_id,
            essConClient=essentialContactsClient,
            data=data,
            db_client=bqclient,
            current_table_id=current_table_id,
        )
        return {"message": "success"}
    except CustomEssentialContactException as e:
        response.status_code = e.status_code
        raise HTTPException(status_code=e.status_code, detail=e.message)
