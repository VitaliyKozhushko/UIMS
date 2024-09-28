from sqlalchemy import Column, Integer, String, TIMESTAMP, DATE, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.constants import statuses, genders

Base = declarative_base()

class Resources(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    last_update = Column(TIMESTAMP(timezone=True), nullable=False)

class Appointments(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(*statuses.keys(), name='status_enum'), nullable=False)
    service_details = Column(JSON) # serviceCategory, serviceType, specialty
    date_start = Column(TIMESTAMP(timezone=True))
    date_end = Column(TIMESTAMP(timezone=True))
    description = Column(String)
    participants = Column(JSON)
    priority = Column(Integer)
    resource_id = Column(Integer, ForeignKey('resources.id'))

    resource = relationship('Resources')

    @property
    def status_title(self):
        return statuses.get(self.status, statuses['entered-in-error'])

class Patients(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String)
    fullname = Column(String, nullable=False)
    gender = Column(Enum(*genders.keys(), name='gender_name', nullable=False))
    birthDate = Column(DATE, nullable=False)
    address = Column(JSON)
    resource_id = Column(Integer, ForeignKey('resources.id'))

    resource = relationship('Resources')

    @property
    def gender_title(self):
        return genders.get(self.gender, 'Не указан')