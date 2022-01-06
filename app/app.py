from app.lib.ressources.models import (
    EssentialContactList,
    EssentialContactListOut,
    EssentialContactOut,
    Policy,
    ProjectDetails,
    GroupDetails,
    SetIamDetails,
    HistoricalIamDetails,
)

from fastapi import FastAPI, Response, status
import json
from app.lib.ressources.projectCreator import create_project_orange
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient import discovery
from app.lib.utils.iam import get_interval_historical_data
from app.lib.utils.secret import get_secrets, get_sa_info
from app.lib.utils import basicatClient
from app import config
from app.lib.ressources.essentialContacts import (
    modify_essentialContacts,
    create_essential_contact_from_list_email,
    wait_essential_contacts_disponibility,
)
from app.lib.utils.essentialContactsClient import EssentialContactsClient
from app.lib.utils.bigqueryWrapper import BigQueryWrapper


app = FastAPI()


@app.post("/create_project", status_code=200)
def create_project(request: ProjectDetails, response: Response):
    sa_info = get_sa_info(config.SECRETS["create_project"])
    iosw_secret = get_secrets(engine="co-tools-secrets", secret="iosw")
    current_table_id = config.ESSENTIAL_CONTACTS_CURRENT_TABLE
    info = get_sa_info(config.SECRETS["essential_contacts"])
    a = get_sa_info(config.SECRETS["biqquery"])
    credentials = service_account.Credentials.from_service_account_info(
        sa_info
    )

    response_basicat = basicatClient.get_basicat_info(
        iosw_secret["username"], iosw_secret["password"], request.basicat
    )
    if response_basicat.status_code != 200:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": f"No application found for basicat :{request.basicat}",
        }

    try:
        response_create, name = create_project_orange(
            request=request, credentials=credentials
        )
    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "project could not be created"}

    client = EssentialContactsClient(info)
    bqclient = BigQueryWrapper(a)

    wait_essential_contacts_disponibility(client, name)

    try:
        mappings = [
            {"emails": request.label_map.accountable, "category": "TECHNICAL"},
            {"emails": request.label_map.project_owner, "category": "ALL"},
        ]

        create_essential_contact_from_list_email(
            project_id=name,
            mappings=mappings,
            essConClient=client,
            db_client=bqclient,
            table_id=current_table_id,
        )

    except Exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": "project created but ownership and accountability could not be set"
        }

    return {"message": "project created"}


@app.post("/create_group")
def create_group(request: GroupDetails):

    sa_info = get_secrets(engine="sa", secret="create_group")
    creds = service_account.IDTokenCredentials.from_service_account_info(
        sa_info, target_audience=config.GROUP_CREATION_CLIENT_ID
    )
    creds.refresh(Request())
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


@app.get("/contacts/{contact_id}/owner")
async def get_projects(contact_id: str):
    a = get_secrets(engine="sa", secret="bigquery_cotools_dev")
    bqclient = BigQueryWrapper(a)
    current_view = config.ESSENTIAL_CONTACTS_CURRENT_VIEW
    query = (
        f"select project from `{current_view}`" f" where email ='{contact_id}'"
    )
    results = bqclient.query_data(query=query)
    return [{"project": result.project} for result in results]


@app.get("/get_project_iam_rights/{project_id}", response_model=Policy)
def get_project_iam_rights(project_id: str, response: Response):
    credentials = service_account.Credentials.from_service_account_info(
        get_secrets(engine="sa", secret="read_iam"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )

    try:
        return_value = (
            service.projects()
            .getIamPolicy(resource=project_id, body={})
            .execute(num_retries=5)
        )
        return return_value
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}


@app.post("/set_project_iam_rights")
def set_project_iam_rights(request: SetIamDetails, response: Response):
    credentials = service_account.Credentials.from_service_account_info(
        get_secrets(engine="sa", secret="read_iam"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )

    try:

        body = {"policy": request.details.dict()}
        response = (
            service.projects()
            .setIamPolicy(resource=request.project_id, body=body)
            .execute(num_retries=5)
        )
        return {"message": "success"}
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "failed"}


@app.get("/set_cache")
def set_cache():
    get_secrets(engine="sa", secret="create_project")
    get_secrets(engine="sa", secret="essential_contacts")
    get_secrets(engine="sa", secret="bigquery_cotools_dev")


@app.get("/get_folder_hierarchy")
def get_folder_hierarchy():
    bearer = get_secrets(engine="co-tools-secrets", secret="api_hierarchy")[
        "token"
    ]
    r = requests.get(
        url=config.HIERARCHY_URL,
        headers={"Authorization": f"Bearer {bearer}"},
        verify=False,
    )
    return r.json()


# TODO: create optional parameters to get information for 1 contact after slash. might need to switch to raw api
@app.get(
    "/projects/{project_id}/essential_contacts",
    response_model=EssentialContactListOut,
    status_code=200,
)
def get_essential_contacts(project_id: str, response: Response):

    info = get_sa_info(config.SECRETS["essential_contacts"])
    client = EssentialContactsClient(info)
    try:
        a = client.get_essentialContacts(project_id)
        return a
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return EssentialContactListOut(**{})


@app.patch("/projects/{project_id}/essential_contacts", status_code=200)
def modify_essential_contacts(
    project_id: str, data: EssentialContactList, response: Response
):

    current_table_id = config.ESSENTIAL_CONTACTS_CURRENT_TABLE
    info = get_sa_info(config.SECRETS["essential_contacts"])
    a = get_sa_info(config.SECRETS["biqquery"])
    client = EssentialContactsClient(info)
    bqclient = BigQueryWrapper(a)
    try:
        modify_essentialContacts(
            project_id=project_id,
            essConClient=client,
            data=data,
            db_client=bqclient,
            current_table_id=current_table_id,
        )
        return {"message": "success"}
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "failed"}


@app.get("/get_roles_recommandation")
def get_recommandation():
    with open("app/config/recoRoles.json") as roles:
        return json.load(roles)


@app.get("/all_roles")
def get_roles():
    with open("app/config/allRoles.json") as roles:
        return json.load(roles)


@app.get("/projects/{project_id}/iam/list_history")
def list_iam_history(project_id, interval: HistoricalIamDetails):
    service_account = get_secrets(engine="sa", secret="bigquery_cotools_dev")
    bq_client = BigQueryWrapper(service_account)
    time_interval = get_interval_historical_data(interval)
    query_root = f"SELECT * FROM `{config.REFERENCE_TABLE_IAM_HISTORY}` where project_name = '{str(project_id)}'"
    query = (
        f"{query_root} AND {time_interval}" if time_interval else query_root
    )
    result = bq_client.query_data(query)
    return [dict(row) for row in result]


@app.get("/basicat/{basicat}")
def get_basicat_info(basicat: str):
    secret = get_secrets(engine="co-tools-secrets", secret="iosw")
    return basicatClient.get_basicat_info(
        secret["username"], secret["password"], basicat
    ).json()
