from google.oauth2 import service_account
from googleapiclient import discovery
from app.lib.ressources.models import Label_map, ProjectDetails
from app.lib.utils import project


def create_project_orange(request: ProjectDetails, credentials):

    name = project.name(request)
    parent = f"folders/{request.parent_folder_id}"
    labels1 = request.label_map.dict(by_alias=True)
    labels2 = request.dict(
        by_alias=True,
        exclude={
            "demandeur",
            "workload_details",
            "parent_folder_id",
            "label_map",
        },
    )
    labels = labels1 | labels2

    return _create_project(
        name=name, parent=parent, labels=labels, credentials=credentials
    )


def _create_project(name, parent, labels, credentials):
    print(labels)
    client = discovery.build(
        "cloudresourcemanager", "v3", credentials=credentials
    )

    body = {"project_id": name, "parent": parent, "labels": labels}
    operation = client.projects().create(body=body).execute()
    return operation
