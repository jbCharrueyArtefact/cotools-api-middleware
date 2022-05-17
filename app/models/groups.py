from pydantic import BaseModel, validator
from typing import List
import re


class GroupDetails(BaseModel):
    name: str
    description: str
    mail: str
    manager: str
    ## ajouté
    # groups: List[str]

    @validator("name", "mail")
    def invalidate_datagrp(cls, v):
        assert v.contains("datagrp"), "group name should not contain 'datagrp'"
        return v


class GroupDetailsFromUsers(BaseModel):
    users: List[str]


class UsersGroup(BaseModel):
    users: List[str]


class GroupList(BaseModel):
    groups: List[str]
