# deploy-ml-job.ps1
# Script to deploy the ML model as a job to Minikube

# Check if Minikube is running
Write-Host "Checking Minikube status..."
$status = minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..."
    minikube start
}

# Apply Kubernetes configurations
Write-Host "Deploying ML model job to Minikube..."
kubectl apply -f k8s/csv-configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/ml-model-job.yaml
kubectl apply -f k8s/ml-model-service.yaml

# Check job status
Write-Host "Checking job status..."
kubectl get jobs
kubectl get pods -l app=ml-model

# Instructions for viewing logs
Write-Host "`nTo view the logs of the ML model job, run:"
Write-Host "kubectl logs -l app=ml-model"