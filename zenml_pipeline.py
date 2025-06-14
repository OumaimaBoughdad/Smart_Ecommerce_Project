from zenml import pipeline, step
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# Note: Newer ZenML versions use different import patterns
try:
    # For newer ZenML versions
    from zenml.steps import Output
    NEWER_ZENML = True
except ImportError:
    # For older ZenML versions
    NEWER_ZENML = False

@step
def preprocess_data(input_file: str) -> pd.DataFrame:
    """Load and preprocess the data."""
    print(f"Loading data from {input_file}")
    
    # Try different CSV parsing options to handle the problematic file
    try:
        # First attempt with error handling for quoted fields
        df = pd.read_csv(input_file, error_bad_lines=False, warn_bad_lines=True, 
                         quoting=pd.io.common.csv.QUOTE_NONE, escapechar='\\')
    except:
        try:
            # Second attempt with different delimiter detection
            df = pd.read_csv(input_file, sep=None, engine='python')
        except:
            # Last resort - skip problematic rows
            df = pd.read_csv(input_file, on_bad_lines='skip')
    
    print(f"Successfully loaded {len(df)} rows")
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)
    
    # Create availability score
    if 'disponibilite' in df.columns:
        dispo_map = {'En stock': 1.0, 'Rupture': 0.0}
        df['dispo_score'] = df['disponibilite'].map(lambda x: dispo_map.get(x, 0.5))
    
    # Create estimated sales
    if 'note_moyenne' in df.columns and 'dispo_score' in df.columns:
        df['ventes_estimees'] = np.random.poisson(
            df['note_moyenne'] * 10 * df['dispo_score'] + 1
        )
    
    return df


##

@step
def normalize_features(df: pd.DataFrame) -> tuple:
    """Normalize features and calculate global score."""
    # Normalize features
    features = ['prix', 'note_moyenne', 'ventes_estimees', 'dispo_score']
    available_features = [f for f in features if f in df.columns]
    
    # Check if we have any features to normalize
    print(f"Available features: {available_features}")
    if not available_features:
        print("No features available for normalization. Creating dummy features.")
        # Create dummy features if none are available
        df['prix'] = 0.5
        df['note_moyenne'] = 0.5
        df['ventes_estimees'] = 0.5
        df['dispo_score'] = 0.5
        available_features = features
    
    # Ensure we have at least some data
    if len(df) == 0:
        print("DataFrame is empty. Creating dummy row.")
        df = pd.DataFrame({col: [0.5] for col in available_features})
    
    scaler = MinMaxScaler()
    df[available_features] = scaler.fit_transform(df[available_features])
    
    # Invert price (lower is better)
    if 'prix' in df.columns:
        df['prix_inv'] = 1 - df['prix']
    else:
        df['prix_inv'] = 0.5
    
    # Calculate global score
    weights = {
        'note_moyenne': 0.4,
        'prix_inv': 0.3,
        'ventes_estimees': 0.2,
        'dispo_score': 0.1
    }
    
    # Ensure all required columns exist
    for col in weights.keys():
        if col not in df.columns:
            df[col] = 0.5
    
    df['score_global'] = sum(
        df[col] * weight for col, weight in weights.items()
    )
    
    # Prepare features and target
    X = df[available_features]
    y = df['score_global']
    
    return X, y, df

@step
def train_model(X_y_df: tuple) -> tuple:
    """Train a Random Forest model to predict global score."""
    X, y, df = X_y_df
    print("Training Random Forest model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Model R² score - Train: {train_score:.4f}, Test: {test_score:.4f}")
    
    return model, df

@step
def save_results(model_df: tuple, output_dir: str) -> None:
    """Save model and top-K products."""
    model, df = model_df
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, 'product_scoring_model.joblib')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save top-K products
    top_k = 5
    top_products = df.sort_values('score_global', ascending=False).head(top_k)
    output_file = os.path.join(output_dir, 'top_produits_attractifs.csv')
    top_products.to_csv(output_file, index=False)
    print(f"Top {top_k} products saved to {output_file}")

@pipeline
def product_scoring_pipeline(input_file: str, output_dir: str):
    """Pipeline to preprocess data, train model and save results."""
    df = preprocess_data(input_file)
    X_y_df = normalize_features(df)
    model_df = train_model(X_y_df)
    save_results(model_df, output_dir)

if __name__ == "__main__":
    # Initialize ZenML
    from zenml.client import Client
    client = Client()
    
    # Run the pipeline
    product_scoring_pipeline(
    input_file="Analyse-et-s-lection-des-Top-K-produits/produits_scrapy.csv",
    output_dir="./output"
)