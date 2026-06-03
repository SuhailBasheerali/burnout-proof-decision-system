from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_title: str = "Burnout-Proof Decision Engine"
    google_gemini_api_key: str | None = os.getenv("GOOGLE_GEMINI_API_KEY")
    gemini_model: str = "gemini-2.5-flash"
    gemini_max_output_tokens: int = 1500
    gemini_temperature: float = 0.7
    ai_cache_dir: Path = BASE_DIR / ".ai_cache"
    ai_cache_expiry_hours: int = 24
    max_gemini_calls_per_day: int = 100

    @property
    def rate_limit_path(self) -> Path:
        return self.ai_cache_dir / "rate_limit.json"


settings = Settings()
