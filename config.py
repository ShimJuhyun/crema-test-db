import os
from pydantic_settings import BaseSettings

env_mode = os.getenv("APP_ENV", "development")

class Settings(BaseSettings):
    DB_USER: str
    DB_PW: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    class Config:
        env_file = ".env.production" if env_mode == "production" else ".env.local"
        extra = "allow"
        case_sensitive = True
        
settings = Settings()
