from datetime import datetime

from pydantic import BaseModel, Field


class TelegramMessageSchema(BaseModel):
    created_at: datetime = Field(default=datetime.now())
    forWhom: str = Field(default="Продавцы")
    countMessageAdmin: int = Field(ge=1)


class TelegramMessageInDBSchema(TelegramMessageSchema):
    id: int = Field(ge=1)
