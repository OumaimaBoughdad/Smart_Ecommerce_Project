# E-commerce ML Application - DevOps Guide

This guide explains how to deploy and manage the E-commerce ML application using DevOps practices.

## Components

1. **ML Model Service**: Analyzes product data and generates rankings
2. **MCP Server**: Implements Model Context Protocol for responsible AI
3. **Shared Data Volume**: Stores product data and model outputs

## Deployment Instructions

### Prerequisites

- Docker installed
- Kubernetes cluster (Minikube for local development)
- kubectl configured

### Quick Deployment

Run the comprehensive deployment script:

```powershell
# PowerShell
.\build-and-deploy-all.ps1
```

### Manual Deployment Steps

1. **Build and push Docker images**:

```bash
# ML Model
cd Analyse-et-s-lection-des-Top-K-produits
docker build -t oumaimaboughdad/ecommerce_ml:latest .
docker push oumaimaboughdad/ecommerce_ml:latest

# MCP Server
cd ../Architecture_responsable_avec_Model_Context_Protocol-
docker build -t oumaimaboughdad/ecommerce_mcp:latest .
docker push oumaimaboughdad/ecommerce_mcp:latest
```

2. **Deploy to Kubernetes**:

```bash
# Apply PVC
kubectl apply -f k8s/pvc.yaml

# Apply ConfigMap with product data
kubectl apply -f k8s/optimized-csv-configmap.yaml

# Deploy ML model
kubectl apply -f k8s/ml-model-deployment-latest.yaml

# Deploy MCP server
kubectl apply -f k8s/mcp-deployment.yaml
```

## Monitoring

Check the status of your deployments:

```bash
kubectl get pods
kubectl get services
```

View logs:

```bash
# ML Model logs
kubectl logs -l app=ml-model

# MCP Server logs
kubectl logs -l app=mcp-server
```

## Troubleshooting

If pods are not starting:

1. Check pod status: `kubectl describe pod <pod-name>`
2. Check logs: `kubectl logs <pod-name>`
3. Verify ConfigMap: `kubectl get configmap produits-scrapy-csv -o yaml`
4. Check PVC: `kubectl get pvc ecommerce-data-pvc`

## Scaling

To scale the ML model deployment:

```bash
kubectl scale deployment ml-model --replicas=3
```

## Cleanup

To remove all deployments:

```bash
kubectl delete deployment ml-model mcp-server
kubectl delete service ml-model-service mcp-service
kubectl delete configmap produits-scrapy-csv
kubectl delete pvc ecommerce-data-pvc
```