from datetime import datetime

from pydantic import BaseModel, Field


class AdminSchema(BaseModel):
    admin_id: int = Field(ge=1)


class AdminInDBSchema(AdminSchema):
    id: int = Field(ge=1)
