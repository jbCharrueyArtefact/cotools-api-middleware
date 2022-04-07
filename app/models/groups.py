from pydantic import BaseModel
from typing import List
import re


class GroupDetails(BaseModel):
    name: str
    description: str
    mail: str
    manager: str
    ## ajouté
    # groups: List[str]


class GroupDetailsFromUsers(BaseModel):
    users: List[str]
