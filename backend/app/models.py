from sqlalchemy import (Integer,
                        String,
                        TIMESTAMP,
                        DATE,
                        ForeignKey,
                        Enum,
                        JSON,
                        Boolean)
from sqlalchemy.orm import (relationship,
                            mapped_column,
                            DeclarativeBase)
from .constants import (STATUSES,
                        GENDERS)


class Base(DeclarativeBase):
    pass


class Resources(Base):
    """
    Resources - таблица ресурсов для основных действий. В рамках данного задания исп. 1 ресурс - Appointment
    Атрибуты:
        type (str) - тип ресурса (Appointments)
        last_update (datetime) - дата обновления (запрос Appointment => .meta.lastUpdated)
        offline (bool) - определяет, откуда загружать данные: online / из json-файла
    """
    __tablename__ = 'resources'

    id = mapped_column(Integer, primary_key=True, index=True)
    type = mapped_column(String, nullable=False, unique=True)
    last_update = mapped_column(TIMESTAMP(timezone=True))
    offline = mapped_column(Boolean, nullable=False, default=False)


class Appointments(Base):
    """
    Appointments - таблица записей на прием
    Атрибуты:
        status (ENUM) - статус записи (один из ключей константы STATUSES)
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

    id = mapped_column(Integer, primary_key=True, index=True)
    status = mapped_column(Enum(STATUSES), name='status_enum', nullable=False)
    service_details = mapped_column(JSON)  # serviceCategory, serviceType, specialty
    date_start = mapped_column(TIMESTAMP(timezone=True))
    date_end = mapped_column(TIMESTAMP(timezone=True))
    description = mapped_column(String)
    participants = mapped_column(JSON)
    priority = mapped_column(Integer)
    resource_id = mapped_column(Integer, ForeignKey('resources.id'))
    patient_id = mapped_column(String, ForeignKey('patients.patient_id', ondelete='CASCADE'))

    resource = relationship('Resources')
    patient = relationship('Patients', back_populates='appointments')


class Patients(Base):
    """
    Patients - таблица пациентов
    Атрибуты:
        patient_id (int) - id пациента для поиска данных о нем (actor.reference)
        identifier (str) - № карты пациента
        fullname (str) - ФИО
        gender (ENUM) - пол (один из ключей константы GENDERS)
        birth_date (datetime) - ДР
        address (List[Dict[str, Any]]) - адрес
    """
    __tablename__ = 'patients'

    id = mapped_column(Integer, primary_key=True, index=True)
    patient_id = mapped_column(String, unique=True, nullable=False)
    identifier = mapped_column(String)
    fullname = mapped_column(String, nullable=False)
    gender = mapped_column(Enum(GENDERS), name='gender_name', nullable=False)
    birth_date = mapped_column(DATE)
    address = mapped_column(JSON)

    appointments = relationship('Appointments', back_populates='patient')
