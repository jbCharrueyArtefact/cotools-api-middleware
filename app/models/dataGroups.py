from typing import List
from pydantic import BaseModel


class DataGroupDetails(BaseModel):
    gestionnaire: List[str]
    restriction_entities: List[str]
    is_bank: str
    description: str
    workload: str
    env: str
