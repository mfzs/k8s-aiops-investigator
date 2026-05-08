from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    slack_webhook_url: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")
    watch_namespace: Optional[str] = os.getenv("WATCH_NAMESPACE") or None
    log_tail_lines: int = int(os.getenv("LOG_TAIL_LINES", "200"))
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() in {"1", "true", "yes"}


settings = Settings()
