import time
from app.lib.ressources.models import (
    EssentialContactList,
    ProjectDetails,
    GroupDetails,
    SetIamDetails,
)

from fastapi import FastAPI
import json
import subprocess
from app.lib.ressources.projectCreator import create_project_orange
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient import discovery
from app.lib.utils.secret import get_secrets, get_sa_info

from app import config
from app.lib.ressources.essentialContacts import (
    modify_essentialContacts,
    create_essential_contact_from_list_email,
    wait_essential_contacts_disponibility,
)
from app.lib.utils.essentialContactsClient import EssentialContactsClient
from app.lib.utils.bigqueryWrapper import BigQueryWrapper


app = FastAPI()


@app.post("/create_project")
def create_project(request: ProjectDetails):
    sa_info = get_sa_info(config.SECRETS["create_project"])
    credentials = service_account.Credentials.from_service_account_info(
        sa_info
    )
    response, name = create_project_orange(
        request=request, credentials=credentials
    )

    current_table_id = config.ESSENTIAL_CONTACTS_CURRENT_TABLE
    info = get_sa_info(config.SECRETS["essential_contacts"])
    a = get_sa_info(config.SECRETS["biqquery"])
    client = EssentialContactsClient(info)
    bqclient = BigQueryWrapper(a)

    wait_essential_contacts_disponibility(client, name)

    create_essential_contact_from_list_email(
        project_id=name,
        list_email=request.label_map.accountable,
        notificationCategorySubscriptions="TECHNICAL",
        essConClient=client,
        db_client=bqclient,
        table_id=current_table_id,
    )
    create_essential_contact_from_list_email(
        name,
        request.label_map.project_owner,
        "ALL",
        client,
        bqclient,
        current_table_id,
    )

    return response


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


@app.get("/get_project_iam_rights/{project_id}")
def get_project_iam_rights(project_id: str):
    credentials = service_account.Credentials.from_service_account_info(
        get_secrets(engine="sa", secret="read_iam"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )

    response = (
        service.projects()
        .getIamPolicy(resource=project_id, body={})
        .execute(num_retries=5)
    )
    return response


@app.post("/set_project_iam_rights")
def set_project_iam_rights(request: SetIamDetails):
    credentials = service_account.Credentials.from_service_account_info(
        get_secrets(engine="sa", secret="read_iam"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = discovery.build(
        "cloudresourcemanager", "v1", credentials=credentials
    )

    try:
        for key in config.KEYS_TO_DELETE:
            request.details.pop(key, None)

        response = (
            service.projects()
            .setIamPolicy(resource=request.project_id, body=request.details)
            .execute(num_retries=5)
        )
        return {"code": 200, "response": str(response)}
    except Exception as err_msg:
        return {"code": 400, "response": str(err_msg)}


@app.get("/set_cache")
def set_cache():
    get_secrets(engine="sa", secret="read_iam")
    get_secrets(engine="sa", secret="create_project")
    get_secrets(engine="sa", secret="essential_contacts")
    get_secrets(engine="sa", secret="bigquery_cotools_dev")
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
@app.get("/projects/{project_id}/essential_contacts")
def get_essential_contacts(project_id: str):
    info = get_sa_info(config.SECRETS["essential_contacts"])
    client = EssentialContactsClient(info)
    return client.get_essentialContacts(project_id)


@app.patch("/projects/{project_id}/essential_contacts")
def modify_essential_contacts(project_id: str, data: EssentialContactList):
    current_table_id = config.ESSENTIAL_CONTACTS_CURRENT_TABLE
    info = get_sa_info(config.SECRETS["essential_contacts"])
    a = get_sa_info(config.SECRETS["biqquery"])
    client = EssentialContactsClient(info)
    bqclient = BigQueryWrapper(a)
    return modify_essentialContacts(
        project_id=project_id,
        essConClient=client,
        data=data,
        db_client=bqclient,
        current_table_id=current_table_id,
    )


@app.get("/get_roles_recommandation")
def get_recommandation():
    with open("app/config/recoRoles.json") as roles:
        return json.load(roles)


@app.get("/all_roles")
def get_roles():
    with open("app/config/allRoles.json") as roles:
        return json.load(roles)


############ Test purpose: simulate listening webhook ############
@app.post("/test_create_project")
async def test_create_project(request: ProjectDetails):
    print("FINAL SPRINT")
    print(request.json())
    return {"data": f'blog is created as {request.label_map["hello"]}'}
