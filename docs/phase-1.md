# Phase 1 MVP

Phase 1 detects unhealthy Kubernetes pods, collects recent pod logs and events, asks an LLM for a root-cause summary, and optionally sends the result to Slack.

## Flow

```text
Kubernetes API -> Pod Watcher -> Logs + Events -> AI Analyzer -> Slack Alert
```

## Scope

- Detect `CrashLoopBackOff`, image pull errors, container config errors, and non-zero terminations.
- Fetch recent pod logs and Kubernetes events.
- Generate a structured incident summary.
- Avoid repeated alerts for the same pod/container/restart fingerprint.

## Local Run

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
DRY_RUN=true python -m app.main
```

`DRY_RUN=true` skips the OpenAI call and returns a deterministic fallback analysis, which is useful while testing cluster access.

