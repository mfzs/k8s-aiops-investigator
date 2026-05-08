from typing import Any, Dict, List

import requests

from app.config import settings


def fetch_metrics(pod_name: str, namespace: str, container_name: str) -> str:
    if not settings.prometheus_url:
        return "Prometheus is not configured. Set PROMETHEUS_URL to include metric correlation."

    queries = {
        "restart_count": (
            "kube_pod_container_status_restarts_total"
            f'{{namespace="{namespace}",pod="{pod_name}",container="{container_name}"}}'
        ),
        "cpu_rate": (
            f'rate(container_cpu_usage_seconds_total'
            f'{{namespace="{namespace}",pod="{pod_name}",container="{container_name}"}}'
            f'[{settings.metrics_lookback}])'
        ),
        "memory_working_set_bytes": (
            "container_memory_working_set_bytes"
            f'{{namespace="{namespace}",pod="{pod_name}",container="{container_name}"}}'
        ),
        "last_terminated_reason": (
            "kube_pod_container_status_last_terminated_reason"
            f'{{namespace="{namespace}",pod="{pod_name}",container="{container_name}"}}'
        ),
    }

    lines: List[str] = []
    for label, query in queries.items():
        result = _query_prometheus(query)
        lines.append(f"{label}: {result}")

    return "\n".join(lines)


def _query_prometheus(query: str) -> str:
    try:
        response = requests.get(
            f"{settings.prometheus_url.rstrip('/')}/api/v1/query",
            params={"query": query},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"unavailable ({exc})"

    payload: Dict[str, Any] = response.json()
    if payload.get("status") != "success":
        return f"query failed ({payload.get('error', 'unknown error')})"

    results = payload.get("data", {}).get("result", [])
    if not results:
        return "no data"

    formatted = []
    for item in results[:5]:
        metric = item.get("metric", {})
        value = item.get("value", ["", ""])[1]
        reason = metric.get("reason")
        if reason:
            formatted.append(f"{reason}={value}")
        else:
            formatted.append(str(value))

    return ", ".join(formatted)
