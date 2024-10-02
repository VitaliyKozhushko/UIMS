from sqlalchemy import Column, Integer, String, TIMESTAMP, DATE, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.constants import statuses, genders

Base = declarative_base()


class Resources(Base):
  """
  Resources - таблица ресурсов для основных действий. В рамках данного задания исп. 1 ресурс - Appointment
  Атрибуты:
      type (str) - тип ресурса (Appointments)
      last_update (datetime) - дата обновления (запрос Appointment => .meta.lastUpdated)
      offline (bool) - определяет, откуда загружать данные: online / из json-файла
  """
  __tablename__ = 'resources'

  id = Column(Integer, primary_key=True, index=True)
  type = Column(String, nullable=False)
  last_update = Column(TIMESTAMP(timezone=True))
  offline = Column(Boolean, nullable=False, default=False)


class Appointments(Base):
  """
  Appointments - таблица записей на прием
  Атрибуты:
      status (str) - статус записи (один из ключей константы statuses)
      service_details (List[Dict[str, Any]]) - вкл. набор serviceCategory, serviceType, specialty
      date_start (datetime) - дата начала приема
      date_end (datetime) - дата завершения приема
      description (str) - описание
      participants (List[Dict[str, Any]]) - данные о пациенте
      priority (int) - приоритет
      resource_id (int) - foreign key на ресурс
      patient_id (int) - foreign key на пациента
  """
  __tablename__ = 'appointments'

  id = Column(Integer, primary_key=True, index=True)
  status = Column(Enum(*statuses.keys(), name='status_enum'), nullable=False)
  service_details = Column(JSON)  # serviceCategory, serviceType, specialty
  date_start = Column(TIMESTAMP(timezone=True))
  date_end = Column(TIMESTAMP(timezone=True))
  description = Column(String)
  participants = Column(JSON)
  priority = Column(Integer)
  resource_id = Column(Integer, ForeignKey('resources.id'))
  patient_id = Column(String, ForeignKey('patients.patient_id'))

  resource = relationship('Resources')
  patient = relationship('Patients', back_populates='appointments')


class Patients(Base):
  """
  Patients - таблица пациентов
  Атрибуты:
      patient_id (int) - id пациента для поиска данных о нем (actor.reference)
      identifier (str) - № карты пациента
      fullname (str) - ФИО
      gender (str) - пол (один из ключей константы genders)
      birth_date (datetime) - ДР
      address (List[Dict[str, Any]]) - адрес
  """
  __tablename__ = 'patients'

  id = Column(Integer, primary_key=True, index=True)
  patient_id = Column(String, unique=True, nullable=False)
  identifier = Column(String)
  fullname = Column(String, nullable=False)
  gender = Column(Enum(*genders.keys(), name='gender_name', nullable=False))
  birth_date = Column(DATE, nullable=False)
  address = Column(JSON)

  appointments = relationship('Appointments', back_populates='patient')
