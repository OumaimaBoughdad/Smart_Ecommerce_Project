import pandas as pd
import joblib

# Load the model
model = joblib.load('./output/product_scoring_model.joblib')
print("Model loaded successfully")

# Load the top products
top_products = pd.read_csv('./output/top_produits_attractifs.csv')
print(f"Top products loaded: {len(top_products)} rows")
print(top_products.head())