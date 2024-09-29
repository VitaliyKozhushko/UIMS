from pydantic import BaseModel
from typing import Dict, Optional, Type
from datetime import datetime
from app.constants import statuses, genders
from enum import Enum
from pydantic import field_validator

def create_enum(name: str, choices: Dict[str, str]) -> Type[Enum]:
    return Enum(name, {key: value for key, value in choices.items()})

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

    @field_validator('status', mode='before')
    def convert_gender(cls, value):
        return statuses.get(value, 'Статус не получен')

class PatientsBase(BaseModel):
    fullname: str
    gender: GenderEnum
    birth_date: datetime

class PatientsResponse(PatientsBase):
    class Config:
        from_attributes = True

    @field_validator('gender', mode='before')
    def convert_gender(cls, value):
        return genders.get(value, 'Не указан')