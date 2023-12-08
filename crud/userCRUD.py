from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from crud.dao import BaseDAO
from models import User, create_async_session
from schemas import UserInDBSchema, UserSchema


class CRUDUsers(BaseDAO):
    model = User
    inDBSchemas = UserInDBSchema

    @classmethod
    @create_async_session
    async def add(cls, user: UserSchema, session: AsyncSession = None) -> UserInDBSchema | None:
        users = cls.model(**user.dict())
        session.add(users)
        try:
            await session.commit()
        except IntegrityError as e:
            print(e)
        else:
            await session.refresh(users)
            return cls.inDBSchemas(**users.__dict__)

    @classmethod
    @create_async_session
    async def get_user(cls, model_id: int, session: AsyncSession = None):
        drivers = await session.execute(
            select(cls.model)
            .where(cls.model.id == model_id)
        )
        if driver := drivers.first():
            return cls.inDBSchemas(**driver[0].__dict__)