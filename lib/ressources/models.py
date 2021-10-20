from pydantic import BaseModel


class ProjectDetails(BaseModel):
    demandeur: str
    country: str
    basicat: str
    workload_details: str
    env: str
    parent_folder_id: int
    label_project_confidentiality: str
    label_personal_data: str
    unicity_id: int
    label_map: dict


class OwnerDetails(BaseModel):
    email: str


class GroupDetails(BaseModel):
    name: str
    description: str
    mail: str
