from pydantic import BaseModel
from typing import Dict, Optional, Type
from datetime import datetime
from app.constants import statuses, genders
from enum import Enum

def create_enum(name: str, choices: Dict[str, str]) -> Type[Enum]:
    return Enum(name, choices)

StatusEnum = create_enum('StatusEnum', statuses)
GenderEnum = create_enum('GenderEnam', genders)

class AppointmentsBase(BaseModel):
    id: int
    status: StatusEnum
    date_start: datetime
    description: Optional[str] = None

class AppointmentsResponse(AppointmentsBase):
    class Config:
        from_attributes = True

class PatientsBase(BaseModel):
    id: int
    fullname: str
    gender: GenderEnum
    birthDate: datetime

class PatientsResponse(PatientsBase):
    class Config:
        from_attributes = True