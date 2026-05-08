import requests

from app.config import settings
from app.incident import Incident


def send_slack_alert(incident: Incident, analysis: str) -> None:
    if not settings.slack_webhook_url:
        return

    text = (
        f"*Kubernetes Incident Detected*\n"
        f"*Pod:* `{incident.namespace}/{incident.pod_name}`\n"
        f"*Container:* `{incident.container_name}`\n"
        f"*Reason:* `{incident.reason}`\n\n"
        f"{analysis}"
    )

    response = requests.post(
        settings.slack_webhook_url,
        json={"text": text},
        timeout=10,
    )
    response.raise_for_status()

