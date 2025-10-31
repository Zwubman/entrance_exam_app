from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    GOOGLE_API_KEY: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    UPLOADS_DIR: str = 'uploads/'
    CHUNK_LENGTH: int = 250

    class Config:
        env_file = '.env'

settings = Settings()