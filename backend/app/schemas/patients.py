from datetime import datetime, date
from typing import (List,
                    Optional,
                    ClassVar)
from pydantic import (BaseModel,
                      Field,
                      field_validator,
                      ConfigDict)
from ..constants import GENDERS
from .schemas import AppointmentsResponse


class PatientsBase(BaseModel):
    fullname: str
    gender: GENDERS
    birth_date: Optional[datetime] = None


class PatientsResponse(PatientsBase):
    config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @staticmethod
    @field_validator('gender', mode='before')
    def convert_gender(key: str) -> Optional[str]:
        gender: Optional[GENDERS] = GENDERS.__members__.get(key.upper())
        return gender.value if gender else 'Не указан'


class PatientAppointmentsResponse(BaseModel):
    id: int
    fullname: str
    gender: str
    birth_date: Optional[datetime] = None
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
    identifier: List[Identifier] = Field(default_factory=list)
    fullname: str
    gender: str
    birth_date: Optional[date] = None
    address: Optional[List[Address]] = Field(default=None)
