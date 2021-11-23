from app.lib.ressources.models import (
    ProjectDetails,
    OwnerDetails,
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
from app.lib.utils.secret import get_secrets

from app import config

app = FastAPI()


@app.post("/create_project")
def create_project(request: ProjectDetails):
    sa_info = get_secrets(engine="sa", secret="create_project")
    credentials = service_account.Credentials.from_service_account_info(
        sa_info
    )
    return create_project_orange(request=request, credentials=credentials)


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


@app.post("/get_projects")
async def get_projects(request: OwnerDetails):
    email = request.dict()["email"].replace(".", "_dot_").replace("@", "_at_")
    projects = subprocess.check_output(
        [
            "gcloud",
            "projects",
            "list",
            "--filter",
            f"labels.cost-center={email}",
            "--format",
            "json",
        ],
        encoding="utf-8",
    )
    return [project["projectId"] for project in json.loads(projects)]


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
