from lib.ressources.models import ProjectDetails, OwnerDetails
from fastapi import FastAPI
import json
import config
import subprocess
from lib.ressources.projectCreator import ProjectCreator


app = FastAPI()

# {"demandeur": "demandeur", "country": "ofr", "basicat": "qwerty", "workload_details": "workload_details", "env": "dev", "parent_folder_id": 12345, "label_project_confidentiality": "c1","label_personal_data": "g0", "unicity_id": 1, "label_map": {"aa": "bb", "hello": 1}}
@app.post("/create_project")
async def create_project(request: ProjectDetails):
    return ProjectCreator.create_project(
        config.URL_OF_REMOTE_GIT, config.PATH_OF_GIT_REPO, request
    )


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
