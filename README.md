# Project Phoenix — Day 1 Starter

GitOps Mastery · A small e-commerce app (frontend + product API) used throughout the course.

```
Browser ──► frontend (nginx, NodePort 30080) ──/api──► product-api (FastAPI, ClusterIP 8000)
```

| Folder | What it is |
|---|---|
| `backend/` | FastAPI product API, tests, Dockerfile |
| `frontend/` | Static store page served by nginx; proxies `/api` to the API |
| `k8s/` | Plain Kubernetes manifests (namespace, deployments, services) |
| `kind-config.yaml` | Local cluster that exposes the store on http://localhost:8080 |

> Day 1 keeps products in memory. The database, Kustomize overlays and Argo CD arrive on later days.
> On Day 2 these manifests move into the separate `phoenix-gitops` repository.

## Run it on kind (Windows: run inside WSL2 Ubuntu)

```bash
# 1. Create the cluster
kind create cluster --config kind-config.yaml

# 2. Build images
docker build -t phoenix-product-api:v1 ./backend
docker build -t phoenix-frontend:v1 ./frontend

# 3. Load images into the kind node (no registry needed)
kind load docker-image phoenix-product-api:v1 phoenix-frontend:v1 --name phoenix

# 4. Deploy
kubectl apply -f k8s/
kubectl -n phoenix get pods -w

# 5. Open http://localhost:8080
```

## Run the API tests

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

## Clean up

```bash
kind delete cluster --name phoenix
```
