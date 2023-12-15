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


