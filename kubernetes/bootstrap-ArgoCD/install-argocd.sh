#!/usr/bin/env bash
set -euo pipefail

ARGOCD_VERSION="10.2.0"

helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

helm upgrade --install argocd argo/argo-cd \
    --namespace argocd \
    --create-namespace \
    --version "${ARGOCD_VERSION}" \
    -f ./values.yaml