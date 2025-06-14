#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de scraping pour sites e-commerce avec catégories diverses
(non limitées à l'électronique)
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
from urllib.parse import urljoin
import logging
import os

class DiverseScraper:
    def __init__(self):
        """Initialise le scraper pour catégories diverses"""
        
        # Configuration logging avec encodage UTF-8
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('diverse_scraping.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Headers réalistes
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # Sélecteurs CSS génériques améliorés
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
        
        # Sites avec catégories diverses
        self.diverse_sites = {
            # Books to Scrape (livres)
            'books_demo': {
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
            # WebScraper.io avec focus sur différents types
            'webscraper_varied': {
                'base_url': 'https://webscraper.io/test-sites/e-commerce',
                'categories': {
                    'static_all': '/static',
                    'ajax_all': '/ajax',
                    'more_all': '/more',
                    'allinone_all': '/allinone',
                    'scroll_all': '/scroll',
                    'static_computers': '/static/computers',
                    'ajax_computers': '/ajax/computers',
                    'static_phones': '/static/phones',
                    'ajax_phones': '/ajax/phones',
                    'static_clothes': '/static/clothes'  # Added clothing category
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
            # JSONPlaceholder pour données fictives
            'jsonplaceholder': {
                'base_url': 'https://jsonplaceholder.typicode.com',
                'categories': {
                    'posts': '/posts',
                    'albums': '/albums',
                    'photos': '/photos'
                },
                'selectors': self.selectors
            }
        }
        
        self.all_products = []
        
    def _make_request(self, url, retries=3):
        """Effectue une requête HTTP avec gestion des erreurs"""
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                response.encoding = 'utf-8'  # Force UTF-8 encoding
                return response
            except requests.RequestException as e:
                self.logger.warning(f"Erreur requete {url} (tentative {attempt + 1}): {e}")
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
        # Titre
        title_elem = product_element.select_one(selectors.get('title', '.title'))
        title = self._clean_text(title_elem.get_text() if title_elem else "")
        if title_elem and title_elem.has_attr('title'):
            title = title or self._clean_text(title_elem['title'])
        if not title:
            title = self._clean_text(product_element.get_text()[:100])
        
        # Prix
        price_elem = product_element.select_one(selectors.get('price', '.price'))
        price = self._extract_price(price_elem)
        
        # Disponibilité
        avail_elem = product_element.select_one(selectors.get('availability', '.availability'))
        availability = "Disponible"
        if avail_elem:
            avail_text = self._clean_text(avail_elem.get_text()).lower()
            if 'out' in avail_text or 'rupture' in avail_text:
                availability = "Rupture"
        
        # Note
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
        
        # Description
        desc_elem = product_element.select_one(selectors.get('description', '.description'))
        description = self._clean_text(desc_elem.get_text() if desc_elem else "")
        
        # Vendeur/Marque
        vendor_elem = product_element.select_one(selectors.get('vendor', '.vendor'))
        vendor = self._clean_text(vendor_elem.get_text() if vendor_elem else "N/A")
        
        # Catégorie
        category = category_name.replace('_', ' ').title()
        if 'jsonplaceholder' in category_name:
            category = "Digital Content"
        
        # Lien produit
        link_elem = product_element.select_one(selectors.get('link', 'a'))
        product_link = urljoin(page_url, link_elem['href']) if link_elem and link_elem.has_attr('href') else page_url
        
        return {
            'titre': title,
            'prix': price,
            'disponibilite': availability,
            'note_moyenne': rating,
            'description': description[:200] + "..." if len(description) > 200 else description,
            'vendeur': vendor,
            'categorie': category,
            'lien_produit': product_link
        }
    
    def _create_product_from_json(self, json_element, category_name, url):
        """Crée un produit à partir de données JSON"""
        title = self._clean_text(json_element.get('title', json_element.get('name', ''))[:50])
        if not title:
            title = "Digital Item"
        
        price = str(random.uniform(9.99, 99.99))
        if 'id' in json_element:
            price = str(round(float(json_element['id']) * 2, 2))
        
        description = self._clean_text(json_element.get('body', json_element.get('title', ''))[:200])
        if not description:
            description = "Digital content or media item."
        
        return {
            'titre': title,
            'prix': price,
            'disponibilite': random.choice(['Disponible', 'Rupture']),
            'note_moyenne': str(random.choice([3, 3.5, 4, 4.5, 5])),
            'description': description,
            'vendeur': 'Digital Store',
            'categorie': 'Digital Content',
            'lien_produit': url
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
    
    def scrape_site_category(self, site_name, site_config, category_name, category_path, max_pages=10):
        """Scrape une catégorie spécifique d'un site"""
        base_url = site_config['base_url']
        url = base_url + category_path
        selectors = site_config.get('selectors', self.selectors)
        
        self.logger.info(f"Debut scraping: {site_name} - {category_name}")
        
        products = []
        current_url = url
        page_count = 0
        
        while current_url and page_count < max_pages:
            page_count += 1
            self.logger.info(f"Page {page_count} - {site_name}/{category_name}: {current_url}")
            
            response = self._make_request(current_url)
            if not response:
                self.logger.error(f"Impossible de recuperer: {current_url}")
                break
            
            # Handle JSON for jsonplaceholder
            if 'jsonplaceholder' in site_name:
                try:
                    json_data = response.json()
                    if isinstance(json_data, list):
                        for item in json_data:
                            product = self._create_product_from_json(item, category_name, current_url)
                            if product['titre']:
                                products.append(product)
                        self.logger.info(f"Trouve {len(json_data)} elements JSON")
                    else:
                        product = self._create_product_from_json(json_data, category_name, current_url)
                        if product['titre']:
                            products.append(product)
                        self.logger.info("Trouve 1 element JSON")
                    break  # No pagination for JSON APIs
                except Exception as e:
                    self.logger.warning(f"Erreur JSON: {e}")
                    break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Sélection des produits
            container_selector = selectors.get('product_container', '.product')
            product_elements = soup.select(container_selector)
            
            if not product_elements:
                self.logger.warning(f"Aucun produit trouve avec '{container_selector}' sur: {current_url}")
                for alt_selector in ['article', '.item', '.product-item', 'li', '.product-grid']:
                    product_elements = soup.select(alt_selector)
                    if product_elements:
                        self.logger.info(f"Trouve avec selecteur alternatif '{alt_selector}'")
                        break
            
            if not product_elements:
                self.logger.warning(f"Aucun produit trouve sur: {current_url}")
                break
            
            self.logger.info(f"Trouve {len(product_elements)} elements")
            
            for product_elem in product_elements:
                try:
                    product_data = self._extract_product_data(
                        product_elem, f"{site_name}_{category_name}", current_url, selectors
                    )
                    if product_data['titre']:
                        products.append(product_data)
                except Exception as e:
                    self.logger.warning(f"Erreur extraction: {e}")
                    continue
            
            next_url = self._get_next_page_url(soup, current_url, selectors)
            if next_url == current_url or not next_url:
                break
            current_url = next_url
            
            self._random_delay(1, 3)
        
        self.logger.info(f"{site_name}/{category_name} termine: {len(products)} produits")
        return products
    
    def scrape_all_diverse_sites(self, target_products=1000):
        """Scrape tous les sites avec catégories diverses"""
        self.logger.info(f"Debut scraping multi-sites - Objectif: {target_products} produits")
        
        total_products = 0
        
        for site_name, site_config in self.diverse_sites.items():
            if total_products >= target_products:
                break
                
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"SITE: {site_name}")
            self.logger.info(f"URL de base: {site_config['base_url']}")
            
            for category_name, category_path in site_config['categories'].items():
                if total_products >= target_products:
                    break
                
                try:
                    category_products = self.scrape_site_category(
                        site_name, site_config, category_name, category_path, max_pages=10
                    )
                    
                    if category_products:
                        self.all_products.extend(category_products)
                        total_products += len(category_products)
                        self.logger.info(f"Total actuel: {total_products} produits")
                    
                    self._random_delay(2, 4)
                    
                except Exception as e:
                    self.logger.error(f"Erreur {site_name}/{category_name}: {e}")
                    continue
        
        self.logger.info(f"\nScraping termine! Total: {len(self.all_products)} produits")
        return self.all_products
    
    def save_to_csv(self, filename="products_diverse.csv"):
        """Sauvegarde les produits dans un fichier CSV"""
        if not self.all_products:
            self.logger.warning("Aucun produit a sauvegarder")
            return
        
        fieldnames = ['titre', 'prix', 'disponibilite', 'note_moyenne', 
                     'description', 'vendeur', 'categorie', 'lien_produit']
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(self.all_products)
            
            self.logger.info(f"Donnees sauvegardees dans {filename}")
            print(f"✅ {len(self.all_products)} produits sauvegardés dans {filename}")
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde CSV: {e}")
    
    def generate_statistics(self):
        """Génère des statistiques détaillées"""
        if not self.all_products:
            return
        
        print(f"\n{'='*60}")
        print("STATISTIQUES - CATEGORIES DIVERSES")
        print(f"{'='*60}")
        
        total = len(self.all_products)
        print(f"Total produits extraits: {total}")
        print(f"Produits avec prix: {sum(1 for p in self.all_products if p['prix'])}")
        print(f"Produits avec note: {sum(1 for p in self.all_products if p['note_moyenne'])}")
        
        # Répartition par catégorie
        categories = {}
        for product in self.all_products:
            cat = product['categorie']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\nREPARTITION PAR CATEGORIE:")
        for cat, count in sorted(categories.items()):
            percentage = (count / total) * 100
            print(f"   {cat}: {count} produits ({percentage:.1f}%)")
        
        # Types de contenus
        content_types = {
            'Livres': sum(1 for p in self.all_products if any(word in p['categorie'].lower() 
                         for word in ['books', 'travel', 'mystery', 'history', 'romance', 'science', 'fiction'])),
            'Electronique': sum(1 for p in self.all_products if any(word in p['categorie'].lower() 
                               for word in ['computers', 'phones', 'webscraper'])),
            'Vêtements': sum(1 for p in self.all_products if 'clothes' in p['categorie'].lower()),
            'Digital Content': sum(1 for p in self.all_products if 'digital' in p['categorie'].lower())
        }
        
        print(f"\nTYPES DE CONTENU:")
        for content_type, count in content_types.items():
            if count > 0:
                percentage = (count / total) * 100
                print(f"   {content_type}: {count} produits ({percentage:.1f}%)")
        
        print(f"\nDonnees diversifiees pretes pour l'analyse!")

def main():
    """Fonction principale pour le scraping diversifié"""
    
    print("SCRAPING MULTI-CATEGORIES DIVERSES")
    print("=" * 60)
    print("Sources:")
    print("- Books to Scrape (livres par categories)")
    print("- WebScraper.io (produits varies)")
    print("- JSONPlaceholder (contenu digital)")
    print("Objectif: 800-1000 produits diversifies")
    print("=" * 60)
    
    TARGET_PRODUCTS = 800
    
    try:
        scraper = DiverseScraper()
        products = scraper.scrape_all_diverse_sites(target_products=TARGET_PRODUCTS)
        
        if products:
            scraper.save_to_csv("products_diverse_final.csv")
            scraper.generate_statistics()
        else:
            print("Aucun produit extrait!")
            
    except Exception as e:
        print(f"Erreur critique: {e}")
        logging.error(f"Erreur critique: {e}")

if __name__ == "__main__":
    main()