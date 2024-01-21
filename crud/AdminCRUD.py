from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.dao import BaseDAO
from models import create_async_session, Admin
from schemas.adminSchemas import AdminInDBSchema


class CRUDAdmin(BaseDAO):
    model = Admin
    inDBSchemas = AdminInDBSchema

    @classmethod
    @create_async_session
    async def get_all_only_id(cls, session: AsyncSession = None) -> list:
        getAll = await session.execute(
            select(cls.model.admin_id)
        )
        return [get_All[0] for get_All in getAll]

    @classmethod
    @create_async_session
    async def get_admin_group_id_all(cls, group_id: int, session: AsyncSession = None) -> list[inDBSchemas]:
        getAll = await session.execute(
            select(cls.model).where(cls.model.groups_id == group_id)
        )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]


