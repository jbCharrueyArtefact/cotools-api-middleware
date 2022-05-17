from fastapi import APIRouter, Depends, HTTPException
from app.clients.groupClient import GroupClient
from app.dependencies import (
    get_bq_client,
    get_bq_client_shared_data,
    get_data_group_client,
    get_entities_client,
)
from app.lib.utils.customRoute import CustomRoute
from app.lib.utils.custom_error_handling import CustomBaseException
from app.models.dataGroups import DataGroupDetails

subrouter = APIRouter(route_class=CustomRoute)


@subrouter.post("/")
def create_data_groups(
    project_id,
    request: DataGroupDetails,
    data_group_client: GroupClient = Depends(get_data_group_client),
    entities_client=Depends(get_entities_client),
):
    try:
        name = f"{request.workload}-{request.env}"
        description = request.description
        gestionnaire = request.gestionnaire
        is_bank = request.is_bank
        restriction_entities = request.restriction_entities
        id_entities = entities_client.get_list_id_entities(
            restriction_entities
        )

        data_group_client.create_data_group(
            name, description, id_entities, is_bank, project_id, gestionnaire
        )

        return {"message": "group created"}
    except CustomBaseException as e:
        raise HTTPException(e.status_code, detail=e.message)
