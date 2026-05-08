from app.incident import Incident


def build_prompt(incident: Incident) -> str:
    return f"""
You are a senior Kubernetes SRE investigating a production incident.

Analyze the incident context and respond in this exact structure:

Root Cause:

Severity:

Suggested Fix:

Prevention:

Useful Commands:

Incident Context:
- Detected At: {incident.detected_at.isoformat()}
- Namespace: {incident.namespace}
- Pod: {incident.pod_name}
- Container: {incident.container_name}
- Image: {incident.image}
- Node: {incident.node_name or "unknown"}
- Reason: {incident.reason}
- Message: {incident.message or "none"}
- Restart Count: {incident.restart_count}

Recent Logs:
---
{incident.logs or "No logs returned."}
---

Recent Kubernetes Events:
---
{incident.events or "No events returned."}
---
""".strip()

