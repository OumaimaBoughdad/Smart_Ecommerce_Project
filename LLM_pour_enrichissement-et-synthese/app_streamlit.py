"""
Interface Streamlit Chat pour l'Analyseur Chain of Thought
Permet une interaction conversationnelle avec l'analyseur de produits
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import traceback

# Import du code original (à adapter selon votre structure)
# from your_original_file import ProductInsightsCoTGenerator

# Configuration de la page
st.set_page_config(
    page_title="🧠 Analyseur CoT - Chat Interface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .insight-box {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .recommendation-box {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CoTChatInterface:
    """Interface chat pour l'analyseur Chain of Thought"""
    
    def __init__(self):
        self.generator = None
        self.analysis_results = None
        self.conversation_history = []
        
    def initialize_generator(self):
        """Initialise le générateur CoT (simulation)"""
        if self.generator is None:
            with st.spinner("🧠 Initialisation de l'analyseur Chain of Thought..."):
                try:
                    # Simulation de l'initialisation
                    # self.generator = ProductInsightsCoTGenerator()
                    st.success("✅ Analyseur initialisé avec succès!")
                    return True
                except Exception as e:
                    st.error(f"❌ Erreur d'initialisation: {str(e)}")
                    return False
        return True
    
    def process_file_upload(self, uploaded_file):
        """Traite le fichier uploadé"""
        if uploaded_file is not None:
            try:
                # Lecture du fichier
                df = pd.read_csv(uploaded_file, sep=';')
                
                # Validation des colonnes
                required_columns = ['titre', 'prix', 'note_moyenne', 'vendeur', 'disponibilite', 'score_global']
                missing_cols = [col for col in required_columns if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Colonnes manquantes: {missing_cols}")
                    return None
                
                st.success(f"✅ Fichier chargé: {len(df)} produits analysables")
                return df
                
            except Exception as e:
                st.error(f"❌ Erreur de lecture: {str(e)}")
                return None
        return None
    
    def simulate_cot_analysis(self, df):
        """Simulation de l'analyse CoT (à remplacer par le vrai code)"""
        with st.spinner("🔍 Analyse Chain of Thought en cours..."):
            # Simulation des résultats
            analysis_results = {
                'data_stats': {
                    'total_products': len(df),
                    'avg_price': df['prix'].mean(),
                    'median_score': df['score_global'].median(),
                    'unique_vendors': df['vendeur'].nunique()
                },
                'patterns': {
                    'price_performance_correlation': df['prix'].corr(df['score_global']),
                    'top_vendor': df['vendeur'].value_counts().index[0],
                    'stock_rate': (df['disponibilite'] == 'En stock').mean()
                },
                'recommendations': {
                    'pricing': "Adopter une stratégie dynamique basée sur la performance",
                    'vendor': "Diversifier le portefeuille vendeurs",
                    'inventory': "Optimiser les niveaux de stock",
                    'marketing': "Concentrer sur les produits stars"
                }
            }
            
            return analysis_results
    
    def generate_visualizations(self, df):
        """Génère les visualisations interactives"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribution des Prix")
            fig_price = px.histogram(df, x='prix', nbins=20, 
                                   title="Distribution des Prix")
            st.plotly_chart(fig_price, use_container_width=True)
        
        with col2:
            st.subheader("⭐ Scores par Vendeur")
            vendor_scores = df.groupby('vendeur')['score_global'].mean().reset_index()
            fig_vendor = px.bar(vendor_scores, x='vendeur', y='score_global',
                              title="Score Moyen par Vendeur")
            st.plotly_chart(fig_vendor, use_container_width=True)
        
        # Graphique scatter prix vs score
        st.subheader("💰 Relation Prix-Performance")
        fig_scatter = px.scatter(df, x='prix', y='score_global', 
                               color='vendeur', size='note_moyenne',
                               title="Prix vs Score Global")
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    def handle_chat_query(self, user_query, df=None):
        """Gère les requêtes chat"""
        response = ""
        
        # Analyse des intentions de la requête
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ['prix', 'price', 'coût', 'tarif']):
            if df is not None:
                avg_price = df['prix'].mean()
                median_price = df['prix'].median()
                response = f"""
                🧠 **Analyse CoT - Pricing:**
                
                **Étape 1 - Observation:**
                Prix moyen: {avg_price:.2f}€
                Prix médian: {median_price:.2f}€
                
                **Étape 2 - Raisonnement:**
                {'Les prix sont homogènes' if abs(avg_price - median_price) < avg_price * 0.1 else 'Distribution des prix hétérogène'}
                
                **Étape 3 - Recommandation:**
                {'Stratégie de prix uniforme possible' if abs(avg_price - median_price) < avg_price * 0.1 else 'Segmentation tarifaire recommandée'}
                """
        
        elif any(word in query_lower for word in ['vendeur', 'fournisseur', 'supplier']):
            if df is not None:
                top_vendor = df['vendeur'].value_counts().index[0]
                vendor_count = df['vendeur'].nunique()
                response = f"""
                🧠 **Analyse CoT - Vendeurs:**
                
                **Étape 1 - Observation:**
                {vendor_count} vendeurs identifiés
                Vendeur leader: {top_vendor}
                
                **Étape 2 - Analyse de concentration:**
                Répartition: {df['vendeur'].value_counts().to_dict()}
                
                **Étape 3 - Recommandation:**
                {'Diversifier le portefeuille' if df['vendeur'].value_counts().iloc[0] / len(df) > 0.5 else 'Concentration acceptable'}
                """
        
        elif any(word in query_lower for word in ['recommandation', 'conseil', 'suggestion']):
            response = """
            🧠 **Recommandations Chain of Thought:**
            
            **1. Pricing (Priorité: Haute)**
            - Raisonnement: Analyse de la corrélation prix-performance
            - Action: Ajuster la stratégie tarifaire
            
            **2. Vendeurs (Priorité: Moyenne)**
            - Raisonnement: Équilibrage du risque fournisseur
            - Action: Diversifier ou concentrer selon la performance
            
            **3. Stock (Priorité: Haute)**
            - Raisonnement: Impact direct sur les ventes
            - Action: Optimiser les niveaux de disponibilité
            
            **4. Marketing (Priorité: Moyenne)**
            - Raisonnement: ROI marketing sur produits performants
            - Action: Réallouer le budget vers les stars
            """
        
        elif any(word in query_lower for word in ['stock', 'inventaire', 'disponibilité']):
            if df is not None:
                stock_rate = (df['disponibilite'] == 'En stock').mean()
                response = f"""
                🧠 **Analyse CoT - Inventaire:**
                
                **Étape 1 - État actuel:**
                Taux de disponibilité: {stock_rate:.1%}
                
                **Étape 2 - Évaluation:**
                {'Situation critique' if stock_rate < 0.8 else 'Situation acceptable'}
                
                **Étape 3 - Plan d'action:**
                {'Renforcement immédiat des stocks' if stock_rate < 0.8 else 'Optimisation fine des niveaux'}
                """
        
        else:
            response = """
            🧠 **Assistant CoT disponible pour:**
            
            📊 Analyses disponibles:
            - Prix et stratégie tarifaire
            - Performance des vendeurs
            - Gestion des stocks
            - Recommandations marketing
            
            💬 Exemples de questions:
            - "Analyse les prix de mes produits"
            - "Quels sont mes meilleurs vendeurs ?"
            - "Donne-moi des recommandations"
            - "Comment optimiser mon stock ?"
            """
        
        return response

def main():
    """Fonction principale de l'interface Streamlit"""
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Analyseur Chain of Thought - Interface Chat</h1>
        <p>Analyse conversationnelle de vos données produits avec raisonnement explicite</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation de l'interface
    if 'chat_interface' not in st.session_state:
        st.session_state.chat_interface = CoTChatInterface()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Bonjour ! Je suis votre assistant Chain of Thought. Uploadez vos données produits et posez-moi vos questions d'analyse !"}
        ]
    
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    # Sidebar pour le contrôle
    with st.sidebar:
        st.header("🎛️ Configuration")
        
        # Upload de fichier
        st.subheader("📁 Données")
        uploaded_file = st.file_uploader(
            "Choisir un fichier CSV",
            type=['csv'],
            help="Format attendu: titre, prix, note_moyenne, vendeur, disponibilite, score_global"
        )
        
        if uploaded_file is not None:
            df = st.session_state.chat_interface.process_file_upload(uploaded_file)
            if df is not None:
                st.session_state.data = df
                st.success(f"✅ {len(df)} produits chargés")
        
        # Options d'analyse
        st.subheader("⚙️ Options")
        show_reasoning = st.checkbox("Afficher le raisonnement détaillé", value=True)
        auto_insights = st.checkbox("Insights automatiques", value=False)
        
        # Statistiques rapides
        if st.session_state.data is not None:
            st.subheader("📊 Aperçu rapide")
            df = st.session_state.data
            st.metric("Produits", len(df))
            st.metric("Prix moyen", f"{df['prix'].mean():.0f}€")
            st.metric("Score moyen", f"{df['score_global'].mean():.3f}")
    
    # Interface chat principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat avec l'Analyseur CoT")
        
        # Affichage des messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input utilisateur
        if prompt := st.chat_input("Posez votre question d'analyse..."):
            # Ajouter le message utilisateur
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Afficher le message utilisateur
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Générer et afficher la réponse
            with st.chat_message("assistant"):
                with st.spinner("🧠 Raisonnement en cours..."):
                    response = st.session_state.chat_interface.handle_chat_query(
                        prompt, st.session_state.data
                    )
                    st.markdown(response)
            
            # Ajouter la réponse à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.header("📈 Visualisations")
        
        if st.session_state.data is not None:
            # Bouton pour générer l'analyse complète
            if st.button("🚀 Analyse CoT Complète", type="primary"):
                with st.spinner("🔍 Analyse approfondie..."):
                    results = st.session_state.chat_interface.simulate_cot_analysis(
                        st.session_state.data
                    )
                    
                    # Affichage des résultats
                    st.subheader("🎯 Insights Clés")
                    
                    stats = results['data_stats']
                    st.metric("Produits analysés", stats['total_products'])
                    st.metric("Prix moyen", f"{stats['avg_price']:.0f}€")
                    st.metric("Score médian", f"{stats['median_score']:.3f}")
                    
                    # Recommandations
                    st.subheader("💡 Recommandations")
                    for domain, rec in results['recommendations'].items():
                        st.info(f"**{domain.upper()}**: {rec}")
            
            # Mini visualisations
            if st.checkbox("Graphiques rapides"):
                df = st.session_state.data
                
                # Distribution des prix
                fig = px.histogram(df, x='prix', nbins=10, title="Distribution Prix")
                st.plotly_chart(fig, use_container_width=True, key="mini_price_dist")
                
                # Top vendeurs
                top_vendors = df['vendeur'].value_counts().head(5)
                fig2 = px.bar(x=top_vendors.index, y=top_vendors.values, 
                             title="Top 5 Vendeurs")
                st.plotly_chart(fig2, use_container_width=True, key="mini_vendors")
        
        else:
            st.info("📁 Uploadez vos données pour voir les visualisations")
    
    # Section d'analyse détaillée (expandable)
    if st.session_state.data is not None:
        with st.expander("📊 Analyse Détaillée"):
            st.session_state.chat_interface.generate_visualizations(st.session_state.data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🧠 Analyseur Chain of Thought - Interface conversationnelle pour l'analyse produit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()