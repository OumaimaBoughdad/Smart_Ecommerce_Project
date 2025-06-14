# Top-K Products Selection

This repository contains the machine learning model for analyzing and selecting the top-K most attractive products from e-commerce data.

## Features

- Data preprocessing for e-commerce product data
- Product scoring algorithm based on multiple factors
- Machine learning model for predicting product attractiveness
- Export of top-K products for business decision making

## Usage

### Prerequisites

- Python 3.9+
- Required packages: pandas, numpy, scikit-learn, joblib

### Installation

```bash
pip install -r requirements.txt
```

### Running the Model

```bash
python model_training.py
```

Environment variables:
- `INPUT_FILE`: Path to the input CSV file (default: 'produits_scrapy.csv')
- `OUTPUT_DIR`: Directory for output files (default: './output')

### Docker

```bash
docker build -t ecommerce_ml .
docker run -v /path/to/data:/data ecommerce_ml
```

## Model Details

The model uses a Random Forest regressor to predict product attractiveness based on:
- Price (lower is better)
- Rating (higher is better)
- Availability (in stock is better)
- Estimated sales (higher is better)

## Output

- `product_scoring_model.joblib`: Trained model
- `top_produits_attractifs.csv`: Top-K most attractive products

## Deployment

To deploy this model to Kubernetes:

1. Build and push the Docker image:
```bash
docker build -t oumaimaboughdad/ecommerce_ml:latest .
docker push oumaimaboughdad/ecommerce_ml:latest
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f ../k8s/ml-model-deployment-latest.yaml
```