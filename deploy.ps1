# deploy.ps1
Write-Host "Deploying E-commerce ML Application to Kubernetes..."

# Apply PVC
Write-Host "Applying PVC..."
kubectl apply -f k8s/pvc.yaml

# Apply ConfigMap
Write-Host "Applying ConfigMap with product data..."
kubectl apply -f k8s/optimized-csv-configmap.yaml

# Apply ML model deployment
Write-Host "Deploying ML model..."
kubectl apply -f k8s/ml-model-deployment-latest.yaml

# Check deployment status
Write-Host "Checking deployment status..."
kubectl get pods

Write-Host "Deployment complete! Waiting for pods to be ready..."
Start-Sleep -Seconds 5
kubectl get pods