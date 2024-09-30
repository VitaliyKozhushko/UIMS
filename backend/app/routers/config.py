from fastapi import APIRouter, Depends, HTTPException
from app.schemas import OfflineResponse, OfflineUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import get_offline_status, update_offline_status

router = APIRouter()

@router.get("/resources/{resource_type}", response_model=OfflineResponse)
async def get_resource(resource_type: str, db: AsyncSession = Depends(get_db)):
    resource = await get_offline_status(db, resource_type)
    if not resource:
        raise HTTPException(status_code=404, detail="Ресурс не найден")
    return resource

@router.patch("/resources/{resource_type}", response_model=OfflineUpdate)
async def update_resource_offline(resource_type: str, update_data: OfflineUpdate, db: AsyncSession = Depends(get_db)):
    offline_status = bool(update_data.offline)
    updated_resource = await update_offline_status(db, resource_type, offline_status)
    if not updated_resource:
        raise HTTPException(status_code=404, detail="Ресурс не найден")
    return updated_resource