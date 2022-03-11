from pydantic import BaseModel


class GroupDetails(BaseModel):
    name: str
    description: str
    mail: str
    manager: str
