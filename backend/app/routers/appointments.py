"""
Роуты для работы со списком пацинтов с записями
"""
from fastapi import (APIRouter,
                     Depends)
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from ..models import (Patients,
                        Appointments)
from ..schemas.schemas import (AppointmentsResponse)
from ..schemas.patients import (PatientsResponse,
                                PatientAppointmentsResponse)
from ..database import get_db
from ..services.FHIR import get_appointments

router = APIRouter()


@router.get("/patients/appointments", response_model=List[PatientAppointmentsResponse],
            summary='Список пациентов с записями')
async def get_all_patients_appointments(db: AsyncSession = Depends(get_db)) -> List[PatientAppointmentsResponse]:
  await get_appointments()
  async with db.begin():
    patients_result = await db.execute(select(Patients).options(selectinload(Patients.appointments)))
    patients = patients_result.scalars().fetchall()

    result = [transform_patient_appointments(patient) for patient in patients]
    await db.commit()
    return result


def transform_patient_appointments(patient: Patients) -> PatientAppointmentsResponse:
  """
  Преобразование пациента и его записи в Pydantic модель для ответа
  """
  patient_copy = PatientsResponse.model_validate(patient, from_attributes=True)

  appointments_data = [
    transform_appointment(appointment) for appointment in patient.appointments
  ]

  return PatientAppointmentsResponse(
    id=patient.id,
    fullname=patient_copy.fullname,
    gender=patient_copy.gender.value,
    birth_date=patient_copy.birth_date,
    appointments=appointments_data
  )


def transform_appointment(appointment: Appointments) -> AppointmentsResponse:
  """
  Преобразование записи в Pydantic модель с обработкой статуса
  """
  appointment_copy = AppointmentsResponse.model_validate(appointment, from_attributes=True)

  return appointment_copy
