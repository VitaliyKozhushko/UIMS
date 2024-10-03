import pytest
from httpx import (AsyncClient,
                   ASGITransport)
from app.main import app
from app.logging_config import logger


@pytest.mark.asyncio
async def test_get_resource_status():
  """
  Проверяем получение статуса offline
  """
  resource_type = "Appointment"

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    response = await ac.get(f"/resources/{resource_type}")

  logger.info(f"Response status: {response.status_code}, data: {response.json()}")
  assert response.status_code == 200
  data = response.json()

  assert "offline" in data
  assert "type" in data
  assert data['offline'] is True or data['offline'] is False
  assert data['type'] == 'Appointment'


@pytest.mark.asyncio
async def test_get_patients_appointments():
  """
  Проверяем получение списка пациентов
  """
  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
    response = await ac.get("/patients/appointments")
  logger.info(f"Response status: {response.status_code}, data: {response.json()}")
  assert response.status_code == 200
  data = response.json()

  # Проверяем, что получен список
  assert isinstance(data, list)
  assert len(data) > 0

  for patient in data:
    assert "fullname" in patient
    assert "gender" in patient
    assert "birth_date" in patient
    assert "gender" in patient
    assert "appointments" in patient
