from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int = Field()

    last_name: str = Field()
    first_name: str = Field()
    middle_name: str = Field()
    lnr: str = Field()
    phone: str
    is_block: bool = Field(default=False)
    quotation_number: str = Field()

    created_at: datetime = Field()
    updated_at: datetime = Field()
    groups_id: int = Field(default=1)


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)
