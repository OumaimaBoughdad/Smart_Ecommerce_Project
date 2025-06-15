import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Define paths
DATA_DIR = "/app/data"
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
MODEL_PATH = os.path.join(OUTPUT_DIR, "product_scoring_model.joblib")
TOP_PRODUCTS_PATH = os.path.join(OUTPUT_DIR, "top_produits_attractifs.csv")
SCRAPED_DATA_PATH = os.path.join(DATA_DIR, "produits_scrapy.csv")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
    }
    .card {
        border-radius: 5px;
        padding: 1.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def load_data():
    """Load the scraped product data"""
    try:
        if os.path.exists(SCRAPED_DATA_PATH):
            df = pd.read_csv(SCRAPED_DATA_PATH, sep=';')
            return df
        else:
            st.error(f"Data file not found at {SCRAPED_DATA_PATH}")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def load_top_products():
    """Load the top products identified by the ML model"""
    try:
        if os.path.exists(TOP_PRODUCTS_PATH):
            df = pd.read_csv(TOP_PRODUCTS_PATH)
            return df
        else:
            st.warning(f"Top products file not found at {TOP_PRODUCTS_PATH}")
            return None
    except Exception as e:
        st.error(f"Error loading top products: {e}")
        return None

def load_model():
    """Load the trained ML model"""
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            return model
        else:
            st.warning(f"Model file not found at {MODEL_PATH}")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def display_metrics(df):
    """Display key metrics about the dataset"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(df)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Products</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{df["categorie"].nunique()}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Categories</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        avg_price = df["prix"].mean()
        st.markdown(f'<div class="metric-value">${avg_price:.2f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Average Price</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        avg_rating = df["note_moyenne"].mean()
        st.markdown(f'<div class="metric-value">{avg_rating:.1f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Average Rating</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def plot_category_distribution(df):
    """Plot the distribution of products by category"""
    st.markdown('<div class="sub-header">Product Distribution by Category</div>', unsafe_allow_html=True)
    
    # Get top categories
    category_counts = df['categorie'].value_counts().head(10)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=category_counts.values, y=category_counts.index, palette='viridis', ax=ax)
    ax.set_title('Top 10 Categories by Product Count')
    ax.set_xlabel('Number of Products')
    ax.set_ylabel('Category')
    
    st.pyplot(fig)

def plot_price_distribution(df):
    """Plot the distribution of product prices"""
    st.markdown('<div class="sub-header">Price Distribution</div>', unsafe_allow_html=True)
    
    # Filter out extreme values for better visualization
    price_df = df[df['prix'] <= df['prix'].quantile(0.95)]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(price_df['prix'], kde=True, bins=30, ax=ax)
    ax.set_title('Price Distribution (excluding top 5% for better visualization)')
    ax.set_xlabel('Price')
    ax.set_ylabel('Count')
    
    st.pyplot(fig)

def plot_rating_vs_price(df):
    """Plot the relationship between ratings and prices"""
    st.markdown('<div class="sub-header">Rating vs Price</div>', unsafe_allow_html=True)
    
    # Filter out extreme values for better visualization
    plot_df = df[df['prix'] <= df['prix'].quantile(0.95)]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='prix', y='note_moyenne', data=plot_df, alpha=0.6, ax=ax)
    ax.set_title('Product Ratings vs Price')
    ax.set_xlabel('Price')
    ax.set_ylabel('Rating')
    
    st.pyplot(fig)

def display_top_products(top_df):
    """Display the top products identified by the ML model"""
    st.markdown('<div class="sub-header">Top Products by Attractiveness Score</div>', unsafe_allow_html=True)
    
    if top_df is not None:
        # Format the dataframe for display
        display_df = top_df.copy()
        if 'score_attractivite' in display_df.columns:
            display_df['score_attractivite'] = display_df['score_attractivite'].round(2)
        
        # Display as a table
        st.dataframe(
            display_df,
            column_config={
                "titre": "Product Name",
                "prix": st.column_config.NumberColumn("Price", format="$%.2f"),
                "note_moyenne": st.column_config.NumberColumn("Rating", format="%.1f"),
                "score_attractivite": st.column_config.NumberColumn("Attractiveness Score", format="%.2f"),
                "categorie": "Category"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No top products data available. Please run the ML model first.")

def display_chat_interface():
    """Display a simple chat interface for product recommendations"""
    st.markdown('<div class="sub-header">Product Recommendation Assistant</div>', unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I can help you find products based on your preferences. What kind of products are you looking for?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"**{message['role'].title()}**: {message['content']}")
    
    # Chat input
    if prompt := st.text_input("Your question:", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Simple response logic based on keywords
        response = generate_recommendation(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display the new messages
        st.rerun()

def generate_recommendation(prompt):
    """Generate a simple product recommendation based on user input"""
    prompt_lower = prompt.lower()
    
    # Load data for recommendations
    df = load_data()
    if df is None:
        return "I'm sorry, I can't access the product database at the moment."
    
    # Simple keyword matching
    if "laptop" in prompt_lower or "computer" in prompt_lower:
        products = df[df['categorie'].str.contains('Electronics', case=False, na=False) & 
                     df['titre'].str.contains('Laptop', case=False, na=False)]
        if len(products) > 0:
            top_product = products.sort_values('note_moyenne', ascending=False).iloc[0]
            return f"I recommend {top_product['titre']} with a rating of {top_product['note_moyenne']:.1f}/5. It costs ${top_product['prix']:.2f}."
        else:
            return "I don't have any laptop recommendations at the moment."
    
    elif "phone" in prompt_lower or "smartphone" in prompt_lower:
        products = df[df['categorie'].str.contains('Electronics', case=False, na=False) & 
                     df['titre'].str.contains('Smartphone|Phone', case=False, na=False, regex=True)]
        if len(products) > 0:
            top_product = products.sort_values('note_moyenne', ascending=False).iloc[0]
            return f"I recommend {top_product['titre']} with a rating of {top_product['note_moyenne']:.1f}/5. It costs ${top_product['prix']:.2f}."
        else:
            return "I don't have any smartphone recommendations at the moment."
    
    elif "tablet" in prompt_lower:
        products = df[df['categorie'].str.contains('Electronics', case=False, na=False) & 
                     df['titre'].str.contains('Tablet', case=False, na=False)]
        if len(products) > 0:
            top_product = products.sort_values('note_moyenne', ascending=False).iloc[0]
            return f"I recommend {top_product['titre']} with a rating of {top_product['note_moyenne']:.1f}/5. It costs ${top_product['prix']:.2f}."
        else:
            return "I don't have any tablet recommendations at the moment."
    
    elif "best" in prompt_lower or "top" in prompt_lower:
        top_products = load_top_products()
        if top_products is not None and len(top_products) > 0:
            top_product = top_products.iloc[0]
            return f"Our top product is {top_product['titre']} with an attractiveness score of {top_product['score_attractivite']:.2f}. It costs ${top_product['prix']:.2f} and has a rating of {top_product['note_moyenne']:.1f}/5."
        else:
            return "I don't have information about top products at the moment."
    
    else:
        return "I'm not sure what product you're looking for. Could you specify if you're interested in laptops, smartphones, tablets, or our best products?"

def main():
    """Main function to run the Streamlit app"""
    st.markdown('<h1 class="main-header">E-commerce Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Could not load product data. Please check if the data file exists.")
        return
    
    # Display tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Product Analysis", "Recommendation Assistant"])
    
    with tab1:
        # Display key metrics
        display_metrics(df)
        
        # Display charts
        col1, col2 = st.columns(2)
        
        with col1:
            plot_category_distribution(df)
        
        with col2:
            plot_price_distribution(df)
        
        # Display top products
        top_products = load_top_products()
        if top_products is not None:
            display_top_products(top_products)
    
    with tab2:
        st.markdown('<div class="sub-header">Product Data Explorer</div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            categories = ['All'] + sorted(df['categorie'].unique().tolist())
            selected_category = st.selectbox('Filter by Category', categories)
        
        with col2:
            min_rating = st.slider('Minimum Rating', 0.0, 5.0, 0.0, 0.5)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['categorie'] == selected_category]
        
        filtered_df = filtered_df[filtered_df['note_moyenne'] >= min_rating]
        
        # Display filtered data
        st.dataframe(
            filtered_df,
            column_config={
                "titre": "Product Name",
                "prix": st.column_config.NumberColumn("Price", format="$%.2f"),
                "note_moyenne": st.column_config.NumberColumn("Rating", format="%.1f"),
                "categorie": "Category",
                "vendeur": "Vendor"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Additional analysis
        plot_rating_vs_price(filtered_df)
    
    with tab3:
        # Simple chat interface for product recommendations
        display_chat_interface()

if __name__ == "__main__":
    main()