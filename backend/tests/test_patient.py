from typing import AsyncIterator
import httpx
import pytest
import pytest_asyncio
from httpx import (AsyncClient,
                   ASGITransport)
from app.main import app
from app.logging_config import logger



@pytest_asyncio.fixture(loop_scope='module')
async def client() -> AsyncIterator[httpx.AsyncClient]:
  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
    yield client


@pytest.mark.asyncio(loop_scope='module')
async def test_get_resource_status(client: httpx.AsyncClient):
  """
  Проверяем получение статуса offline
  """
  resource_type = "Appointment"

  response = await client.get(f"/resources/{resource_type}")

  logger.info(f"Response status: {response.status_code}, data: {response.json()}")
  assert response.status_code == 200
  data = response.json()

  assert "offline" in data
  assert "type" in data
  assert data['offline'] is True or data['offline'] is False
  assert data['type'] == 'Appointment'


@pytest.mark.asyncio(loop_scope='module')
async def test_get_patients_appointments(client: httpx.AsyncClient):
  """
  Проверяем получение списка пациентов
  """
  response = await client.get("/patients/appointments")

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
