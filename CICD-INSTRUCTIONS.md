# GitHub Actions CI/CD Pipeline Instructions

This project uses GitHub Actions for continuous integration and continuous deployment. The pipeline builds Docker images for the scraper, ML model, and dashboard components, and then deploys them to a Kubernetes cluster.

## How to Trigger the CI/CD Pipeline

### Automatic Triggers

The CI/CD pipeline is automatically triggered on:

1. **Push to main branch**: Any commits pushed to the `main` branch will trigger the pipeline.
2. **Pull Requests to main branch**: When a pull request is created targeting the `main` branch.

### Manual Trigger

You can also manually trigger the workflow:

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select "CI/CD Pipeline" from the list of workflows
4. Click the "Run workflow" button
5. Select the branch you want to run the workflow on
6. Click "Run workflow"

## Pipeline Steps

The CI/CD pipeline consists of three main jobs:

1. **Test**: Runs Python tests to ensure code quality
2. **Build and Push**: Builds Docker images and pushes them to Docker Hub
3. **Deploy**: Deploys the application to a Kubernetes cluster

## Required Secrets

Before running the pipeline, make sure to set up the following secrets in your GitHub repository:

1. `DOCKER_HUB_USERNAME`: Your Docker Hub username
2. `DOCKER_HUB_ACCESS_TOKEN`: Your Docker Hub access token
3. `KUBE_CONFIG`: Your Kubernetes configuration file (base64 encoded)

To add these secrets:
1. Go to your GitHub repository
2. Click on "Settings"
3. Click on "Secrets and variables" > "Actions"
4. Click "New repository secret"
5. Add each secret with its corresponding value

## Kubernetes Deployment

The pipeline deploys the following Kubernetes resources:
- ConfigMap with CSV data
- Persistent Volume Claim for data storage
- ML Model deployment
- Dashboard deployment

## Troubleshooting

If the pipeline fails, check:
1. GitHub Actions logs for detailed error messages
2. Docker Hub credentials
3. Kubernetes configuration and access
4. Resource availability in your Kubernetes cluster