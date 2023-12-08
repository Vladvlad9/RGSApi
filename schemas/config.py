from pydantic import BaseModel


class BotSchema(BaseModel):
    TOKEN: str
    NGROK_TUNEL_URL: str
    ADMINS: list[int]


class ConfigSchema(BaseModel):
    BOT: BotSchema
    DATABASE: str
