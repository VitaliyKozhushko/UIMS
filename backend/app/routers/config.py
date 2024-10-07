"""
Роуты для изменения настроек проекта. В данном случае - вкл./выкл. симуляции обрыва сети
"""
from typing import Optional
from fastapi import (APIRouter,
                     Depends,
                     HTTPException)
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.schemas import (OfflineResponse,
                               OfflineUpdate,
                               OfflineUpdateRequest)
from ..database import get_db
from ..crud import (get_resource_data,
                    update_offline_status)
from ..models import Resources

router = APIRouter()


@router.get("/resources/{resource_type}",
            response_model=OfflineResponse,
            summary="Статус иммитации обрыва сети")
async def get_resource(resource_type: str,
                       db: AsyncSession = Depends(get_db)) -> Optional[Resources]:
    resource = await get_resource_data(db, resource_type)
    if not resource:
        raise HTTPException(status_code=404, detail="Ресурс не найден")
    return resource


@router.patch("/resources/{resource_type}", response_model=OfflineUpdate,
              summary="Изменение статуса иммитации обрыва сети")
async def update_resource_offline(resource_type: str, update_data: OfflineUpdateRequest,
                                  db: AsyncSession = Depends(get_db)) \
        -> Optional[Resources]:
    offline_status = bool(update_data.offline)
    updated_resource = await update_offline_status(db, resource_type, offline_status)
    if not updated_resource:
        raise HTTPException(status_code=404, detail="Ресурс не найден")
    return updated_resource
