.PHONY: setup cluster deploy-broken deploy-demo install-observability prometheus-port-forward grafana-port-forward loki-port-forward run run-dry docker-build helm-lint helm-template helm-install

setup:
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

cluster:
	kind create cluster --name aiops

deploy-broken:
	kubectl apply -f kubernetes/namespace.yaml
	kubectl apply -f kubernetes/broken-app.yaml

deploy-demo:
	kubectl apply -f kubernetes/namespace.yaml
	kubectl apply -f kubernetes/healthy-apps.yaml
	kubectl apply -f kubernetes/broken-app.yaml

install-observability:
	./scripts/install-observability.sh

prometheus-port-forward:
	kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090

grafana-port-forward:
	kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

loki-port-forward:
	kubectl port-forward -n monitoring svc/loki 3100:3100

run:
	cd backend && ./venv/bin/python -m app.main

run-dry:
	cd backend && DRY_RUN=true WATCH_NAMESPACE=aiops ./venv/bin/python -m app.main

docker-build:
	docker build -t mfzs/k8s-aiops-investigator:local backend

helm-lint:
	helm lint helm/k8s-aiops-investigator

helm-template:
	helm template investigator helm/k8s-aiops-investigator --namespace aiops

helm-install:
	helm upgrade --install investigator helm/k8s-aiops-investigator --namespace aiops --create-namespace
