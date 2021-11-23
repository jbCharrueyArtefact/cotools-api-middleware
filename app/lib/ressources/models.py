import re
from typing import List

from pydantic import BaseModel, Field, root_validator, validator


class Label_map(BaseModel):
    cost_center: str = Field(alias="cost-center")
    accountable: List[str]
    project_owner: List[str] = Field(alias="project-owner")
    project_family: str = Field(alias="project-family")
    id_orange_carto: str = Field(alias="id-orange-carto")

    class Config:
        arbitrary_types_allowed = True
        anystr_lower = True
        max_anystr_length = 63

    @validator("*", each_item=True)
    def validate_format(cls, v):
        assert re.match(
            r"^[a-zA-Z0-9_-]+$", v
        ), "charactere should only use lower case letters, digits, _ or -"
        return v

    @validator("accountable", "project_owner", each_item=True, pre=True)
    def replace_dot_at_(cls, v):
        return v.replace("@", "_at_").replace(".", "_dot_")

    @validator("accountable", "project_owner")
    def good_number_of_person(cls, v):
        assert len(v) < 5, "too much accountables"
        return v

    @root_validator
    def parse_liste(cls, values):

        for key in ["project_owner", "accountable"]:
            n = 1
            for elem in values[key]:
                values[f"{key}{n}".replace("_", "-")] = elem
                n += 1
            del values[key]
        return values


class ProjectDetails(BaseModel):
    demandeur: str
    country: str
    basicat: str = Field(alias="project-internal-id")
    workload_details: str
    env: str = Field(alias="environment")
    parent_folder_id: int
    label_project_confidentiality: str = Field(alias="project-confidentiality")
    label_personal_data: str = Field(alias="personal-data")
    unicity_id: str
    label_map: Label_map

    class Config:
        arbitrary_types_allowed = True
        anystr_lower = True
        allow_population_by_field_name = True

    @validator(
        "country",
        "basicat",
        "workload_details",
        "env",
        "label_project_confidentiality",
        "label_personal_data",
        each_item=True,
    )
    def validate_format(cls, v):
        assert re.match(
            r"^[a-zA-Z0-9_-]+$", v
        ), "charactere should only use lower case letters, digits, _ or -"
        return v


class OwnerDetails(BaseModel):
    email: str


class GroupDetails(BaseModel):
    name: str
    description: str
    mail: str
    manager: str


class SetIamDetails(BaseModel):
    project_id: str
    details: dict
