# ZenML MLOps Pipeline for Smart eCommerce

This guide explains how to set up and run the ZenML MLOps pipeline for the Smart eCommerce project.

## Overview

ZenML is a lightweight MLOps framework that helps standardize ML workflows. We're using it as an alternative to Kubeflow for our product scoring pipeline.

## Prerequisites

- Python 3.9+
- Docker installed
- Git repository set up

## Setup Instructions

### 1. Install ZenML and Dependencies

```bash
pip install -r requirements-zenml.txt
```

### 2. Initialize ZenML

```bash
# Initialize ZenML
zenml init

# Run the setup script
python zenml_setup.py
```

### 3. Run the Pipeline

```bash
# Run the pipeline
python zenml_pipeline.py
```

### 4. View Pipeline Results

```bash
# List pipelines
zenml pipeline list

# Get the latest run
zenml pipeline runs list product_scoring_pipeline

# View artifacts
zenml artifact list
```

### 5. Visualize in the Dashboard

```bash
# Start the ZenML dashboard
zenml up

# Access the dashboard at http://127.0.0.1:8237
```

## Pipeline Structure

The ZenML pipeline consists of four main steps:

1. **preprocess_data**: Loads and cleans the raw product data
2. **normalize_features**: Normalizes features and calculates the global score
3. **train_model**: Trains a Random Forest model to predict product scores
4. **save_results**: Saves the model and top-K products

## Docker Integration

The pipeline uses Docker for containerization. Each step runs in its own container, ensuring reproducibility and isolation.

## Extending the Pipeline

To add more steps to the pipeline:

1. Define new steps using the `@step` decorator
2. Add the steps to the pipeline function
3. Update dependencies in `requirements-zenml.txt` if needed

## Troubleshooting

- **Docker issues**: Ensure Docker is running and you have sufficient permissions
- **Import errors**: Check that all dependencies are installed
- **Pipeline failures**: Check logs with `zenml pipeline runs get <run_id>`

## Next Steps

1. Add model versioning with ZenML's model registry
2. Set up experiment tracking with MLflow integration
3. Configure automated deployment with ZenML's deployment integrations