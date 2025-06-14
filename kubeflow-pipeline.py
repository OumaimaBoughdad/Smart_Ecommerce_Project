import kfp
from kfp import dsl
from kfp.components import func_to_container_op

# Define component functions
@func_to_container_op
def preprocess_data(input_file: str, output_file: str):
    import pandas as pd
    import numpy as np
    
    # Load data
    df = pd.read_csv(input_file)
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)
    
    # Create availability score
    dispo_map = {'En stock': 1.0, 'Rupture': 0.0}
    df['dispo_score'] = df['disponibilite'].map(lambda x: dispo_map.get(x, 0.5))
    
    # Create estimated sales
    df['ventes_estimees'] = np.random.poisson(
        df['note_moyenne'] * 10 * df['dispo_score'] + 1
    )
    
    # Save preprocessed data
    df.to_csv(output_file, index=False)
    
    return output_file

@func_to_container_op
def train_model(input_file: str, model_file: str, top_k_file: str):
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    import joblib
    
    # Load preprocessed data
    df = pd.read_csv(input_file)
    
    # Normalize features
    features = ['prix', 'note_moyenne', 'ventes_estimees', 'dispo_score']
    available_features = [f for f in features if f in df.columns]
    
    scaler = MinMaxScaler()
    df[available_features] = scaler.fit_transform(df[available_features])
    
    # Invert price (lower is better)
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
    
    # Train model
    X = df[available_features]
    y = df['score_global']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, model_file)
    
    # Save top-K products
    top_k = 5
    top_products = df.sort_values('score_global', ascending=False).head(top_k)
    top_products.to_csv(top_k_file, index=False)
    
    return model_file, top_k_file

# Define pipeline
@dsl.pipeline(
    name='Product Scoring Pipeline',
    description='A pipeline to preprocess data and train a product scoring model'
)
def product_scoring_pipeline(
    input_file: str = 'produits_scrapy.csv'
):
    # Preprocess data
    preprocess_task = preprocess_data(input_file=input_file, output_file='preprocessed_data.csv')
    
    # Train model
    train_task = train_model(
        input_file=preprocess_task.output,
        model_file='product_scoring_model.joblib',
        top_k_file='top_produits_attractifs.csv'
    )
    train_task.after(preprocess_task)

# Compile pipeline
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(
        product_scoring_pipeline,
        'product_scoring_pipeline.yaml'
    )