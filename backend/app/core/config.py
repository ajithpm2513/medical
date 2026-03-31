from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "MRI Diagnostic Suite"
    API_VERSION: str = "v1"
    MODEL_PATH: str = "/home/user/medical/backend/models"
    RESEARCH_PATH: str = "/home/user/medical/backend/research"
    DEBUG: bool = True
    GROQ_API_KEY: Optional[str] = None
    CLASS_MAPPING: dict = {
        0: "Glioma",
        1: "Meningioma",
        2: "No Tumor",
        3: "Pituitary"
    }

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
