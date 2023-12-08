from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import create_async_session


class BaseDAO:
    model = None
    inDBSchemas = None

    @classmethod
    @create_async_session
    async def get_all(cls, session: AsyncSession = None) -> list[inDBSchemas]:
        getAll = await session.execute(
            select(cls.model)
        )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]

    @classmethod
    @create_async_session
    async def get(cls, model_id: int, session: AsyncSession = None):
        drivers = await session.execute(
            select(cls.model)
            .where(cls.model.id == model_id)
        )
        if driver := drivers.first():
            return cls.inDBSchemas(**driver[0].__dict__)

    @classmethod
    @create_async_session
    async def update(cls, schemas: inDBSchemas, session: AsyncSession = None) -> None:
        await session.execute(
            update(cls.model)
            .where(cls.model.id == schemas.id)
            .values(**schemas.dict())
        )
        await session.commit()