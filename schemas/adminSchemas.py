from datetime import datetime

from pydantic import BaseModel, Field


class AdminSchema(BaseModel):
    admin_id: int = Field(ge=1)
    last_name: str
    first_name: str
    middle_name: str


class AdminInDBSchema(AdminSchema):
    id: int = Field(ge=1)
