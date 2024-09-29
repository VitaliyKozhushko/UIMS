from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select
from typing import List
from app.models import Patients, Appointments
from app.schemas import AppointmentsResponse, PatientsResponse, PatientAppointmentsResponse
from app.database import get_db

router = APIRouter()

@router.get("/patients/appointments", response_model=List[PatientAppointmentsResponse])
async def get_all_patients_appointments(db: AsyncSession = Depends(get_db)):
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
        gender=patient_copy.gender,
        birth_date=patient_copy.birth_date,
        appointments=appointments_data
    )


def transform_appointment(appointment: Appointments) -> AppointmentsResponse:
    """
    Преобразование записи в Pydantic модель с обработкой статуса
    """
    appointment_copy = AppointmentsResponse.model_validate(appointment, from_attributes=True)

    return appointment_copy