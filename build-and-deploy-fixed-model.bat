@echo off
echo Building fixed ML model Docker image...
cd Analyse-et-s-lection-des-Top-K-produits
docker build -t oumaimaboughdad/ecommerce_ml:fixed -f ../k8s/ml-model-fixed-dockerfile.yaml .

echo Pushing Docker image to Docker Hub...
docker push oumaimaboughdad/ecommerce_ml:fixed

echo Updating Kubernetes deployment...
cd ..
kubectl delete deployment ml-model
kubectl apply -f k8s/ml-model-deployment-fixed.yaml

echo Done!