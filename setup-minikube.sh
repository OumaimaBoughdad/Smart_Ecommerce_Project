#!/bin/bash

# Start Minikube with Docker driver
echo "Starting Minikube with Docker driver..."
minikube start --driver=docker

# Enable Minikube addons
echo "Enabling Minikube addons..."
minikube addons enable storage-provisioner
minikube addons enable dashboard

# Install Kubeflow Pipelines
echo "Installing Kubeflow Pipelines..."
export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"

# Wait for Kubeflow to be ready
echo "Waiting for Kubeflow Pipelines to be ready..."
kubectl wait --for=condition=ready pod --all -n kubeflow --timeout=300s

# Create PVC for data sharing
echo "Creating PVC for data sharing..."
kubectl apply -f k8s/pvc.yaml

# Set Docker Hub username for deployments
echo "Please enter your Docker Hub username:"
read DOCKER_HUB_USERNAME
export DOCKER_HUB_USERNAME=$DOCKER_HUB_USERNAME

# Apply Kubernetes manifests with variable substitution
echo "Deploying applications to Kubernetes..."
envsubst < k8s/ml-model-deployment.yaml | kubectl apply -f -
envsubst < k8s/dashboard-deployment.yaml | kubectl apply -f -

# Get service URLs
echo "Getting service URLs..."
echo "Dashboard URL: $(minikube service dashboard-service --url)"
echo "Kubeflow Pipelines URL: $(minikube service -n kubeflow ml-pipeline-ui --url)"

echo "Setup complete!"