#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

MANIFESTS=(
  "k8s/db-secret.yaml"
  "k8s/db-deployment.yaml"
  "k8s/db-service.yaml"
  "k8s/app2-deployment.yaml"
  "k8s/app2-service.yaml"
  "k8s/app1-deployment.yaml"
  "k8s/app1-service.yaml"
)

for manifest in "${MANIFESTS[@]}"; do
  kubectl apply -f "$manifest"
done

if [[ "${USE_REGISTRY_IMAGES:-false}" == "true" ]]; then
  REGISTRY="${REGISTRY:-ghcr.io}"
  IMAGE_NAMESPACE="${IMAGE_NAMESPACE:-abderrahmanezaidi}"
  IMAGE_TAG="${IMAGE_TAG:-latest}"

  kubectl set image deployment/app1-frontend \
    app1-frontend="${REGISTRY}/${IMAGE_NAMESPACE}/app1-frontend:${IMAGE_TAG}"
  kubectl set image deployment/app2-api \
    app2-api="${REGISTRY}/${IMAGE_NAMESPACE}/app2-api:${IMAGE_TAG}"
fi

kubectl rollout status deployment/app2-api --timeout=120s
kubectl rollout status deployment/app1-frontend --timeout=120s
kubectl get pods

