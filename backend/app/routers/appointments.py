from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select
from typing import List
from app.models import Appointments, Patients
from app.schemas import AppointmentsBase, PatientsBase, BaseModel
from app.database import get_db
from app.constants import statuses, genders

router = APIRouter()

class PatientAppointmentsResponse(BaseModel):
    patient: PatientsBase
    appointments: List[AppointmentsBase]

@router.get("/patients/appointments", response_model=List[PatientAppointmentsResponse])
async def get_all_patients_appointments(db: Session = Depends(get_db)):
    result = []

    patients_result = await db.execute(select(Patients).options(selectinload(Patients.appointments)))
    patients = patients_result.scalars().fetchall()

    for patient in patients:
        result.append(PatientAppointmentsResponse(
            patient=PatientsBase(
                id=patient.id,
                fullname=patient.fullname,
                gender=genders.get(patient.gender, 'unknown'),
                birthDate=patient.birth_date
            ),
            appointments=[AppointmentsBase(
                id=appointment.id,
                status=statuses.get(appointment.status, 'entered-in-error'),
                date_start=appointment.date_start,
                description=appointment.description
            ) for appointment in patient.appointments]
        ))

    return result
