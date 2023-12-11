from pydantic import BaseModel


class AuthSchema(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str


class BotSchema(BaseModel):
    TOKEN: str
    NGROK_TUNEL_URL: str
    ADMINS: list[int]


class ConfigSchema(BaseModel):
    BOT: BotSchema
    AUTH: AuthSchema
    DATABASE: str
