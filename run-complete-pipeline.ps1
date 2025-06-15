# run-complete-pipeline.ps1
# Script to run the complete pipeline: ML model job followed by dashboard

# Check if Minikube is running
Write-Host "Checking Minikube status..."
$status = minikube status
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..."
    minikube start
}

# Apply ConfigMap and PVC
Write-Host "Setting up ConfigMap and PVC..."
kubectl apply -f k8s/csv-configmap.yaml
kubectl apply -f k8s/pvc.yaml

# Deploy ML model as a job
Write-Host "Deploying ML model job..."
kubectl apply -f k8s/ml-model-job.yaml

# Wait for ML model job to complete
Write-Host "Waiting for ML model job to complete..."
$jobStatus = ""
while ($jobStatus -ne "Complete") {
    Start-Sleep -Seconds 5
    $jobStatus = kubectl get job ml-model-job -o jsonpath='{.status.conditions[?(@.type=="Complete")].type}'
    if ($jobStatus -ne "Complete") {
        Write-Host "ML model job still running..."
    }
}

Write-Host "ML model job completed successfully!"

# Deploy dashboard
Write-Host "Deploying dashboard..."
kubectl apply -f k8s/dashboard-deployment.yaml
kubectl apply -f k8s/dashboard-service.yaml

# Check deployment status
Write-Host "Checking deployment status..."
kubectl get pods

# Show service information
Write-Host "Service information:"
kubectl get services

# Instructions for accessing the dashboard
Write-Host "`nTo access the dashboard, run:"
Write-Host "minikube service dashboard-service"