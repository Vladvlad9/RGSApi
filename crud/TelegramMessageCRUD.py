from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.dao import BaseDAO
from models import TelegramMessage, create_async_session
from schemas.TelegramMessageSchemas import TelegramMessageInDBSchema, TelegramMessageSchema


class CRUDTelegramMessage(BaseDAO):
    model = TelegramMessage
    inDBSchemas = TelegramMessageInDBSchema

    @classmethod
    @create_async_session
    async def add(cls, message: TelegramMessageSchema, session: AsyncSession = None) -> TelegramMessageInDBSchema | None:
        messages = cls.model(**message.dict())
        session.add(messages)
        try:
            await session.commit()
        except IntegrityError as e:
            print(e)
        else:
            await session.refresh(messages)
            return cls.inDBSchemas(**messages.__dict__)