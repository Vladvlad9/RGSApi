from datetime import datetime

from pydantic import Field, BaseModel


class DialogSchemas(BaseModel):
    user_id: int = Field()
    admin_id: int = Field(default=0)
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    who_closed: str = Field(default="None")
    gradeUser: int = Field(default=1)

    gradeAdmin: int = Field(default=1)
    chat_name: str = Field(default=None)

    dialogue_time: float = Field()
    reaction_time: float = Field()

    sales_channel_id: int = Field(default=1)


class DialogInDBSchema(DialogSchemas):
    id: int = Field(ge=1)
    