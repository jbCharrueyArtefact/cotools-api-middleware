from fastapi import APIRouter, Depends, Response, status
from app.dependencies import (
    get_billing_client,
    get_bq_client,
    get_essential_contact_client,
    get_project_client,
    get_iam_client,
)
from app.lib.utils.customRoute import CustomRoute
from app.lib.utils.secret import get_secrets
from app.models.projects import ProjectDetails
from app.lib.ressources.projectCreator import create_project_orange
from app import config
from app.lib.ressources.essentialContacts import (
    create_essential_contact_from_list_email,
    wait_essential_contacts_disponibility,
)
from app.roles.ProjectCreationRoles import ProjectCreationRoles
from app.lib.ressources.projectCreator import set_iam_from_requests
from app.clients.basicatClient import get_basicat_info

from app.lib.utils.custom_error_handling import CustomBaseException

subrouter = APIRouter(
    route_class=CustomRoute,
    dependencies=[
        Depends(get_bq_client),
        Depends(get_essential_contact_client),
    ],
)


@subrouter.get("/")
def get_projects(contact_id: str, bqclient=Depends(get_bq_client)):
    current_view = config.ESSENTIAL_CONTACTS_CURRENT_VIEW
    query = (
        f"select project from `{current_view}`" f" where email ='{contact_id}'"
    )
    results = bqclient.query_data(query=query)
    return [{"project": result.project} for result in results]


@subrouter.post("/", status_code=200)
def create_project(
    request: ProjectDetails,
    response: Response,
    bqclient=Depends(get_bq_client),
    essential_contacts_client=Depends(get_essential_contact_client),
    billing_client=Depends(get_billing_client),
    project_client=Depends(get_project_client),
    iam_client=Depends(get_iam_client),
):
    iosw_secret = get_secrets(secret="iosw")
    current_table_id = config.ESSENTIAL_CONTACTS_CURRENT_TABLE

    response_basicat = get_basicat_info(
        iosw_secret["username"], iosw_secret["password"], request.basicat
    )
    if response_basicat.status_code != 200:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": f"No application found for basicat :{request.basicat}",
        }
    try:
        response_create, name = create_project_orange(
            request=request, client=project_client
        )

        wait_essential_contacts_disponibility(essential_contacts_client, name)

        if config.ENV == "PRD":
            billing_client.set_billing_account(name, config.BILLING_ID)

        mappings = [
            {"emails": request.label_map.accountable, "category": "TECHNICAL"},
            {
                "emails": request.label_map.project_owner
                + [request.demandeur],
                "category": "ALL",
            },
        ]

        create_essential_contact_from_list_email(
            project_id=name,
            mappings=mappings,
            essConClient=essential_contacts_client,
            db_client=bqclient,
            table_id=current_table_id,
        )
        list_roles = [
            ProjectCreationRoles.projectIamAdmin,
            ProjectCreationRoles.serviceUsageAdmin,
        ]

        set_iam_from_requests(iam_client, request, name, list_roles)

    except CustomBaseException as e:
        response.status_code = e.status_code
        return {"message": e.message}
    except Exception as e:
        response.status_code = 500
        return {"message": str(e)}

    return {"message": "project created"}
