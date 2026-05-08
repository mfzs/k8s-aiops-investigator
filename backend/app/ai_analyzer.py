from openai import APIError, OpenAI, OpenAIError, RateLimitError

from app.config import settings
from app.incident import Incident
from app.prompts import build_prompt


def analyze_incident(incident: Incident) -> str:
    if settings.dry_run:
        return _fallback_analysis(incident, "DRY_RUN is enabled.")

    if not settings.openai_api_key:
        return _fallback_analysis(incident, "OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=settings.openai_api_key)
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a precise Kubernetes SRE assistant."},
                {"role": "user", "content": build_prompt(incident)},
            ],
            temperature=0.2,
        )
    except RateLimitError as exc:
        return _fallback_analysis(
            incident,
            f"OpenAI rate limit or quota error: {exc.message}",
        )
    except APIError as exc:
        return _fallback_analysis(
            incident,
            f"OpenAI API error: {exc.message}",
        )
    except OpenAIError as exc:
        return _fallback_analysis(
            incident,
            f"OpenAI client error: {exc}",
        )

    return response.choices[0].message.content or _fallback_analysis(
        incident,
        "The AI provider returned an empty response.",
    )


def _fallback_analysis(incident: Incident, note: str) -> str:
    return f"""
Root Cause:
Pod {incident.namespace}/{incident.pod_name} has container {incident.container_name} in {incident.reason}.

Severity:
Medium. The workload is not healthy and may be unavailable.

Suggested Fix:
Inspect the container command, image, configuration, secrets, and recent pod events. Start with:
kubectl describe pod {incident.pod_name} -n {incident.namespace}
kubectl logs {incident.pod_name} -n {incident.namespace} -c {incident.container_name}

Prevention:
Add startup validation, health probes, resource limits, and CI checks for Kubernetes manifests.

Useful Commands:
kubectl get pods -n {incident.namespace}
kubectl describe pod {incident.pod_name} -n {incident.namespace}

Note:
{note}
""".strip()
