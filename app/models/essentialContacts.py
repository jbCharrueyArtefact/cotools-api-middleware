from typing import List, Optional

from pydantic import BaseModel, Field, validator


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
