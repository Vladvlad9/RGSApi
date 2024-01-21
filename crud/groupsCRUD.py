from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.dao import BaseDAO
from models import Groups, create_async_session
from schemas.groupsSchemas import GroupsInDBSchema


class CRUDGroups(BaseDAO):
    model = Groups
    inDBSchemas = GroupsInDBSchema

    @classmethod
    @create_async_session
    async def get_id(cls, id: int, session: AsyncSession = None) -> inDBSchemas:
        drivers = await session.execute(
            select(cls.model)
            .where(cls.model.id == id)
        )
        if driver := drivers.first():
            return cls.inDBSchemas(**driver[0].__dict__)