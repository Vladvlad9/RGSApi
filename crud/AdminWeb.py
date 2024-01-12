from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.dao import BaseDAO
from models import AdminWeb, create_async_session
from schemas.adminWebSchemas import AdminWebInDBSchema


class CRUDAdminWeb(BaseDAO):
    model = AdminWeb
    inDBSchemas = AdminWebInDBSchema

    @staticmethod
    @create_async_session
    async def get_admin(email: str, password: str,
                  session: AsyncSession = None) -> AdminWebInDBSchema | None:
        admins = await session.execute(
            select(AdminWeb).where(and_(AdminWeb.email == email, AdminWeb.password == password))
        )
        if admin := admins.first():
            return AdminWebInDBSchema(**admin[0].__dict__)

    @classmethod
    @create_async_session
    async def get_id(cls, id: int, session: AsyncSession = None) -> AdminWebInDBSchema | None:
        admins = await session.execute(
            select(cls.model).where(cls.model.id == id)
        )
        if admin := admins.first():
            return AdminWebInDBSchema(**admin[0].__dict__)

