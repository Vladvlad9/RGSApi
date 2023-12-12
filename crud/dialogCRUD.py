from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from crud.dao import BaseDAO
from models import Dialogue, create_async_session
from schemas.dialogsSchemas import DialogSchemas, DialogInDBSchema
from datetime import datetime, timedelta


class CRUDDialog(BaseDAO):
    model = Dialogue
    inDBSchemas = DialogInDBSchema

    @staticmethod
    @create_async_session
    async def add(dialog: DialogSchemas, session: AsyncSession = None) -> DialogInDBSchema | None:
        dialogs = Dialogue(**dialog.dict())
        session.add(dialogs)
        try:
            await session.commit()
        except IntegrityError as e:
            print(e)
        else:
            await session.refresh(dialogs)
            return DialogInDBSchema(**dialogs.__dict__)

    @classmethod
    @create_async_session
    async def getTrueDialog(cls, user_id: int, session: AsyncSession = None):
        dialogs = await session.execute(
            select(cls.model).where(cls.model.user_id == user_id).where(cls.model.is_active == True)
        )
        if dialog := dialogs.first():
            return cls.inDBSchemas(**dialog[0].__dict__)

    @classmethod
    @create_async_session
    async def getDialogAll(cls, is_active: bool, session: AsyncSession = None) -> list[inDBSchemas]:
        if is_active:
            getAll = await session.execute(
                select(cls.model).where(cls.model.is_active == True)
            )
            return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]
        else:
            getAll = await session.execute(
                select(cls.model).where(cls.model.is_active == False)
            )
            return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]

    @classmethod
    @create_async_session
    async def getTrueDialogAdmin(cls, admin_id: int, session: AsyncSession = None):
        dialogs = await session.execute(
            select(cls.model).where(cls.model.admin_id == admin_id)
        )
        if dialog := dialogs.first():
            return cls.inDBSchemas(**dialog[0].__dict__)

    @classmethod
    @create_async_session
    async def get_all_for_user(cls, user_id: int, session: AsyncSession = None) -> list[inDBSchemas]:
        getAll = await session.execute(
            select(cls.model).where(cls.model.user_id == user_id).where(cls.model.who_closed == "None")
        )
        if get_All := getAll.first():
            return cls.inDBSchemas(**get_All[0].__dict__)

    @classmethod
    @create_async_session
    async def getActiveUser(cls, user_id: int, session: AsyncSession = None) -> inDBSchemas:
        drivers = await session.execute(
            select(cls.model)
            .where(cls.model.user_id == user_id).where(cls.model.who_closed == "None")
        )
        if driver := drivers.first():
            return cls.inDBSchemas(**driver[0].__dict__)

    @classmethod
    @create_async_session
    async def getActiveNone(cls, admin_id: int, session: AsyncSession = None) -> inDBSchemas:
        drivers = await session.execute(
            select(cls.model)
            .where(cls.model.admin_id == admin_id).where(cls.model.who_closed == "None")
        )
        if driver := drivers.first():
            return cls.inDBSchemas(**driver[0].__dict__)

    @classmethod
    @create_async_session
    async def get_all_td(cls, session: AsyncSession = None) -> list[inDBSchemas]:
        # Получаем начало сегодняшнего дня
        start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        # Получаем конец сегодняшнего дня
        end_of_today = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос с фильтром по дате создания
        getAll = await session.execute(
            select(cls.model)
            .where(cls.model.created_at >= start_of_today,
                   cls.model.created_at <= end_of_today)
        )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]

    @classmethod
    @create_async_session
    async def get_all_wk(cls, session: AsyncSession = None) -> list[inDBSchemas]:
        # Получаем начало текущей недели (понедельник)
        start_of_week = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        # Получаем конец текущей недели (воскресенье)
        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос с фильтром по дате создания за неделю
        get_all_week = await session.execute(
            select(cls.model).where(cls.model.created_at >= start_of_week,
                                    cls.model.created_at <= end_of_week)
        )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in get_all_week]

    @classmethod
    @create_async_session
    async def get_all_mn(cls, session: AsyncSession = None) -> list[inDBSchemas]:
        # Получаем начало текущего месяца
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Получаем конец текущего месяца
        end_of_month = (datetime.utcnow().replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос с фильтром по дате создания за месяц
        get_all_month = await session.execute(
            select(cls.model).where(cls.model.created_at >= start_of_month,
                                    cls.model.created_at <= end_of_month)
        )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in get_all_month]


    @classmethod
    @create_async_session
    async def get_all_today(cls, is_active: bool, session: AsyncSession = None) -> list[inDBSchemas]:
        # Получаем начало сегодняшнего дня
        start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        # Получаем конец сегодняшнего дня
        end_of_today = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос с фильтром по дате создания
        if is_active:
            getAll = await session.execute(
                select(cls.model)
                .where(cls.model.created_at >= start_of_today,
                       cls.model.created_at <= end_of_today)
                .where(cls.model.is_active == True)
            )
        else:
            getAll = await session.execute(
                select(cls.model)
                .where(cls.model.created_at >= start_of_today,
                       cls.model.created_at <= end_of_today)
                .where(cls.model.is_active == False)
            )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in getAll]

    @classmethod
    @create_async_session
    async def get_all_week(cls, is_active: bool, session: AsyncSession = None) -> list[inDBSchemas]:
        # Получаем начало текущей недели (понедельник)
        start_of_week = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        # Получаем конец текущей недели (воскресенье)
        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос с фильтром по дате создания за неделю
        if is_active:
            get_all_week = await session.execute(
                select(cls.model).where(cls.model.created_at >= start_of_week,
                                        cls.model.created_at <= end_of_week)
                .where(cls.model.is_active == True)
            )
        else:
            get_all_week = await session.execute(
                select(cls.model).where(cls.model.created_at >= start_of_week,
                                        cls.model.created_at <= end_of_week)
                .where(cls.model.is_active == False)
            )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in get_all_week]

    @classmethod
    @create_async_session
    async def get_all_month(cls, is_active: bool, session: AsyncSession = None) -> list[inDBSchemas]:
        # Получаем начало текущего месяца
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Получаем конец текущего месяца
        end_of_month = (datetime.utcnow().replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Выполняем запрос с фильтром по дате создания за месяц
        if is_active:
            get_all_month = await session.execute(
                select(cls.model).where(cls.model.created_at >= start_of_month,
                                        cls.model.created_at <= end_of_month)
                .where(cls.model.is_active == True)
            )
        else:
            get_all_month = await session.execute(
                select(cls.model).where(cls.model.created_at >= start_of_month,
                                        cls.model.created_at <= end_of_month)
                .where(cls.model.is_active == False)
            )
        return [cls.inDBSchemas(**get_All[0].__dict__) for get_All in get_all_month]

