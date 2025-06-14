# build-and-deploy-all.ps1
Write-Host "Building and deploying all components..."

# Build and push ML model image
Write-Host "Building and pushing ML model image..."
Set-Location -Path ".\Analyse-et-s-lection-des-Top-K-produits"
docker build -t oumaimaboughdad/ecommerce_ml:latest .
docker push oumaimaboughdad/ecommerce_ml:latest
Set-Location -Path ".."

# Build and push MCP server image
Write-Host "Building and pushing MCP server image..."
Set-Location -Path ".\Architecture_responsable_avec_Model_Context_Protocol-"
docker build -t oumaimaboughdad/ecommerce_mcp:latest .
docker push oumaimaboughdad/ecommerce_mcp:latest
Set-Location -Path ".."

# Deploy to Kubernetes
Write-Host "Deploying to Kubernetes..."
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/optimized-csv-configmap.yaml
kubectl apply -f k8s/ml-model-deployment-latest.yaml
kubectl apply -f k8s/mcp-deployment.yaml

# Check deployment status
Write-Host "Checking deployment status..."
kubectl get pods

Write-Host "Deployment complete! Waiting for pods to be ready..."
Start-Sleep -Seconds 10
kubectl get pods