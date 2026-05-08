#!/usr/bin/env bash
set -euo pipefail

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --wait

helm upgrade --install loki grafana/loki-stack \
  --namespace monitoring \
  --wait

echo "Observability stack installed in namespace: monitoring"
echo "Prometheus: make prometheus-port-forward"
echo "Grafana:    make grafana-port-forward"
echo "Loki:       make loki-port-forward"
