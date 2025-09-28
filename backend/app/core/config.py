from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "YieldSync AI"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    REDIS_URL: str
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()
