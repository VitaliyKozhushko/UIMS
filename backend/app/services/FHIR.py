import httpx, json, os
from fastapi import HTTPException
from app.models import Appointments, Resources, Patients
from app.database import get_db
from datetime import datetime
from sqlalchemy import select, exists, delete
from pathlib import Path


async def get_appointments():
  """
  Получение списка записей на прием
  """
  try:
    async with httpx.AsyncClient() as client:
      response = await client.get('https://hapi.fhir.org/baseR4/Appointment?_count=10')
      response.raise_for_status()
      data = response.json()
  except (httpx.RequestError, httpx.HTTPStatusError):
    try:
      backup_directory = Path(__file__).resolve().parent.parent / 'backup'
      with open(os.path.join(backup_directory, 'appointments-bundle.json'), 'r') as file:
        data = json.load(file)
    except FileNotFoundError:
      raise HTTPException(status_code=500, detail="Сторонний ресурс недоступен, файл с записями на прием не найден.")

  async for db in get_db():
    try:
      resource_id = await check_resources(db, 'Appointment', data.get('meta', {}))

      if not resource_id:
        return

      # Удаляем старые данные
      await db.execute(delete(Appointments))
      await db.execute(delete(Patients))
      await db.commit()

      for item in data.get('entry', []):
        resource = item.get('resource')
        if resource:
          patient_id = await get_patient(db, resource.get('participant'))
          if patient_id:
            new_appointment = await create_appointment(resource, resource_id, patient_id)
            db.add(new_appointment)

      await db.commit()
      print('Данные сохранены')
    except Exception as e:
      await db.rollback()
      print(f"Ошибка при сохранении записи: {e}")
    finally:
      await db.close()


async def create_appointment(resource, resource_id, patient_id):
  """
  Создание новой записи на приём
  """
  service_details = extract_service_details(resource)
  date_start = transform_start_end(resource.get('start'))
  date_stop = transform_start_end(resource.get('end'))

  return Appointments(
    status=resource.get('status', 'entered-in-error'),
    service_details=service_details,
    date_start=date_start,
    date_end=date_stop,
    description=resource.get('description'),
    participants=resource.get('participant'),
    priority=resource.get('priority'),
    resource_id=resource_id,
    patient_id=patient_id
  )


def extract_service_details(resource):
  """Формирование данных о враче, специализации"""
  service_details = []
  if 'serviceCategory' in resource:
    service_details.append({'serviceCategory': resource['serviceCategory']})
  if 'serviceType' in resource:
    service_details.append({'serviceType': resource['serviceType']})
  if 'specialty' in resource:
    service_details.append({'specialty': resource['specialty']})
  return service_details


def transform_start_end(date_str):
  """Преобразование даты в TIMESTAMP"""
  if isinstance(date_str, str):
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
  return date_str


async def check_resources(db, resource, meta):
  """
  Проверка на существование типа ресурса в БД и добавление запрашиваемого ресурса в БД при его отсутствии
  """
  date = meta.get('lastUpdated')
  exist_resource = await db.execute(
    select(Resources).where(Resources.type == resource)
  )
  exist_resource = exist_resource.scalars().first()
  transform_date = datetime.fromisoformat(date.replace("Z", "+00:00")) if date else None

  if transform_date and exist_resource.last_update == transform_date:
    return

  if exist_resource:
    exist_resource.last_update = transform_date
    return exist_resource.id
  else:
    new_resource = Resources(
      type=resource,
      last_update=datetime.fromisoformat(date.replace("Z", "+00:00")) if date else None
    )
    db.add(new_resource)
    await db.commit()

    return new_resource.id


async def get_patient(db, patient_data):
  """
  Получение данных о пациенте
  """
  patient = next(
      (item['actor']['reference'] for item in patient_data if item.get('actor', {}).get('reference', '').startswith('Patient/')),
      None
  )
  if not patient:
    print('Отсутствует id пациента')
    return

  patient_id = patient.removeprefix('Patient/')

  exist_patient = await db.execute(
    select(exists().where(Patients.patient_id == patient_id))
  )

  if exist_patient.scalar():
    return patient_id

  try:
    async with httpx.AsyncClient() as client:
      response = await client.get(f'http://hapi.fhir.org/baseR4/Patient/{patient_id}')
      response.raise_for_status()
      data = response.json()
  except (httpx.RequestError, httpx.HTTPStatusError):
    try:
      backup_directory = Path(__file__).resolve().parent.parent / 'backup'
      with open(os.path.join(backup_directory, f'patient-{patient_id}.json'), 'r') as file:
        data = json.load(file)
    except FileNotFoundError:
      raise HTTPException(status_code=500,
                          detail="Сторонний ресурс недоступен, файл с данными о пациенте не найден.")

  try:
      fullname_patient = get_fullname(data.get('name', []))
      upd_birth_date = transform_birth_date(data.get('birthDate'))

      new_patient = Patients(
          patient_id=patient_id,
          identifier=data.get('identifier', [{}])[0].get('value'),
          fullname=fullname_patient,
          gender=data.get('gender', 'unknown'),
          birth_date=upd_birth_date,
          address=data.get('address', [{}])[0].get('text')
      )
      db.add(new_patient)
      await db.commit()
      return patient_id
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
