from pydantic.main import BaseModel
from lib.ressources.models import ProjectDetails, OwnerDetails, GroupDetails
from fastapi import FastAPI
import json
import config
import subprocess
from lib.ressources.projectCreator import ProjectCreator
import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token


app = FastAPI()

class Test3(BaseModel):
    ok:str

# {"demandeur": "demandeur", "country": "ofr", "basicat": "qwerty", "workload_details": "workload_details", "env": "dev", "parent_folder_id": 12345, "label_project_confidentiality": "c1","label_personal_data": "g0", "unicity_id": 1, "label_map": {"aa": "bb", "hello": 1}}
@app.post("/create_project")
async def create_project(request: ProjectDetails):
    return ProjectCreator.create_project(
        config.URL_OF_REMOTE_GIT, config.PATH_OF_GIT_REPO, request
    )


@app.post("/create_group")
async def create_group(request: GroupDetails):
    open_id_connect_token = id_token.fetch_id_token(
        Request(), config.GROUP_CREATION_CLIENT_ID
    )
    import pdb; pdb.set_trace()
    data = request.dict()
    
    manager = data.pop("manager")
    params = {"my_manager":manager}
    header = {
        "Authorization": "Bearer {}".format(open_id_connect_token),
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    resp = requests.request('PUT',
        url = f'{config.URL_GROUP_CREATION}/createGroup/test',
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


############ Test purpose: simulate listening webhook ############
@app.post("/test_create_project")
async def test_create_project(request: ProjectDetails):
    print("FINAL SPRINT")
    print(request.json())
    return {"data": f'blog is created as {request.label_map["hello"]}'}
