from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Resources


async def get_resource_data(db: AsyncSession, resource_type: str) -> Resources:
  """
  Получение списка ресурсов
  """
  try:
    query = select(Resources).where(Resources.type == resource_type)
    result = await db.execute(query)
    resource = result.scalar_one_or_none()
    await db.commit()
    return resource
  except Exception as e:
    print(f'Ошибка {e}')
    raise


async def update_offline_status(db: AsyncSession, resource_type: str, offline_status: bool) -> Optional[Resources]:
  """
  Вкл./выкл. симуляции обрыва сети
  """
  query = select(Resources).where(Resources.type == resource_type)
  result = await db.execute(query)
  resource = result.scalar_one_or_none()

  if resource:
    resource.offline = offline_status
    await db.commit()
    return resource
  return None
