# Observability Phase

This phase enriches Kubernetes incidents with metric context.

## Flow

```text
Kubernetes Watcher
  -> Pod Logs
  -> Kubernetes Events
  -> Prometheus Metrics
  -> AI Incident Analysis
  -> Slack Alert
```

## Prometheus Queries

The backend currently collects:

- container restart count
- container CPU usage rate
- container memory working set
- last terminated reason

If `PROMETHEUS_URL` is not set, the watcher still runs and includes a metrics-not-configured note.

## Demo

1. Deploy demo workloads:

```bash
make deploy-demo
```

2. Install observability:

```bash
make install-observability
```

3. Port-forward Prometheus:

```bash
make prometheus-port-forward
```

4. Run the watcher in another terminal:

```bash
make run
```

For quota-safe demos:

```bash
make run-dry
```
