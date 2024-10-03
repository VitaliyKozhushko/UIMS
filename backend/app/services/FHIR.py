"""
Модуль для получения данных о пациентах и записях и сохранения их в БД
"""
import httpx
import json
import os
from pathlib import Path
from datetime import datetime, date
from typing import Union, List, Optional, Any
from fastapi import HTTPException
from sqlalchemy import (select,
                        exists,
                        delete,
                        func)
from sqlalchemy.ext.asyncio import AsyncSession
from ..logging_config import logger
from ..models import (Appointments,
                      Resources,
                      Patients)
from ..database import get_db
from ..schemas.patients import PatientCreate, Identifier, Address


async def get_appointments():
  """
  Получение списка записей на прием
  """
  async for db in get_db():
    try:
      result = await db.execute(select(Resources).where(Resources.type == 'Appointment'))
      resource = result.scalar_one_or_none()

      if not resource:
        result = await db.execute(select(func.count()).select_from(Resources))
        count = result.scalar()
        if count == 0:
          new_resource = Resources(
            type='Appointment'
          )
          db.add(new_resource)
          await db.commit()
      resourse_offline = resource and resource.offline

      if resourse_offline:
        data = get_json_data('appointment', resourse_offline)
      else:
        data = await get_online_data(resourse_offline, resourse_offline)

      resource_id = await check_resources(db, 'Appointment', data.get('meta', {}))

      if not resource_id:
        return

      # Удаляем старые данные
      await db.execute(delete(Patients))
      await db.commit()

      for item in data.get('entry', []):
        resource = item.get('resource')
        if resource:
          patient_id = await get_patient(db, resource.get('participant', {}), resourse_offline)
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


async def create_appointment(resource: dict[str, Union[str, int, List[dict], dict]], resource_id: int,
                             patient_id: str) -> Appointments:
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


def extract_service_details(resource: dict[str, Union[str, int, List[dict], dict]]) -> list[
  dict[str, list[dict[str, Union[str, list[dict[str, str]]]]]]
]:
  """Формирование данных о враче, специализации"""
  service_details = []
  if 'serviceCategory' in resource:
    service_details.append({'serviceCategory': resource['serviceCategory']})
  if 'serviceType' in resource:
    service_details.append({'serviceType': resource['serviceType']})
  if 'specialty' in resource:
    service_details.append({'specialty': resource['specialty']})
  return service_details


def transform_start_end(date_str: str) -> Union[datetime, str]:
  """Преобразование даты в TIMESTAMP"""
  if date_str:
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
  return date_str


async def check_resources(db: AsyncSession, resource: str, meta: Union[dict[str, str], dict]) -> Optional[int]:
  """
  Проверка на существование типа ресурса в БД и добавление запрашиваемого ресурса в БД при его отсутствии
  """
  date_upd = meta.get('lastUpdated')
  exist_resource = await db.execute(
    select(Resources).where(Resources.type == resource)
  )
  exist_resource = exist_resource.scalars().first()
  transform_date = datetime.fromisoformat(date_upd.replace("Z", "+00:00")) if date_upd else None

  if transform_date and exist_resource and exist_resource.last_update == transform_date:
    await db.commit()
    return

  if exist_resource:
    exist_resource.last_update = transform_date
    await db.commit()
    return exist_resource.id
  else:
    new_resource = Resources(
      type=resource,
      last_update=datetime.fromisoformat(date_upd.replace("Z", "+00:00")) if date else None
    )
    db.add(new_resource)
    await db.commit()

    return new_resource.id


