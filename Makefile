.PHONY: setup cluster deploy-broken deploy-demo run run-dry docker-build

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

run:
	cd backend && ./venv/bin/python -m app.main

run-dry:
	cd backend && DRY_RUN=true WATCH_NAMESPACE=aiops ./venv/bin/python -m app.main

docker-build:
	docker build -t k8s-aiops-investigator:local backend
