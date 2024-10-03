from datetime import datetime
from enum import Enum
from pydantic import (BaseModel,
                      field_validator)
from typing import (Dict,
                    Optional,
                    Type)
from ..constants import statuses


def create_enum(name: str, choices: Dict[str, str]) -> Type[Enum]:
  return Enum(name, {key: value for key, value in choices.items()})


StatusEnum = create_enum('StatusEnum', statuses)


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


class ResourseBase(BaseModel):
  pass


class OfflineUpdateRequest(BaseModel):
  offline: bool


class OfflineUpdate(ResourseBase):
  offline: bool
  type: Optional[str] = None

  class Config:
    from_attributes = True


class OfflineResponse(ResourseBase):
  offline: bool
  type: Optional[str] = None

  class Config:
    from_attributes = True
