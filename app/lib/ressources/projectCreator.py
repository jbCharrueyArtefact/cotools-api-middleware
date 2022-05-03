from fastapi import HTTPException

from app.models.projects import ProjectDetails
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


def set_iam_from_requests(iam_client, request: ProjectDetails, name, roles):
    roles_list = []
    for role in roles:
        roles_list.append(
            {
                "members": [
                    f"user:{request.demandeur}",
                    "user:louis.rousselotdesaintceran.ext@orange.com",
                ],
                "role": role,
            }
        )
    policy = {"bindings": roles_list}
    iam_client.set_project_iam_rights(policy, name)


def _create_project(name, parent, labels, client):

    return client.create_project(name, parent, labels), name