async def get_patient(db: AsyncSession, patient_data: Union[list[dict[str, Union[dict[str, str], str]]], dict],
                      resourse_offline: bool) -> Optional[str]:
  """
  Получение данных о пациенте
  """
  patient = next(
    (item['actor']['reference'] for item in patient_data if
     item.get('actor', {}).get('reference', '').startswith('Patient/')),
    None
  )
  if not patient:
    print('Отсутствует id пациента')
    return

  patient_id = patient.removeprefix('Patient/')

  exist_patient = await db.scalar(
    select(exists().where(Patients.patient_id == patient_id))
  )

  if exist_patient:
    return patient_id

  if resourse_offline:
    data = get_json_data('patient', resourse_offline, patient_id)
  else:
    data = await get_online_data(db, resourse_offline)

  try:
    fullname_patient = get_fullname(data.get('name', []))
    upd_birth_date = transform_birth_date(data.get('birthDate'))

    print('data_pat:', data)
    print('upd_birth_date:', upd_birth_date)
    patient_data = PatientCreate(
      patient_id=patient_id,
      identifier=[
        Identifier(
          value=ident.get('value'),
          system=ident.get('system')
        )
        for ident in data.get('identifier', [])
      ] if data.get('identifier') else None,
      fullname=fullname_patient,
      gender=data.get('gender', 'unknown'),
      birth_date=upd_birth_date,
      address=[
        Address(
          use=addr.get('use'),
          line=addr.get('line', []),
          text=addr.get('text')
        )
        for addr in data.get('address', [])
      ] if data.get('address') else None
    )

    new_patient = Patients(
      patient_id=patient_data.patient_id,
      identifier=patient_data.identifier[0].value if patient_data.identifier else None,
      fullname=patient_data.fullname,
      gender=patient_data.gender,
      birth_date=patient_data.birth_date,
      address=[addr.model_dump() for addr in patient_data.address] if patient_data.address else None
    )
    db.add(new_patient)
    await db.commit()
    return patient_id
  except Exception as e:
    await db.rollback()
    print(f"Ошибка при сохранении пациента: {e}")


def get_fullname(name: list[dict[str, Union[str, list[str]]]]) -> str:
  """Получаем полное имя пациента."""
  if len(name) == 0:
    return 'н/д'
  fullname_patient = name[0].get('text', '').strip()
  if not fullname_patient:
    family_name = name[0].get('family', '')
    given_name = ' '.join(name[0].get('given', []))
    fullname_patient = f'{family_name.strip()} {given_name.strip()}'
  return fullname_patient if not fullname_patient.isspace() else 'н/д'


def transform_birth_date(birth_date_str: Optional[str]) -> Optional[date]:
  """Преобразование даты рождения из строки в объект date"""
  print('birth_date_str:', birth_date_str)
  if birth_date_str:
    try:
      return datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    except ValueError:
      print(f'Неправильный формат даты: {birth_date_str}')
  return None


def get_json_data(type_data: str, offline: bool, patient_id: Optional[str] = None) -> dict[str, Any]:
  """
  Получение данных из json-файла (записи на прием/ данные по пациенту)
  """
  backup_directory = Path(__file__).resolve().parent.parent / 'backup'
  try:
    filename = f'patient-{patient_id}.json' if patient_id else 'appointments-bundle.json'
    with open(os.path.join(backup_directory, filename), 'r', encoding='utf-8') as file:
      return json.load(file)
  except FileNotFoundError:
    type_file = 'записями на прием' if type_data == 'appointment' else 'данными о пациенте'
    if offline:
      raise HTTPException(status_code=500, detail=f"Файл с {type_file} не найден.")
    else:
      raise HTTPException(status_code=500, detail=f"Сторонний ресурс недоступен, файл с {type_file} не найден.")

  except Exception as e:
    print(f'Ошибка {e}')


async def get_online_data(db: AsyncSession, resourse_offline: bool, patient_id: Optional[str] = None) -> dict[str, Any]:
  """
  Получение данных из онлайн ресурса
  """
  url = 'https://hapi.fhir.org/baseR4/Appointment?_count=10' if not patient_id else f'http://hapi.fhir.org/baseR4/Patient/{patient_id}'
  try:
    async with httpx.AsyncClient() as client:
      response = await client.get(url)
      response.raise_for_status()
      print('url:', url)
      print('response.json():', response.json())
      return response.json()
  except httpx.TimeoutException:
    logger.info("Таймаут при загрузке данных.")
  except httpx.RequestError as e:
    logger.info(f"Ошибка сети: {e}")
  except httpx.HTTPStatusError as e:
    logger.info(f"HTTP ошибка: {e.response.status_code} - {e.response.text}")

  if not patient_id:
    await db.execute(delete(Patients))
    await db.commit()
  type_data = 'patient' if patient_id else 'appointment'
  return get_json_data(type_data, resourse_offline, patient_id)
