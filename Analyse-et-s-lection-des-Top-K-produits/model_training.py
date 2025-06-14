import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

def preprocess_data(input_file):
    """Preprocess the data and return features and target."""
    print(f"Loading data from {input_file}")
    df = pd.read_csv(input_file)
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)
    
    # Create estimated sales based on rating and availability
    if 'note_moyenne' in df.columns and 'disponibilite' in df.columns:
        # Convert availability to numeric score
        dispo_map = {'En stock': 1.0, 'Rupture': 0.0}
        df['dispo_score'] = df['disponibilite'].map(lambda x: dispo_map.get(x, 0.5))
        
        # Simulate estimated sales
        df['ventes_estimees'] = np.random.poisson(
            df['note_moyenne'] * 10 * df['dispo_score'] + 1
        )
    
    # Normalize features
    features = ['prix', 'note_moyenne', 'ventes_estimees', 'dispo_score']
    available_features = [f for f in features if f in df.columns]
    
    scaler = MinMaxScaler()
    df[available_features] = scaler.fit_transform(df[available_features])
    
    # Invert price (lower is better)
    if 'prix' in df.columns:
        df['prix_inv'] = 1 - df['prix']
    
    # Calculate global score
    weights = {
        'note_moyenne': 0.4,
        'prix_inv': 0.3,
        'ventes_estimees': 0.2,
        'dispo_score': 0.1
    }
    
    df['score_global'] = sum(
        df[col] * weight for col, weight in weights.items() 
        if col in df.columns
    )
    
    # Prepare features and target
    X = df[available_features]
    y = df['score_global']
    
    return X, y, df

def train_model(X, y):
    """Train a Random Forest model to predict global score."""
    print("Training Random Forest model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Model R² score - Train: {train_score:.4f}, Test: {test_score:.4f}")
    
    return model

def save_results(model, df, output_dir):
    """Save model and top-K products."""
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

def main():
    input_file = os.environ.get('INPUT_FILE', 'produits_scrapy.csv')
    output_dir = os.environ.get('OUTPUT_DIR', './output')
    
    X, y, df = preprocess_data(input_file)
    model = train_model(X, y)
    save_results(model, df, output_dir)

if __name__ == "__main__":
    main()