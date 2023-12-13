from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from crud.dao import BaseDAO
from models import User, create_async_session
from schemas import UserInDBSchema, UserSchema
from datetime import datetime, timedelta


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

    @classmethod
    @create_async_session
    async def get_all_is_block(cls, is_block: bool, session: AsyncSession = None) -> list[inDBSchemas]:
        if is_block:
            getAll = await session.execute(
                select(cls.model).where(cls.model.is_block == True)
            )
        else:
            getAll = await session.execute(
                select(cls.model).where(cls.model.is_block == False)
            )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]

    @classmethod
    @create_async_session
    async def get_count_today(cls, session: AsyncSession = None) -> tuple[int, int]:
        # Получаем начало и конец сегодняшнего дня
        start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос для подсчета записей, которые попадают под фильтр
        count_inside = await session.execute(
            select(func.count()).where(cls.model.updated_at >= start_of_today,
                                       cls.model.updated_at <= end_of_today)
        )
        inside_count = count_inside.scalar()

        # Выполняем запрос для подсчета записей, которые не попадают под фильтр
        count_outside = await session.execute(
            select(func.count()).where(cls.model.updated_at < start_of_today)
            .union_all(
                select(func.count()).where(cls.model.updated_at > end_of_today)
            )
        )
        outside_count = count_outside.scalar()

        return inside_count, outside_count
