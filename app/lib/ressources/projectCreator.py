from googleapiclient import discovery
from app.models.projects import (
    ProjectDetails,
)
from app.lib.utils.project import create_name


def create_project_orange(request: ProjectDetails, client):

    name = create_name(request)
    parent = f"folders/{request.parent_folder_id}"
    labels1 = request.label_map.dict(
        by_alias=True, exclude={"project_owner", "accountable"}
    )
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
        name=name, parent=parent, labels=labels, client=client
    )


def _create_project(name, parent, labels, client):

    return client.create_project(name, parent, labels), name
