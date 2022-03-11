from typing import List, Optional, Dict
from datetime import date
from pydantic import BaseModel


class Policy(BaseModel):
    bindings: Optional[List[Dict]] = []


class SetIamDetails(BaseModel):
    details: Policy


class HistoricalIamDetails(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
