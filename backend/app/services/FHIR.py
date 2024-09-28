import httpx
from app.models import Appointments, Resources
from app.database import get_db
from datetime import datetime
from sqlalchemy import select

# URL FIHR
FHIR_URL = "https://hapi.fhir.org/baseR4/Appointment?_count=10"

async def get_appointments():
    async with httpx.AsyncClient() as client:
        response = await client.get(FHIR_URL)
        response.raise_for_status()
        data = response.json()
        print('data:', data)

        async for db in get_db():
            try:
                resource_id = await add_resources(db, 'Appointment', data['meta']['lastUpdated'])

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

                await db.commit()
            finally:
                await db.close()

async def add_resources(db, resource, date):
    existing_resource = await db.execute(
        select(Resources).where(Resources.type == resource)
    )
    existing_resource = existing_resource.scalars().first()

    if existing_resource:
        existing_resource.last_update = datetime.fromisoformat(date.replace("Z", "+00:00"))
        return existing_resource.id
    else:
        new_resource = Resources(
            type='Appointment',
            last_update=datetime.fromisoformat(date.replace("Z", "+00:00"))
        )
        db.add(new_resource)
        await db.flush()

        return new_resource.id
