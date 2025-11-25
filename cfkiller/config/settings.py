# cfkiller/config/settings.py
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    target: str = "https://example.com"
    duration: int = 60
    mode: str = "rapid"
    connections: int = 80
    intensity: int = 1500
    proxy_file: Optional[Path] = None
    captcha_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()