from datetime import date
import re
from typing import List, Optional, Union, Dict

from pydantic import BaseModel, Field, validator


class Label_map(BaseModel):
    cost_center: str = Field(alias="cost-center")
    accountable: List[str]
    project_owner: List[str] = Field(alias="project-owner")
    project_family: Optional[str] = Field(alias="project-family")
    id_orange_carto: str = Field(alias="id-orange-carto")
    epic: Optional[str]
    expiration_date: Optional[date] = Field(alias="expiration-date")

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


class ProjectDetails(BaseModel):
    demandeur: str
    country: str
    basicat: str = Field(alias="project-internal-id")
    workload_details: str
    env: str = Field(alias="environment")
    parent_folder_id: int
    label_project_confidentiality: str = Field(alias="project-confidentiality")
    label_personal_data: str = Field(alias="personal-data")
    unicity_id: Optional[str]
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
