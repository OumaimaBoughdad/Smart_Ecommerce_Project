#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Streamlit pour le scraping multi-catégories avec interface de chat CoT
Intègre toutes les fonctionnalités du script de scraping original avec nouvelles boutiques
et sélection des top-5 produits via un modèle RandomForest, plus une interface de chat pour l'analyse CoT
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from urllib.parse import urljoin
import logging
import io
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import base64
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# Configuration de la page
st.set_page_config(
    page_title="Scraper Multi-Catégories avec Chat CoT",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS combiné pour les deux interfaces
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
    
    .progress-bar {
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Classe CoTChatInterface (adaptée pour utiliser les données scrapées)
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
    
    def validate_data(self, df):
        """Valide les données scrapées"""
        if df is None or df.empty:
            st.error("❌ Aucune donnée disponible pour l'analyse.")
            return None
        
        # Vérification des colonnes nécessaires
        required_columns = ['titre', 'prix', 'note_moyenne', 'vendeur', 'disponibilite']
        available_columns = df.columns.tolist()
        missing_cols = [col for col in required_columns if col not in available_columns]
        
        if missing_cols:
            st.error(f"❌ Colonnes manquantes: {missing_cols}")
            return None
        
        # Ajouter score_global si absent (simulation basée sur note_moyenne)
        if 'score_global' not in df.columns:
            df['score_global'] = df['note_moyenne'] * 20  # Conversion arbitraire en score /100
        
        return df
    
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
                    'stock_rate': (df['disponibilite'] == 'Disponible').mean()
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
                stock_rate = (df['disponibilite'] == 'Disponible').mean()
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

# Classe StreamlitDiverseScraper
class StreamlitDiverseScraper:
    def __init__(self):
        """Initialise le scraper pour l'interface Streamlit"""
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        self.selectors = {
            'product_container': '.thumbnail, .product-wrapper, .card, .product-item, .item, article.product_pod, .product-grid, .item-container, li',
            'title': '.title, h4 a, .card-title, .product-title, h3 a, .name, h1, h2, h3, h4, h5',
            'price': '.price, .pull-right.price, .cost, .amount, .product-price, .price_color, span.price',
            'availability': '.stock, .availability, .in-stock, .status, .instock',
            'rating': '.ratings, .rating, .stars, .review, .score, .star-rating',
            'description': '.description, .card-text, .summary, .excerpt, p',
            'vendor': '.brand, .vendor, .seller, .manufacturer, .author',
            'category': '.category, .breadcrumb, .cat, .type',
            'link': 'a.title, h4 a, h3 a, .product-link, a',
            'pagination': '.pagination a, a[rel="next"], .next a, .page, a.page-link',
        }
        
        self.diverse_sites = {
            'books_demo': {
                'name': '📚 Books to Scrape',
                'description': 'Site de démonstration avec livres par catégories',
                'base_url': 'http://books.toscrape.com',
                'categories': {
                    'travel': '/catalogue/category/books/travel_2/index.html',
                    'mystery': '/catalogue/category/books/mystery_3/index.html',
                    'history': '/catalogue/category/books/history_32/index.html',
                    'romance': '/catalogue/category/books/romance_8/index.html',
                    'science': '/catalogue/category/books/science_22/index.html',
                    'fiction': '/catalogue/category/books/fiction_10/index.html',
                    'philosophy': '/catalogue/category/books/philosophy_7/index.html',
                    'business': '/catalogue/category/books/business_35/index.html',
                    'health': '/catalogue/category/books/health_47/index.html',
                    'sports': '/catalogue/category/books/sports-and-games_17/index.html'
                },
                'selectors': {
                    'product_container': 'article.product_pod, li',
                    'title': 'h3 a, h4, .title',
                    'price': '.price_color, .price',
                    'rating': '.star-rating',
                    'link': 'h3 a, a',
                    'availability': '.instock.availability',
                    'description': 'p',
                    'pagination': '.next a, a[rel="next"]'
                }
            },
            'webscraper_varied': {
                'name': '🛒 WebScraper.io Test Sites',
                'description': 'Sites de test e-commerce avec différents types de produits',
                'base_url': 'https://webscraper.io/test-sites/e-commerce',
                'categories': {
                    'static_all': '/static',
                    'ajax_all': '/ajax',
                    'more_all': '/more',
                    'static_computers': '/static/computers',
                    'ajax_computers': '/ajax/computers',
                    'static_phones': '/static/phones',
                    'ajax_phones': '/ajax/phones',
                    'static_clothes': '/static/clothes'
                },
                'selectors': {
                    'product_container': '.thumbnail, .card, .product-item',
                    'title': '.title, h4 a',
                    'price': '.price',
                    'rating': '.ratings',
                    'description': '.description',
                    'link': 'a.title, h4 a',
                    'pagination': '.pagination a, .next a'
                }
            },
            'jsonplaceholder': {
                'name': '💾 JSONPlaceholder',
                'description': 'API de test pour contenu digital',
                'base_url': 'https://jsonplaceholder.typicode.com',
                'categories': {
                    'posts': '/posts',
                    'albums': '/albums',
                    'photos': '/photos'
                },
                'selectors': self.selectors
            },
            'quotes_to_scrape': {
                'name': '📜 Quotes to Scrape',
                'description': 'Site de test avec citations comme produits numériques',
                'base_url': 'http://quotes.toscrape.com',
                'categories': {
                    'all_quotes': '/',
                    'inspirational': '/tag/inspirational',
                    'love': '/tag/love',
                    'life': '/tag/life',
                    'humor': '/tag/humor'
                },
                'selectors': {
                    'product_container': '.quote',
                    'title': '.text',
                    'price': None,
                    'rating': None,
                    'description': '.text',
                    'vendor': '.author',
                    'link': 'a',
                    'pagination': '.next a'
                }
            },
            'dummy_products': {
                'name': '🛍️ Dummy Products API',
                'description': 'API publique de produits fictifs pour e-commerce',
                'base_url': 'https://dummyjson.com',
                'categories': {
                    'products': '/products',
                    'smartphones': '/products/category/smartphones',
                    'laptops': '/products/category/laptops',
                    'fragrances': '/products/category/fragrances',
                    'skincare': '/products/category/skincare',
                    'groceries': '/products/category/groceries'
                },
                'selectors': self.selectors
            },
            'fake_store': {
                'name': '🏬  Store API',
                'description': 'API de test avec produits e-commerce variés',
                'base_url': 'https://fakestoreapi.com',
                'categories': {
                    'all_products': '/products',
                    'electronics': '/products/category/electronics',
                    'jewelery': '/products/category/jewelery',
                    'mens_clothing': '/products/category/men\'s clothing',
                    'womens_clothing': '/products/category/women\'s clothing'
                },
                'selectors': self.selectors
            }
        }
        
        if 'scraping_logs' not in st.session_state:
            st.session_state.scraping_logs = []
        if 'scraped_products' not in st.session_state:
            st.session_state.scraped_products = []
        if 'start_full_scraping' not in st.session_state:
            st.session_state.start_full_scraping = False
        if 'stop_scraping' not in st.session_state:
            st.session_state.stop_scraping = False
    
    def log_message(self, message, level="INFO"):
        """Ajoute un message aux logs de session"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        st.session_state.scraping_logs.append(log_entry)
        return log_entry
    
    def _make_request(self, url, retries=3):
        """Effectue une requête HTTP avec gestion des erreurs"""
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response
            except requests.RequestException as e:
                self.log_message(f"Erreur requête {url} (tentative {attempt + 1}): {e}", "WARNING")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
        return None
    
    def _random_delay(self, min_delay=0.5, max_delay=2):
        """Pause aléatoire entre les requêtes"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def _clean_text(self, text):
        """Nettoie et normalise le texte"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        text = text.replace(';', ',').replace('\n', ' ').replace('\r', ' ')
        return text[:300]
    
    def _extract_price(self, price_element):
        """Extrait et normalise le prix"""
        if not price_element:
            return str(random.choice([19.99, 29.99, 49.99, 79.99, 99.99]))
        price_text = self._clean_text(price_element.get_text())
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            try:
                return str(float(price_match.group()))
            except:
                pass
        return str(random.choice([19.99, 29.99, 49.99, 79.99, 99.99]))
    
    def _extract_product_data(self, product_element, category_name, page_url, selectors):
        """Extrait les données d'un produit avec sélecteurs spécifiques"""
        title_elem = product_element.select_one(selectors.get('title', '.title'))
        title = self._clean_text(title_elem.get_text() if title_elem else "")
        if title_elem and title_elem.has_attr('title'):
            title = title or self._clean_text(title_elem['title'])
        if not title:
            title = self._clean_text(product_element.get_text()[:100])
        
        price_elem = product_element.select_one(selectors.get('price', '.price'))
        price = self._extract_price(price_elem)
        
        avail_elem = product_element.select_one(selectors.get('availability', '.availability'))
        availability = "Disponible"
        if avail_elem:
            avail_text = self._clean_text(avail_elem.get_text()).lower()
            if 'out' in avail_text or 'rupture' in avail_text:
                availability = "Rupture"
        
        rating_elem = product_element.select_one(selectors.get('rating', '.rating'))
        rating = ""
        if rating_elem:
            if 'star-rating' in rating_elem.get('class', []):
                rating_classes = rating_elem.get('class', [])
                rating_map = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}
                for cls in rating_classes:
                    if cls in rating_map:
                        rating = rating_map[cls]
                        break
            else:
                rating = self._extract_price(rating_elem)
        if not rating:
            rating = str(random.choice([3, 3.5, 4, 4.5, 5]))
        
        desc_elem = product_element.select_one(selectors.get('description', '.description'))
        description = self._clean_text(desc_elem.get_text() if desc_elem else "")
        
        vendor_elem = product_element.select_one(selectors.get('vendor', '.vendor'))
        vendor = self._clean_text(vendor_elem.get_text() if vendor_elem else "N/A")
        
        category = category_name.replace('_', ' ').title()
        if 'jsonplaceholder' in category_name:
            category = "Digital Content"
        
        link_elem = product_element.select_one(selectors.get('link', 'a'))
        product_link = urljoin(page_url, link_elem['href']) if link_elem and link_elem.has_attr('href') else page_url
        
        return {
            'titre': title,
            'prix': float(price) if price else 0.0,
            'disponibilite': availability,
            'note_moyenne': float(rating) if rating else 0.0,
            'description': description[:200] + "..." if len(description) > 200 else description,
            'vendeur': vendor,
            'categorie': category,
            'lien_produit': product_link,
            'source': category_name.split('_')[0] if '_' in category_name else category_name
        }
    
    def _create_product_from_json(self, json_element, category_name, url):
        """Crée un produit à partir de données JSON"""
        if 'title' in json_element:
            title = self._clean_text(json_element.get('title', '')[:50])
        elif 'name' in json_element:
            title = self._clean_text(json_element.get('name', '')[:50])
        else:
            title = "Digital Item"

        if not title:
            title = "Digital Item"

        price = json_element.get('price', random.uniform(9.99, 99.99))
        if isinstance(price, (int, float)):
            price = float(price)
        else:
            price = random.uniform(9.99, 99.99)

        description = self._clean_text(json_element.get('description', json_element.get('body', '')[:200]))
        if not description:
            description = "Digital content or media item."

        vendor = json_element.get('brand', json_element.get('author', 'Digital Store'))

        rating = json_element.get('rating', {}).get('rate', random.choice([3, 3.5, 4, 4.5, 5]))
        if isinstance(rating, dict):
            rating = random.choice([3, 3.5, 4, 4.5, 5])

        return {
            'titre': title,
            'prix': round(price, 2),
            'disponibilite': random.choice(['Disponible', 'Rupture']),
            'note_moyenne': float(rating),
            'description': description,
            'vendeur': self._clean_text(vendor),
            'categorie': category_name.replace('_', ' ').title(),
            'lien_produit': url,
            'source': category_name.split('_')[0] if '_' in category_name else category_name
        }
    
    def _get_next_page_url(self, soup, current_url, selectors):
        """Trouve l'URL de la page suivante"""
        next_links = soup.select(selectors.get('pagination', '.pagination a'))
        for link in next_links:
            if link.has_attr('href'):
                link_text = self._clean_text(link.get_text()).lower()
                if any(word in link_text for word in ['next', 'suivant', '>', '»']):
                    return urljoin(current_url, link['href'])
        return None
    
    def scrape_site_category(self, site_name, site_config, category_name, category_path, max_pages=5, progress_bar=None):
        """Scrape une catégorie spécifique d'un site avec barre de progression"""
        base_url = site_config['base_url']
        url = base_url + category_path
        selectors = site_config.get('selectors', self.selectors)
        
        self.log_message(f"Début scraping: {site_name} - {category_name}")
        
        products = []
        current_url = url
        page_count = 0
        
        while current_url and page_count < max_pages:
            page_count += 1
            self.log_message(f"Page {page_count} - {site_name}/{category_name}")
            
            if progress_bar:
                progress_bar.progress(page_count / max_pages)
            
            response = self._make_request(current_url)
            if not response:
                self.log_message(f"Impossible de récupérer: {current_url}", "ERROR")
                break
            
            if 'jsonplaceholder' in site_name or 'dummy_products' in site_name or 'fake_store' in site_name:
                try:
                    json_data = response.json()
                    if isinstance(json_data, dict) and 'products' in json_data:
                        json_data = json_data['products']
                    if isinstance(json_data, list):
                        for item in json_data:
                            product = self._create_product_from_json(item, category_name, current_url)
                            if product['titre']:
                                products.append(product)
                        self.log_message(f"Trouvé {len(json_data)} éléments JSON")
                    else:
                        product = self._create_product_from_json(json_data, category_name, current_url)
                        if product['titre']:
                            products.append(product)
                        self.log_message("Trouvé 1 élément JSON")
                    break
                except Exception as e:
                    self.log_message(f"Erreur JSON: {e}", "WARNING")
                    break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            container_selector = selectors.get('product_container', '.product')
            product_elements = soup.select(container_selector)
            
            if not product_elements:
                self.log_message(f"Aucun produit trouvé avec '{container_selector}'", "WARNING")
                for alt_selector in ['article', '.item', '.product-item', 'li', '.product-grid']:
                    product_elements = soup.select(alt_selector)
                    if product_elements:
                        self.log_message(f"Trouvé avec sélecteur alternatif '{alt_selector}'")
                        break
            
            if not product_elements:
                self.log_message(f"Aucun produit trouvé sur: {current_url}", "WARNING")
                break
            
            self.log_message(f"Trouvé {len(product_elements)} éléments")
            
            for product_elem in product_elements:
                try:
                    product_data = self._extract_product_data(
                        product_elem, f"{site_name}_{category_name}", current_url, selectors
                    )
                    if product_data['titre']:
                        products.append(product_data)
                except Exception as e:
                    self.log_message(f"Erreur extraction: {e}", "WARNING")
                    continue
            
            next_url = self._get_next_page_url(soup, current_url, selectors)
            if next_url == current_url or not next_url:
                break
            current_url = next_url
            
            self._random_delay(1, 2)
        
        self.log_message(f"{site_name}/{category_name} terminé: {len(products)} produits")
        return products
    
    def select_top_5_products(self, df, model_path="random_forest_model.pkl"):
        """Sélectionne les 5 meilleurs produits à l'aide du modèle RandomForest"""
        try:
            # Charger le modèle
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            
            # Vérifier si le modèle a une méthode predict
            if not hasattr(model, 'predict'):
                raise ValueError("Le fichier chargé n'est pas un modèle scikit-learn valide avec predict.")
            
            # Préparer les données pour la prédiction
            features = ['prix', 'note_moyenne', 'ventes_estimees', 'dispo_score']
            X = df[['prix', 'note_moyenne']].copy()  # Base columns from scraped data
            
            # Calculer ventes_estimees basé sur la note_moyenne
            np.random.seed(42)  # Pour reproductibilité
            X['ventes_estimees'] = np.where(
                df['note_moyenne'] > 3,
                np.random.poisson(lam=50, size=len(df)),
                np.random.poisson(lam=20, size=len(df))
            )
            
            # Calculer dispo_score basé sur disponibilité
            availability_mapping = {
                'Disponible': 1.0,
                'Stock limité': 0.7,
                'Rupture': 0.0,
                'Inconnu': 0.5
            }
            X['dispo_score'] = df['disponibilite'].map(availability_mapping).fillna(0.5)
            
            # Gérer les valeurs manquantes
            X = X.fillna(X.mean())
            
            # Standardisation des caractéristiques
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Faire les prédictions (regression, donc predict seulement)
            try:
                predictions = model.predict(X_scaled)
            except Exception as e:
                self.log_message(f"Erreur lors de la prédiction: {e}", "ERROR")
                return pd.DataFrame()
            
            # Ajouter les prédictions au DataFrame
            df['prediction_score'] = predictions
            
            # Trier et sélectionner les 5 meilleurs produits
            top_5_df = df.sort_values(by='prediction_score', ascending=False).head(5)
            
            return top_5_df[
                ['titre', 'prix', 'note_moyenne', 'categorie', 'disponibilite', 'vendeur', 'source', 'lien_produit', 'prediction_score']
            ]
        except Exception as e:
            self.log_message(f"Erreur lors de la sélection des top-5 produits: {e}", "ERROR")
            return pd.DataFrame()

def create_download_link(df, filename):
    """Crée un lien de téléchargement pour le DataFrame"""
    csv = df.to_csv(index=False, encoding='utf-8', sep=';')
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Télécharger {filename}</a>'
    return href

def main():
    """Interface principale Streamlit"""
    
    st.title("🛍️ Scraper Agent To Agent avec Chat CoT")
    st.markdown("### Application de scraping pour sites e-commerce diversifiés avec analyse conversationnelle")
    
    # Initialisation du scraper
    scraper = StreamlitDiverseScraper()
    
    # Initialisation de l'interface chat
    if 'chat_interface' not in st.session_state:
        st.session_state.chat_interface = CoTChatInterface()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Bonjour ! Je suis votre assistant Chain of Thought. Scrapez des données et posez-moi vos questions d'analyse !"}
        ]
    
    # Sidebar pour la configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Sélection des sites
    st.sidebar.subheader("Sites à scraper")
    selected_sites = {}
    
    for site_key, site_config in scraper.diverse_sites.items():
        selected_sites[site_key] = st.sidebar.checkbox(
            f"{site_config['name']}", 
            value=True,
            help=site_config['description']
        )
    
    # Paramètres de scraping
    st.sidebar.subheader("Paramètres")
    max_pages = st.sidebar.slider("Pages max par catégorie", 1, 20, 5)
    target_products = st.sidebar.number_input("Objectif produits", 100, 5000, 1000)
    
    # Paramètres de l'analyse CoT
    st.sidebar.subheader("Analyse CoT")
    show_reasoning = st.sidebar.checkbox("Afficher le raisonnement détaillé", value=True)
    auto_insights = st.sidebar.checkbox("Insights automatiques", value=False)
    
    # Statistiques rapides
    if st.session_state.scraped_products:
        df = pd.DataFrame(st.session_state.scraped_products)
        st.sidebar.subheader("📊 Aperçu rapide")
        st.sidebar.metric("Produits", len(df))
        st.sidebar.metric("Prix moyen", f"{df['prix'].mean():.0f}€")
        st.sidebar.metric("Note moyenne", f"{df['note_moyenne'].mean():.3f}")
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Scraping", "📊 Données", "📈 Analyses", "📋 Logs", "💬 Chat CoT"])
    
    with tab1:
        st.header("🚀 Contrôle de Scraping")
        
        # Boutons de contrôle global
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 Scraping Complet", type="primary", use_container_width=True):
                if not any(selected_sites.values()):
                    st.error("Veuillez sélectionner au moins un site à scraper!")
                else:
                    st.session_state.start_full_scraping = True
        
        with col2:
            if st.button("🗑️ Effacer Données", use_container_width=True):
                st.session_state.scraped_products = []
                st.session_state.scraping_logs = []
                st.success("Données effacées!")
        
        with col3:
            if st.button("⏹️ Arrêter Scraping", use_container_width=True):
                st.session_state.stop_scraping = True
                st.warning("Arrêt demandé!")
        
        st.divider()
        
        # Scraping par site individuel
        st.subheader("🎯 Scraping Par Site")
        
        for site_key, site_config in scraper.diverse_sites.items():
            if not selected_sites.get(site_key, False):
                continue
                
            with st.expander(f"{site_config['name']} - {len(site_config['categories'])} catégories", expanded=False):
                st.markdown(f"**Description:** {site_config['description']}")
                st.markdown(f"**URL de base:** `{site_config['base_url']}`")
                
                # Bouton pour scraper tout le site
                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button(f"🚀 Scraper tout {site_config['name']}", key=f"full_{site_key}"):
                        st.session_state[f'scrape_site_{site_key}'] = True
                
                with col2:
                    site_products = len([p for p in st.session_state.scraped_products if p.get('source') == site_key])
                    st.metric("Produits", site_products)
                
                st.markdown("**Catégories disponibles:**")
                
                categories_list = list(site_config['categories'].items())
                cols_per_row = 3
                
                for i in range(0, len(categories_list), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, (cat_name, cat_path) in enumerate(categories_list[i:i+cols_per_row]):
                        with cols[j]:
                            cat_products = len([p for p in st.session_state.scraped_products 
                                              if f"{site_key}_{cat_name}" in p.get('source', '')])
                            
                            button_text = f"📂 {cat_name.replace('_', ' ').title()}"
                            if cat_products > 0:
                                button_text += f" ({cat_products})"
                            
                            if st.button(button_text, key=f"cat_{site_key}_{cat_name}", 
                                       use_container_width=True):
                                st.session_state[f'scrape_cat_{site_key}_{cat_name}'] = True
        
        # Gestion du scraping complet
        if st.session_state.get('start_full_scraping', False):
            st.session_state.start_full_scraping = False
            
            st.session_state.scraped_products = []
            st.session_state.scraping_logs = []
            
            total_products = 0
            progress_container = st.container()
            
            with progress_container:
                overall_progress = st.progress(0)
                status_text = st.empty()
                current_progress = st.progress(0)
                
                total_sites = sum(1 for v in selected_sites.values() if v)
                site_counter = 0
                
                for site_key, selected in selected_sites.items():
                    if not selected or total_products >= target_products:
                        continue
                    
                    if st.session_state.get('stop_scraping', False):
                        st.session_state.stop_scraping = False
                        break
                    
                    site_counter += 1
                    site_config = scraper.diverse_sites[site_key]
                    
                    status_text.text(f"Scraping {site_config['name']} ({site_counter}/{total_sites})")
                    overall_progress.progress(site_counter / total_sites)
                    
                    for cat_name, cat_path in site_config['categories'].items():
                        if total_products >= target_products:
                            break
                        
                        if st.session_state.get('stop_scraping', False):
                            break
                        
                        try:
                            products = scraper.scrape_site_category(
                                site_key, site_config, cat_name, cat_path, 
                                max_pages=max_pages, progress_bar=current_progress
                            )
                            
                            if products:
                                st.session_state.scraped_products.extend(products)
                                total_products += len(products)
                            
                        except Exception as e:
                            scraper.log_message(f"Erreur {site_key}/{cat_name}: {e}", "ERROR")
                
                overall_progress.progress(1.0)
                status_text.text(f"✅ Scraping terminé! ")
            
            if st.session_state.scraped_products:
                st.success(f"🎉 Scraping réussi! ")
            else:
                st.warning("Aucun produit extrait. Vérifiez les logs pour plus d'informations.")
        
        # Gestion du scraping par site
        for site_key, site_config in scraper.diverse_sites.items():
            if st.session_state.get(f'scrape_site_{site_key}', False):
                st.session_state[f'scrape_site_{site_key}'] = False
                
                with st.spinner(f"Scraping de {site_config['name']}..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    total_cats = len(site_config['categories'])
                    cat_counter = 0
                    
                    for cat_name, cat_path in site_config['categories'].items():
                        cat_counter += 1
                        status_text.text(f"Scraping {cat_name} ({cat_counter}/{total_cats})")
                        progress_bar.progress(cat_counter / total_cats)
                        
                        try:
                            products = scraper.scrape_site_category(
                                site_key, site_config, cat_name, cat_path, max_pages=max_pages
                            )
                            if products:
                                st.session_state.scraped_products.extend(products)
                        except Exception as e:
                            scraper.log_message(f"Erreur {site_key}/{cat_name}: {e}", "ERROR")
                    
                    st.success(f"✅ Site {site_config['name']} terminé!")
        
        # Gestion du scraping par catégorie
        for site_key, site_config in scraper.diverse_sites.items():
            for cat_name, cat_path in site_config['categories'].items():
                if st.session_state.get(f'scrape_cat_{site_key}_{cat_name}', False):
                    st.session_state[f'scrape_cat_{site_key}_{cat_name}'] = False
                    
                    with st.spinner(f"Scraping {cat_name} de {site_config['name']}..."):
                        try:
                            products = scraper.scrape_site_category(
                                site_key, site_config, cat_name, cat_path, max_pages=max_pages
                            )
                            if products:
                                st.session_state.scraped_products.extend(products)
                                st.success(f"✅ Catégorie {cat_name} terminée! {len(products)} produits ajoutés")
                            else:
                                st.warning(f"Aucun produit trouvé pour {cat_name}")
                        except Exception as e:
                            st.error(f"Erreur lors du scraping de {cat_name}: {e}")
                            scraper.log_message(f"Erreur {site_key}/{cat_name}: {e}", "ERROR")
    
    with tab2:
        st.header("📊 Données Scrapées")
        
        if st.session_state.scraped_products:
            df = pd.DataFrame(st.session_state.scraped_products)
            
            # Statistiques générales
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Produits", len(df))
            with col2:
                st.metric("Prix Moyen", f"{df['prix'].mean():.2f}€")
            with col3:
                st.metric("Note Moyenne", f"{df['note_moyenne'].mean():.1f}/5")
            with col4:
                disponibles = len(df[df['disponibilite'] == 'Disponible'])
                st.metric("Disponibles", f"{disponibles} ({disponibles/len(df)*100:.1f}%)")
            with col5:
                categories_uniques = df['categorie'].nunique()
                st.metric("Catégories", categories_uniques)
            
            # Statistiques par source
            st.subheader("📋 Résumé par Source")
            source_summary = df.groupby('source').agg({
                'titre': 'count',
                'prix': 'mean',
                'note_moyenne': 'mean',
                'categorie': 'nunique'
            }).round(2)
            source_summary.columns = ['Produits', 'Prix Moyen (€)', 'Note Moyenne', 'Catégories']
            
            for source in source_summary.index:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    count = source_summary.loc[source, 'Produits']
                    percentage = count / len(df)
                    st.write(f"**{scraper.diverse_sites.get(source, {}).get('name', source)}**")
                    st.progress(percentage)
                    st.write(f"{count} produits ({percentage*100:.1f}%)")
                with col2:
                    st.metric("Prix €", f"{source_summary.loc[source, 'Prix Moyen (€)']:.2f}")
                with col3:
                    st.metric("Note", f"{source_summary.loc[source, 'Note Moyenne']:.1f}/5")
                with col4:
                    st.metric("Catégories", int(source_summary.loc[source, 'Catégories']))
            
            st.divider()
            
            # Filtres avancés
            st.subheader("🔍 Filtres Avancés")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                categories = ['Toutes'] + sorted(df['categorie'].unique().tolist())
                selected_category = st.selectbox("Catégorie", categories)
            
            with col2:
                sources = ['Toutes'] + sorted(df['source'].unique().tolist())
                selected_source = st.selectbox("Source", sources)
            
            with col3:
                availability_options = ['Toutes'] + sorted(df['disponibilite'].unique().tolist())
                selected_availability = st.selectbox("Disponibilité", availability_options)
            
            col1, col2 = st.columns(2)
            with col1:
                price_range = st.slider(
                    "Fourchette de prix (€)",
                    float(df['prix'].min()),
                    float(df['prix'].max()),
                    (float(df['prix'].min()), float(df['prix'].max()))
                )
            
            with col2:
                rating_range = st.slider(
                    "Fourchette de notes",
                    float(df['note_moyenne'].min()),
                    float(df['note_moyenne'].max()),
                    (float(df['note_moyenne'].min()), float(df['note_moyenne'].max()))
                )
            
            # Application des filtres
            filtered_df = df.copy()
            if selected_category != 'Toutes':
                filtered_df = filtered_df[filtered_df['categorie'] == selected_category]
            if selected_source != 'Toutes':
                filtered_df = filtered_df[filtered_df['source'] == selected_source]
            if selected_availability != 'Toutes':
                filtered_df = filtered_df[filtered_df['disponibilite'] == selected_availability]
            
            filtered_df = filtered_df[
                (filtered_df['prix'] >= price_range[0]) & 
                (filtered_df['prix'] <= price_range[1]) &
                (filtered_df['note_moyenne'] >= rating_range[0]) & 
                (filtered_df['note_moyenne'] <= rating_range[1])
            ]
            
            # Tri
            sort_options = {
                'Titre (A-Z)': ['titre', True],
                'Titre (Z-A)': ['titre', False],
                'Prix (croissant)': ['prix', True],
                'Prix (décroissant)': ['prix', False],
                'Note (croissante)': ['note_moyenne', True],
                'Note (décroissante)': ['note_moyenne', False],
                'Catégorie': ['categorie', True]
            }
            
            selected_sort = st.selectbox("Tri", list(sort_options.keys()))
            sort_column, ascending = sort_options[selected_sort]
            filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)
            
            # Affichage du tableau
            st.subheader(f"📋 Données Filtrées ({len(filtered_df)}/{len(df)} produits)")
            
            col1, col2 = st.columns(2)
            with col1:
                show_description = st.checkbox("Afficher descriptions", value=False)
            with col2:
                show_links = st.checkbox("Afficher liens", value=False)
            
            display_columns = ['titre', 'prix', 'categorie', 'note_moyenne', 'disponibilite', 'vendeur', 'source']
            if show_description:
                display_columns.append('description')
            if show_links:
                display_columns.append('lien_produit')
            
            column_config = {
                'titre': st.column_config.TextColumn('Titre', width="medium"),
                'prix': st.column_config.NumberColumn('Prix (€)', format="%.2f €"),
                'note_moyenne': st.column_config.NumberColumn('Note', format="%.1f ⭐"),
                'lien_produit': st.column_config.LinkColumn('Lien'),
            }
            
            st.dataframe(
                filtered_df[display_columns],
                use_container_width=True,
                column_config=column_config,
                hide_index=True
            )
            
            # Section pour les top-5 produits
            st.subheader("🏆 Top-5 Produits Recommandés")
            top_5_products = scraper.select_top_5_products(df)
            if not top_5_products.empty:
                st.write("Les 5 meilleurs produits selon le modèle RandomForest :")
                column_config = {
                    'titre': st.column_config.TextColumn('Titre', width="medium"),
                    'prix': st.column_config.NumberColumn('Prix (€)', format="%.2f €"),
                    'note_moyenne': st.column_config.NumberColumn('Note', format="%.1f ⭐"),
                    'lien_produit': st.column_config.LinkColumn('Lien'),
                    'prediction_score': st.column_config.NumberColumn('Score', format="%.3f")
                }
                st.dataframe(
                    top_5_products,
                    use_container_width=True,
                    column_config=column_config,
                    hide_index=True
                )
                
                top_5_filename = f"top_5_produits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                st.markdown(create_download_link(top_5_products, top_5_filename), unsafe_allow_html=True)
            else:
                st.warning("Impossible de générer les recommandations. Vérifiez le modèle ou les logs.")
            
            # Actions sur les données
            st.subheader("📥 Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filename = f"produits_scrapes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                st.markdown(create_download_link(filtered_df, filename), unsafe_allow_html=True)
            
            with col2:
                if st.button("🔄 Actualiser les données"):
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Supprimer les données filtrées"):
                    indices_to_remove = filtered_df.index.tolist()
                    st.session_state.scraped_products = [
                        product for i, product in enumerate(st.session_state.scraped_products) 
                        if i not in indices_to_remove
                    ]
                    st.success(f"{len(indices_to_remove)} produits supprimés!")
                    st.rerun()
            
        else:
            st.info("🚀 Aucune donnée disponible. Lancez d'abord un scraping depuis l'onglet Scraping!")
    
    with tab3:
        st.header("📈 Analyses et Visualisations")
        
        if st.session_state.scraped_products:
            df = pd.DataFrame(st.session_state.scraped_products)
            
            st.subheader("Répartition par Catégorie")
            category_counts = df['categorie'].value_counts()
            fig_pie = px.pie(
                values=category_counts.values, 
                names=category_counts.index,
                title="Distribution des produits par catégorie"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.subheader("Distribution des Prix")
            fig_hist = px.histogram(
                df, x='prix', nbins=30,
                title="Distribution des prix",
                labels={'prix': 'Prix (€)', 'count': 'Nombre de produits'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
            st.subheader("Notes Moyennes par Catégorie")
            avg_ratings = df.groupby('categorie')['note_moyenne'].mean().sort_values(ascending=False)
            fig_bar = px.bar(
                x=avg_ratings.index, y=avg_ratings.values,
                title="Note moyenne par catégorie",
                labels={'x': 'Catégorie', 'y': 'Note moyenne'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.subheader("Relation Prix-Note")
            fig_scatter = px.scatter(
                df, x='prix', y='note_moyenne', color='categorie',
                title="Relation entre prix et note",
                labels={'prix': 'Prix (€)', 'note_moyenne': 'Note moyenne'}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.subheader("Statistiques par Source")
            source_stats = df.groupby('source').agg({
                'titre': 'count',
                'prix': 'mean',
                'note_moyenne': 'mean'
            }).round(2)
            source_stats.columns = ['Nombre de produits', 'Prix moyen (€)', 'Note moyenne']
            st.dataframe(source_stats, use_container_width=True)
            
        else:
            st.info("Aucune donnée disponible pour l'analyse. Lancez d'abord un scraping!")
    
    with tab4:
        st.header("📋 Logs de Scraping")
        
        if st.session_state.scraping_logs:
            log_levels = ['Tous', 'INFO', 'WARNING', 'ERROR']
            selected_level = st.selectbox("Niveau de log", log_levels)
            
            logs_to_show = st.session_state.scraping_logs
            if selected_level != 'Tous':
                logs_to_show = [log for log in logs_to_show if selected_level in log]
            
            st.text_area(
                f"Logs ({len(logs_to_show)} entrées)",
                value='\n'.join(logs_to_show),
                height=400
            )
            
            if st.button("🗑️ Effacer les logs"):
                st.session_state.scraping_logs = []
                st.rerun()
        else:
            st.info("Aucun log disponible.")
    
    with tab5:
        st.header("💬 Chat avec l'Analyseur CoT")
        
        # En-tête principal
        st.markdown("""
        <div class="main-header">
            <h1>🧠 Analyseur Chain of Thought</h1>
            <p>Analyse conversationnelle de vos données produits avec raisonnement explicite</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                    df = None
                    if st.session_state.scraped_products:
                        df = pd.DataFrame(st.session_state.scraped_products)
                        df = st.session_state.chat_interface.validate_data(df)
                    
                    response = st.session_state.chat_interface.handle_chat_query(prompt, df)
                    st.markdown(response)
            
            # Ajouter la réponse à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Visualisations et analyse détaillée
        if st.session_state.scraped_products:
            df = pd.DataFrame(st.session_state.scraped_products)
            df = st.session_state.chat_interface.validate_data(df)
            
            if df is not None:
                # Bouton pour analyse complète
                if st.button("🚀 Analyse CoT Complète", type="primary"):
                    with st.spinner("🔍 Analyse approfondie..."):
                        results = st.session_state.chat_interface.simulate_cot_analysis(df)
                        
                        # Affichage des résultats
                        st.subheader("🎯 Insights Clés")
                        
                        stats = results['data_stats']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Produits analysés", stats['total_products'])
                        with col2:
                            st.metric("Prix moyen", f"{stats['avg_price']:.0f}€")
                        with col3:
                            st.metric("Score médian", f"{stats['median_score']:.3f}")
                        
                        # Recommandations
                        st.subheader("💡 Recommandations")
                        for domain, rec in results['recommendations'].items():
                            st.info(f"**{domain.upper()}**: {rec}")
                
                # Section d'analyse détaillée
                with st.expander("📊 Analyse Détaillée"):
                    st.session_state.chat_interface.generate_visualizations(df)
        
        else:
            st.info("🚀 Scrapez des données depuis l'onglet Scraping pour activer l'analyse conversationnelle!")
    
    st.markdown("---")
    st.markdown("**Application Streamlit - Scraper Agent To Agent avec Chat CoT | Développée par Python & Streamlit")

if __name__ == "__main__":
    main()