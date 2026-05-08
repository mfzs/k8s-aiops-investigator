import logging
from typing import Dict, Set

from fastapi import FastAPI

from app.ai_analyzer import analyze_incident
from app.slack_notifier import send_slack_alert
from app.watcher import watch_incidents


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
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
        logger.info("analysis for %s/%s:\n%s", incident.namespace, incident.pod_name, analysis)
        send_slack_alert(incident, analysis)


if __name__ == "__main__":
    main()
