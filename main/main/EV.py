
from pydantic import BaseSettings

class EV(BaseSettings):
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PID_RANDRAGE: int
    class Config:
        env_file =".env"

settings = EV()