import logging
from typing import Dict, Set

from fastapi import FastAPI

from app.ai_analyzer import analyze_incident
from app.logging_config import configure_logging
from app.slack_notifier import send_slack_alert
from app.watcher import watch_incidents


configure_logging()
logger = logging.getLogger(__name__)

api = FastAPI(title="K8s AI Ops Investigator")


@api.get("/healthz")
def healthz() -> Dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    seen: Set[str] = set()

    for incident in watch_incidents():
        if incident.fingerprint in seen:
            continue

        seen.add(incident.fingerprint)
        analysis = analyze_incident(incident)
        logger.info(
            "incident analysis generated",
            extra={
                "namespace": incident.namespace,
                "pod": incident.pod_name,
                "container": incident.container_name,
                "reason": incident.reason,
                "restart_count": incident.restart_count,
            },
        )
        logger.info(analysis)
        send_slack_alert(incident, analysis)


if __name__ == "__main__":
    main()
