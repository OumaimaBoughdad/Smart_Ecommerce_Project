# Build the fixed ML model image
docker build -t oumaimaboughdad/ecommerce_ml:fixed -f Dockerfile.ml-model .

# Push the image to Docker Hub (uncomment if you want to push)
# docker push oumaimaboughdad/ecommerce_ml:fixed

# Apply the fixed ConfigMap with sample data
kubectl apply -f k8s/fixed-csv-configmap.yaml

# Apply the fixed ML model deployment
kubectl apply -f k8s/ml-model-deployment-fixed-image.yaml

# Delete the existing pod to force recreation with the new image
kubectl delete pod -l app=ml-model

# Wait for the new pod to be ready
Start-Sleep -Seconds 5
kubectl get pods