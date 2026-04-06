from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
from pathlib import Path

# Resolves to .../backend/ regardless of where the app is run from
_APP_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "MRI Diagnostic Suite"
    API_VERSION: str = "v1"
    MODEL_PATH: str = str(_APP_ROOT / "models")
    RESEARCH_PATH: str = str(_APP_ROOT / "research")
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
