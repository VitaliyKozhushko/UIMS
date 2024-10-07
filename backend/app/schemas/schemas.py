from datetime import datetime
from typing import (Optional,
                    ClassVar)
from pydantic import (BaseModel,
                      field_validator,
                      ConfigDict)
from ..constants import STATUSES


class AppointmentsBase(BaseModel):
    id: int
    status: STATUSES
    date_start: Optional[datetime] = None
    description: Optional[str] = None


class AppointmentsResponse(AppointmentsBase):
    config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @staticmethod
    @field_validator('status', mode='before')
    def convert_status(key: str) -> str:
        upd_key = key.replace('-', '_')
        status: Optional[STATUSES] = STATUSES.__members__.get(upd_key.upper())
        return status.value if status else 'Статус не получен'


class ResourseBase(BaseModel):
    pass


class OfflineUpdateRequest(BaseModel):
    offline: bool


class OfflineUpdate(ResourseBase):
    offline: bool
    type: Optional[str] = None

    config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class OfflineResponse(ResourseBase):
    offline: bool
    type: Optional[str] = None

    config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
