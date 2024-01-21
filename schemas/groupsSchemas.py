from pydantic import Field, BaseModel


class GroupsSchemas(BaseModel):
    name: str = Field()


class GroupsInDBSchema(GroupsSchemas):
    id: int = Field(ge=1)
