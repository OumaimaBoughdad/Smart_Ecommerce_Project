# CI/CD and Kubernetes Deployment Guide

## Local Deployment with Minikube

To deploy your application to your local Minikube cluster:

1. Make sure Minikube is installed and running:
   ```
   minikube status
   ```

2. Run the deployment script:
   ```
   .\deploy-local.ps1
   ```

   This script will:
   - Check if Minikube is running and start it if needed
   - Apply the Kubernetes configurations
   - Show the status of your pods and services

3. Access your services:
   ```
   minikube service ml-model-service --url
   ```

## GitHub Actions CI/CD Pipeline

The GitHub Actions workflow is configured to:

1. Build Docker images for your components
2. Push them to Docker Hub
3. Deploy to a Kubernetes cluster (if configured)

### Setting Up GitHub Actions

1. Push your code to GitHub:
   ```
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. Add required secrets to your GitHub repository:
   - `DOCKER_HUB_USERNAME`: Your Docker Hub username
   - `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub access token

3. For remote Kubernetes deployment, add:
   - `KUBE_CONFIG`: Base64-encoded Kubernetes config

### Manually Triggering the Workflow

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select "CI/CD Pipeline"
4. Click "Run workflow"

## Troubleshooting

### Minikube Issues

- If Minikube fails to start, try:
  ```
  minikube delete
  minikube start
  ```

- For Docker image issues:
  ```
  minikube image ls
  ```

### GitHub Actions Issues

- Check the workflow logs in the GitHub Actions tab
- Verify your secrets are correctly set
- For Docker Hub authentication issues, regenerate your access token