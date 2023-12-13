from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.dao import BaseDAO
from models import create_async_session, Admin
from schemas.adminSchemas import AdminInDBSchema


class CRUDAdmin(BaseDAO):
    model = Admin
    inDBSchemas = AdminInDBSchema


