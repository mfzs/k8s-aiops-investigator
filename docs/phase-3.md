# Phase 3 Productionization

Phase 3 turns the investigator into something that can run as a production-style Kubernetes workload.

## Delivered

- Docker image builds as a non-root runtime user.
- Structured JSON logging for incident detection and analysis events.
- Helm chart for deployment, RBAC, ConfigMap, Secret references, and resource limits.
- GitHub Actions CI for backend compile checks, Helm lint/template, and Docker build.
- Make targets for local packaging and Helm validation.

## Runtime Secrets

Secrets are not stored in Helm values. Create them separately:

```bash
kubectl create secret generic k8s-aiops-investigator-secrets \
  --namespace aiops \
  --from-literal=OPENAI_API_KEY=<your-key> \
  --from-literal=SLACK_WEBHOOK_URL=<your-webhook>
```

For dry-run demos, secrets are optional:

```bash
helm upgrade --install investigator helm/k8s-aiops-investigator \
  --namespace aiops \
  --create-namespace \
  --set image.tag=local \
  --set config.dryRun=true
```

## Image

Build:

```bash
make docker-build
```

Push:

```bash
docker push mfzs/k8s-aiops-investigator:<tag>
```

## Validation

```bash
make helm-lint
make helm-template
```

