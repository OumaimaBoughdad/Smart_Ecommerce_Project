#!/bin/bash
# deploy.sh

echo "Deploying E-commerce ML Application to Kubernetes..."

# Apply PVC
echo "Applying PVC..."
kubectl apply -f k8s/pvc.yaml

# Apply ConfigMap
echo "Applying ConfigMap with product data..."
kubectl apply -f k8s/optimized-csv-configmap.yaml

# Apply ML model deployment
echo "Deploying ML model..."
kubectl apply -f k8s/ml-model-deployment-latest.yaml

# Check deployment status
echo "Checking deployment status..."
kubectl get pods

echo "Deployment complete! Waiting for pods to be ready..."
sleep 5
kubectl get pods