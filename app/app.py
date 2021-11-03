from pydantic.main import BaseModel
from app.lib.ressources.models import ProjectDetails, OwnerDetails, GroupDetails
from fastapi import FastAPI
import json
from app import config
import subprocess
from app.lib.ressources.projectCreator import ProjectCreator
import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from app.lib.utils.secret import Secret



app = FastAPI()

secret = Secret("/sa/secret.json")




# {"demandeur": "demandeur", "country": "ofr", "basicat": "qwerty", "workload_details": "workload_details", "env": "dev", "parent_folder_id": 12345, "label_project_confidentiality": "c1","label_personal_data": "g0", "unicity_id": 1, "label_map": {"aa": "bb", "hello": 1}}
@app.post("/create_project")
def create_project(request: ProjectDetails):
    return ProjectCreator.create_project(
        url_git_repo=config.URL_OF_REMOTE_GIT,
        path_local_git_repo=config.PATH_OF_GIT_REPO,
        username=secret.get_secret("username"),
        password=secret.get_secret("password"),
        request=request,
    )


@app.post("/create_group")
def create_group(request: GroupDetails):
    open_id_connect_token = id_token.fetch_id_token(
        Request(), config.GROUP_CREATION_CLIENT_ID
    )
    data = request.dict()

    manager = data.pop("manager")
    params = {"my_manager": manager}
    header = {
        "Authorization": "Bearer {}".format(open_id_connect_token),
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
    iam_rights = subprocess.check_output(
        ["gcloud", "projects", "get-iam-policy", project_id, "--format", "json"],
        encoding="utf-8",
    )
    return json.loads(iam_rights)


@app.get("/get_folder_hierarchy")
def get_folder_hierarchy():
    bearer = secret.get_secret("api_hierarchy")
    r = requests.get(
        url=config.HIERARCHY_URL, 
        headers={"Authorization": f"Bearer {bearer}"},
        verify=False
    )
    return r.json() 


############ Test purpose: simulate listening webhook ############
@app.post("/test_create_project")
async def test_create_project(request: ProjectDetails):
    print("FINAL SPRINT")
    print(request.json())
    return {"data": f'blog is created as {request.label_map["hello"]}'}
