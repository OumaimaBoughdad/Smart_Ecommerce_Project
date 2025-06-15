# deploy-local.ps1
# Script to deploy the application to local Minikube cluster

# Check if Minikube is running
Write-Host "Checking Minikube status..."
$status = minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..."
    minikube start
}

# Apply Kubernetes configurations
Write-Host "Deploying to Minikube..."
kubectl apply -f k8s/csv-configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/ml-model-deployment-fixed-image.yaml
kubectl apply -f k8s/dashboard-deployment.yaml

# Check deployment status
Write-Host "Checking deployment status..."
kubectl get pods

# Show service information
Write-Host "Service information:"
kubectl get services

# Instructions for accessing the services
Write-Host "`nTo access the services, run:"
Write-Host "minikube service ml-model-service --url"
Write-Host "minikube service dashboard-service --url (if available)"