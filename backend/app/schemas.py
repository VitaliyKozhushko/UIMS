from pydantic import BaseModel
from typing import Dict, Any, Optional, Type
from datetime import datetime
from constants import statuses, genders
from enum import Enum

def create_enum(name: str, choices: Dict[str, str]) -> Type[Enum]:
    return Enum(name, choices)

StatusEnam = create_enum('StatusEnum', statuses)
GenderEnam = create_enum('GenderEnam', genders)

class AppointmentsBase(BaseModel):
    id: int
    status: StatusEnam
    service_details: Optional[Dict[str, Any]]
    date_start: datetime
    date_end: datetime
    description: Optional[str] = None
    participants: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None

class AppointmentsResponse(AppointmentsBase):
    class Config:
        from_attributes = True

class PatientsBase(BaseModel):
    id: int
    identifier: str
    fullname: str
    gender: GenderEnam
    birthDate: datetime
    address: Optional[Dict[str, Any]]

class PatientsResponse(PatientsBase):
    class Config:
        from_attributes = True