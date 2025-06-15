# E-commerce Analytics Platform

This project deploys a complete e-commerce analytics platform using Kubernetes, consisting of three main components:

1. **Web Scraper** - Collects product data from various e-commerce websites
2. **ML Model** - Processes the collected data and generates insights
3. **Dashboard** - Visualizes the insights for business users

## Architecture

The system uses Kubernetes Jobs for one-time tasks (scraper and ML model) and a Deployment for the long-running dashboard service.

## Components

- **PersistentVolumeClaim (PVC)**: Shared storage for all components
- **ConfigMap**: Contains sample product data
- **Scraper Job**: Collects product data from websites
- **ML Model Job**: Processes data and generates insights
- **Dashboard Deployment**: Visualizes insights for users

## How to Deploy

Apply the complete solution:

```bash
kubectl apply -f k8s/complete-solution.yaml
```

Or deploy components individually:

```bash
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/fixed-csv-configmap.yaml
kubectl apply -f k8s/scraper-job.yaml
kubectl apply -f k8s/ml-model-job.yaml
kubectl apply -f k8s/dashboard-deployment.yaml
```

## Accessing the Dashboard

The dashboard is exposed as a NodePort service. Access it at:

```
http://<node-ip>:<node-port>
```

Find the node port with:

```bash
kubectl get svc dashboard-service
```

## Troubleshooting

If pods show CrashLoopBackOff:
- For scraper and ML model: This is expected as they're designed to run once and complete. Use Jobs instead of Deployments.
- For dashboard: Check logs with `kubectl logs deployment/dashboard`