from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class Incident:
    namespace: str
    pod_name: str
    container_name: str
    reason: str
    message: str
    restart_count: int
    image: str
    node_name: Optional[str]
    logs: str
    events: str
    metrics: str
    detected_at: datetime

    @property
    def fingerprint(self) -> str:
        return f"{self.namespace}:{self.pod_name}:{self.container_name}:{self.reason}:{self.restart_count}"

    @classmethod
    def now(
        cls,
        namespace: str,
        pod_name: str,
        container_name: str,
        reason: str,
        message: str,
        restart_count: int,
        image: str,
        node_name: Optional[str],
        logs: str,
        events: str,
        metrics: str,
    ) -> "Incident":
        return cls(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
            reason=reason,
            message=message,
            restart_count=restart_count,
            image=image,
            node_name=node_name,
            logs=logs,
            events=events,
            metrics=metrics,
            detected_at=datetime.now(timezone.utc),
        )
