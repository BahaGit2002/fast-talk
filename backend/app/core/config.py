from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Конфигурация приложения из переменных окружения"""

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # File Storage
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_AUDIO_FORMATS: str = "mp3,wav,ogg,m4a,webm"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # App
    ENVIRONMENT: str = "development"
    APP_NAME: str = "FastTalk"
    API_V1_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def allowed_audio_formats_list(self) -> List[str]:
        return [fmt.strip() for fmt in self.ALLOWED_AUDIO_FORMATS.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


settings = Settings()