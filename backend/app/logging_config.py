import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from app.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app": settings.app_name,
            "environment": settings.app_env,
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        for key in ("namespace", "pod", "container", "reason", "restart_count"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        return json.dumps(payload, separators=(",", ":"))


def configure_logging() -> None:
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler()

    if settings.log_format.lower() == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
