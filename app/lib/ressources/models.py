from datetime import date
import re
from typing import List, Optional, Union, Dict

from pydantic import BaseModel, Field, root_validator, validator


class Label_map(BaseModel):
    cost_center: str = Field(alias="cost-center")
    accountable: List[str]
    project_owner: List[str] = Field(alias="project-owner")
    project_family: Optional[str] = Field(alias="project-family")
    id_orange_carto: str = Field(alias="id-orange-carto")
    epic: Optional[str]
    expiration_date: Optional[str] = Field(alias="expiration-date")

    class Config:
        arbitrary_types_allowed = True
        anystr_lower = True
        max_anystr_length = 63

    @validator(
        "cost_center", "project_family", "id_orange_carto", each_item=True
    )
    def validate_format(cls, v):
        assert re.match(
            r"^[a-zA-Z0-9_-]+$", v
        ), "charactere should only use lower case letters, digits, _ or -"
        return v

    """@root_validator
    def parse_liste(cls, values):

        for key in ["project_owner", "accountable"]:
            n = 1
            for elem in values[key]:
                values[f"{key}{n}".replace("_", "-")] = elem
                n += 1
            del values[key]
        return values"""


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


class EssentialContact(BaseModel):
    email: Optional[str]
    notificationCategorySubscriptions: List[str]
    name: Optional[str]


class EssentialContactOut(BaseModel):
    email: Optional[str]
    notificationCategorySubscriptions: List[str]


class EssentialContactList(BaseModel):
    essentialContacts: Optional[List[EssentialContact]] = Field(
        alias="contacts", default=[]
    )

    @validator("essentialContacts")
    def merge_same_mail(cls, v):
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                if v[i].email == v[j].email:
                    v[i].notificationCategorySubscriptions.extend(
                        v[j].notificationCategorySubscriptions
                    )
                    del v[j]
        return v

    class Config:
        allow_population_by_field_name = True


class EssentialContactListOut(BaseModel):
    essentialContacts: Optional[List[EssentialContactOut]] = Field(
        alias="contacts", default=[]
    )

    class Config:
        allow_population_by_field_name = True


class Policy(BaseModel):
    bindings: Optional[List[Dict]] = []


class SetIamDetails(BaseModel):
    project_id: str
    details: Policy


class HistoricalIamDetails(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
