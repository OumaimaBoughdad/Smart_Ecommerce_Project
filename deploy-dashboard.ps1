# deploy-dashboard.ps1
# Script to deploy the dashboard to Minikube

# Check if Minikube is running
Write-Host "Checking Minikube status..."
$status = minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..."
    minikube start
}

# Apply Kubernetes configurations
Write-Host "Deploying dashboard to Minikube..."
kubectl apply -f k8s/dashboard-deployment.yaml
kubectl apply -f k8s/dashboard-service.yaml

# Check deployment status
Write-Host "Checking deployment status..."
kubectl get pods -l app=dashboard

# Show service information
Write-Host "Service information:"
kubectl get service dashboard-service

# Instructions for accessing the dashboard
Write-Host "`nTo access the dashboard, run:"
Write-Host "minikube service dashboard-service"