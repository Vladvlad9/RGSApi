from datetime import datetime

from pydantic import BaseModel, Field


class AdminWebSchema(BaseModel):
    email: str
    password: str


class AdminWebInDBSchema(AdminWebSchema):
    id: int = Field(ge=1)
