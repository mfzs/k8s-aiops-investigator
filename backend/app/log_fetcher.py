from typing import Optional

from kubernetes.client.exceptions import ApiException

from app.config import settings
from app.kubernetes_client import core_v1


def fetch_logs(pod_name: str, namespace: str, container_name: Optional[str] = None) -> str:
    try:
        return core_v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            container=container_name,
            tail_lines=settings.log_tail_lines,
            timestamps=True,
        )
    except ApiException as exc:
        return f"Unable to fetch pod logs: {exc.status} {exc.reason}"


def fetch_events(pod_name: str, namespace: str) -> str:
    field_selector = f"involvedObject.name={pod_name},involvedObject.namespace={namespace}"

    try:
        events = core_v1.list_namespaced_event(
            namespace=namespace,
            field_selector=field_selector,
        )
    except ApiException as exc:
        return f"Unable to fetch pod events: {exc.status} {exc.reason}"

    if not events.items:
        return "No Kubernetes events found for this pod."

    lines = []
    for event in events.items[-20:]:
        event_time = event.last_timestamp or event.event_time or event.first_timestamp
        lines.append(
            f"{event_time} {event.type} {event.reason}: {event.message}"
        )

    return "\n".join(lines)
