from datetime import datetime

from pydantic import BaseModel, Field


class TelegramMessageSchema(BaseModel):
    created_at: datetime = Field(default=datetime.now())
    forWhom: str = Field(default="_")
    countMessageAdmin: int = Field(ge=1)
    message: str = Field(default="_")


class TelegramMessageInDBSchema(TelegramMessageSchema):
    id: int = Field(ge=1)
