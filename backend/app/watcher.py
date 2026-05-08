from collections.abc import Iterator
import logging

from kubernetes import watch

from app.config import settings
from app.incident import Incident
from app.kubernetes_client import core_v1
from app.log_fetcher import fetch_events, fetch_logs


CRASH_REASONS = {
    "CrashLoopBackOff",
    "Error",
    "ImagePullBackOff",
    "ErrImagePull",
    "CreateContainerConfigError",
    "CreateContainerError",
    "RunContainerError",
}

logger = logging.getLogger(__name__)


def watch_incidents() -> Iterator[Incident]:
    watcher = watch.Watch()
    stream = _pod_stream(watcher)

    for event in stream:
        pod = event["object"]
        statuses = pod.status.container_statuses or []

        for container in statuses:
            waiting = container.state.waiting if container.state else None
            terminated = container.state.terminated if container.state else None
            reason = None
            message = ""

            if waiting and waiting.reason in CRASH_REASONS:
                reason = waiting.reason
                message = waiting.message or ""
            elif terminated and terminated.exit_code != 0:
                reason = terminated.reason or f"ExitCode{terminated.exit_code}"
                message = terminated.message or ""

            if not reason:
                continue

            namespace = pod.metadata.namespace
            pod_name = pod.metadata.name
            container_name = container.name

            logger.info("incident detected: %s/%s %s", namespace, pod_name, reason)

            yield Incident.now(
                namespace=namespace,
                pod_name=pod_name,
                container_name=container_name,
                reason=reason,
                message=message,
                restart_count=container.restart_count,
                image=container.image,
                node_name=pod.spec.node_name,
                logs=fetch_logs(pod_name, namespace, container_name),
                events=fetch_events(pod_name, namespace),
            )


def _pod_stream(watcher: watch.Watch):
    if settings.watch_namespace:
        return watcher.stream(
            core_v1.list_namespaced_pod,
            namespace=settings.watch_namespace,
            timeout_seconds=0,
        )

    return watcher.stream(core_v1.list_pod_for_all_namespaces, timeout_seconds=0)

