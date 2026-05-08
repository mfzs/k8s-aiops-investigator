# Observability Stack

Phase 2 adds Prometheus, Grafana, and Loki for incident context.

## Install

```bash
make install-observability
```

This installs:

- `kube-prometheus-stack`
- Grafana
- kube-state-metrics
- Loki stack

## Port Forward

Run each command in a separate terminal when needed:

```bash
make prometheus-port-forward
make grafana-port-forward
make loki-port-forward
```

Then set:

```env
PROMETHEUS_URL=http://localhost:9090
LOKI_URL=http://localhost:3100
```

## Grafana Login

Get the generated admin password:

```bash
kubectl get secret -n monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

Open Grafana at:

```text
http://localhost:3000
```

Username:

```text
admin
```
