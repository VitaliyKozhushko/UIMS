from typing import AsyncIterator
import httpx
import pytest
import pytest_asyncio
from httpx import (AsyncClient,
                   ASGITransport)
from app.main import uims_app
from app.logging_config import logger


@pytest_asyncio.fixture(loop_scope='module', name="http_client")
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=uims_app),
                           base_url="http://test") as client_async:
        yield client_async


@pytest.mark.asyncio(loop_scope='module')
async def test_get_resource_status(http_client: httpx.AsyncClient) -> None:
    """
    Проверяем получение статуса offline
    """
    resource_type = "Appointment"

    response = await http_client.get(f"/resources/{resource_type}")

    logger.info("Response status: %s, data: %s", response.status_code, response.json())
    assert response.status_code == 200
    data = response.json()

    assert "offline" in data
    assert "type" in data
    assert data['offline'] is True or data['offline'] is False
    assert data['type'] == 'Appointment'


@pytest.mark.asyncio(loop_scope='module')
async def test_get_patients_appointments(http_client: httpx.AsyncClient) -> None:
    """
    Проверяем получение списка пациентов
    """
    response = await http_client.get("/patients/appointments")

    logger.info("Response status: %s, data: %s", response.status_code, response.json())
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
