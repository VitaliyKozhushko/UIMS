from datetime import datetime
from typing import List, Optional
from pydantic import (BaseModel,
                      Field,
                      field_validator)
from ..constants import genders
from .schemas import create_enum, AppointmentsResponse

GenderEnum = create_enum('GenderEnam', genders)


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


class PatientAppointmentsResponse(BaseModel):
  id: int
  fullname: str
  gender: str
  birth_date: datetime
  appointments: List[AppointmentsResponse]


class Identifier(BaseModel):
  value: str
  system: str


class Address(BaseModel):
  use: Optional[str] = Field(default=None)
  line: List[str] = Field(default_factory=list)
  text: Optional[str] = Field(default=None)


class PatientCreate(BaseModel):
  patient_id: str
  identifier: Optional[List[Identifier]] = Field(default=None)
  fullname: str
  gender: str
  birth_date: datetime
  address: Optional[List[Address]] = Field(default=None)
