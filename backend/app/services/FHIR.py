import httpx
from app.models import Appointments, Resources, Patients
from app.database import get_db
from datetime import datetime
from sqlalchemy import select, exists

# URL FIHR
FHIR_URL = "https://hapi.fhir.org/baseR4/Appointment?_count=10"

async def get_appointments():
    """
    Получение списка записей на прием
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(FHIR_URL)
        response.raise_for_status()
        data = response.json()

        async for db in get_db():
            try:
                resource_id = await check_resources(db, 'Appointment', data['meta']['lastUpdated'])

                for item in data.get('entry', []):
                    resource = item.get('resource')
                    if resource:
                        service_details = []
                        if 'serviceCategory' in resource:
                            service_details.append({'serviceCategory': resource['serviceCategory']})
                        if 'serviceType' in resource:
                            service_details.append({'serviceType': resource['serviceType']})
                        if 'specialty' in resource:
                            service_details.append({'specialty': resource['specialty']})
                        date_start = resource.get('start')
                        date_stop = resource.get('stop')
                        if isinstance(date_start, str):
                            date_start = datetime.fromisoformat(date_start.replace("Z", "+00:00"))
                        if isinstance(date_stop, str):
                            date_stop = datetime.fromisoformat(date_stop.replace("Z", "+00:00"))
                        new_appointment = Appointments(
                            status=resource.get('status', 'entered-in-error'),
                            service_details=service_details,
                            date_start=date_start,
                            date_end=date_stop,
                            description=resource.get('description'),
                            participants=resource.get('participant'),
                            priority=resource.get('priority'),
                            resource_id=resource_id
                        )
                        db.add(new_appointment)
                        await get_patient(db, resource.get('participant'))

                await db.commit()
            except Exception as e:
                await db.rollback()
                print(f"Ошибка при сохранении записи: {e}")
            finally:
                await db.close()

async def check_resources(db, resource, date):
    """
    Проверка на существование типа ресурса в БД и добавление запрашиваемого ресурса в БД при его отсутствии
    """
    exist_resource = await db.execute(
        select(Resources).where(Resources.type == resource)
    )
    exist_resource = exist_resource.scalars().first()

    if exist_resource:
        exist_resource.last_update = datetime.fromisoformat(date.replace("Z", "+00:00"))
        return exist_resource.id
    else:
        new_resource = Resources(
            type=resource,
            last_update=datetime.fromisoformat(date.replace("Z", "+00:00"))
        )
        db.add(new_resource)
        await db.commit()

        return new_resource.id

async def get_patient(db, patient_data):
    """
    Получение данных о пациенте
    """
    patient = patient_data[0].get('actor', {}).get('reference')
    if not patient:
        print('Отсутствует id пациента')
        return

    patient_id = patient.removeprefix('Patient/')

    exist_patient = await db.execute(
        select(exists().where(Patients.patient_id == patient_id))
    )

    if exist_patient.scalar():
        print(f'Пациент с patient_id={patient_id} уже существует в БД')
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://hapi.fhir.org/baseR4/Patient/{patient_id}')
        response.raise_for_status()
        data = response.json()

        try:
            resource_id = await check_resources(db, 'Patient', data['meta']['lastUpdated'])

            fullname_patient = get_fullname(data.get('name', []))
            birth_date = transform_birth_date(data.get('birthDate'))

            new_patient = Patients(
                patient_id=patient_id,
                identifier=data.get('identifier', [{}])[0].get('value'),
                fullname=fullname_patient,
                gender=data.get('gender', 'unknown'),
                birthDate=birth_date,
                address=data.get('address', [{}])[0].get('text'),
                resource_id=resource_id
            )
            db.add(new_patient)
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f"Ошибка при сохранении пациента: {e}")

def get_fullname(name):
    """Получаем полное имя пациента."""
    if len(name) == 0:
        return 'н/д'
    fullname_patient = name[0].get('text')
    if not fullname_patient:
        family_name = name[0].get('family', '')
        given_name = ' '.join(name[0].get('given', []))
        fullname_patient = f'{family_name} {given_name}'
    return fullname_patient if not fullname_patient.isspace() else 'н/д'

def transform_birth_date(birth_date_str):
    """Преобразование даты рождения из строки в объект date"""
    if birth_date_str:
        try:
            return datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f'Неправильный формат даты: {birth_date_str}')
    return None