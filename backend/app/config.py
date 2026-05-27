from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "k8s-aiops-investigator")
    app_env: str = os.getenv("APP_ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "json")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    slack_webhook_url: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")
    prometheus_url: Optional[str] = os.getenv("PROMETHEUS_URL") or None
    loki_url: Optional[str] = os.getenv("LOKI_URL") or None
    watch_namespace: Optional[str] = os.getenv("WATCH_NAMESPACE") or None
    log_tail_lines: int = int(os.getenv("LOG_TAIL_LINES", "200"))
    metrics_lookback: str = os.getenv("METRICS_LOOKBACK", "5m")
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() in {"1", "true", "yes"}


settings = Settings()
