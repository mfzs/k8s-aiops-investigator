# K8s AI Ops Investigator

AI-powered Kubernetes incident investigation and remediation platform with observability, automation, and intelligent root-cause analysis.

## Phase 1 MVP

The current implementation watches Kubernetes pods, detects common failure states, collects logs/events, generates an AI root-cause analysis, and optionally sends a Slack alert.

```text
Kubernetes Cluster
        |
        v
Pod Failure Watcher
        |
        v
Logs + Events Collector
        |
        v
AI Incident Analyzer
        |
        v
Slack Alert / Console Output
```

## Repository Structure

```text
backend/            Python incident investigator service
kubernetes/         Namespace, broken workload, and RBAC manifests
docs/               Project notes and implementation phases
monitoring/         Future Prometheus, Grafana, and Loki assets
```

## Quick Start

Install local Kubernetes tooling:

```bash
brew install kind kubectl helm
kind create cluster --name aiops
kubectl get nodes
```

Deploy the namespace and intentionally broken workload:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/healthy-apps.yaml
kubectl apply -f kubernetes/broken-app.yaml
kubectl get pods -n aiops
```

Run the investigator locally:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
cp .env.example .env
make run-dry
```

Set `OPENAI_API_KEY` and `SLACK_WEBHOOK_URL` in `.env` to enable AI analysis and Slack notifications.
Then run the real-token path from the repository root:

```bash
make run
```

## Docker

```bash
docker build -t k8s-aiops-investigator:local backend
```

## Make Targets

```bash
make setup
make cluster
make deploy-demo
make deploy-broken
make run
make run-dry
make docker-build
```

## Roadmap

Phase 1: Detect pod failures, fetch logs/events, generate AI summary, send Slack alerts.

Phase 2: Add Prometheus, Grafana, Loki, and metrics/log correlation.

Phase 3: Add Helm charts, CI/CD, RBAC hardening, persistence, and structured incident history.

Phase 4: Add runbook RAG, anomaly detection, remediation recommendations, and optional auto-remediation.

## Observability

Install Prometheus, Grafana, and Loki:

```bash
make install-observability
```

Expose Prometheus locally:

```bash
make prometheus-port-forward
```

Set `PROMETHEUS_URL=http://localhost:9090` in `.env` so incident analysis includes metric context.
