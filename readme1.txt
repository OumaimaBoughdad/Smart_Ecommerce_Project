# Projet Smart eCommerce

## Vue d'ensemble
Ce projet implémente un pipeline complet d'analyse de données pour les produits e-commerce, depuis l'extraction web jusqu'à l'analyse avancée et l'intégration d'IA responsable. Le pipeline se compose de quatre composants principaux qui fonctionnent ensemble pour extraire, traiter, analyser et présenter des insights à partir des données de produits e-commerce.

## Composants

### 1. Agent de Scraping
Un système flexible d'extraction web qui collecte des données de produits à partir de plusieurs sites e-commerce dans différentes catégories (livres, électronique, vêtements, etc.). Le scraper recueille les détails des produits, notamment le titre, le prix, la disponibilité, la note, et plus encore.

**Fonctionnalités clés:**
- Support multi-catégories et multi-sites
- Sélecteurs CSS flexibles pour l'adaptabilité
- Gestion des erreurs et journalisation
- Génération de statistiques

### 2. Analyse et Sélection des Top-K Produits
Un module d'analyse de données qui traite les données de produits extraites pour identifier les produits les plus attractifs selon plusieurs critères. Ce composant utilise des techniques statistiques avancées pour classer et sélectionner les meilleurs produits.

**Fonctionnalités clés:**
- Nettoyage et prétraitement des données
- Normalisation des caractéristiques et scoring
- Analyses avancées (ACP, clustering K-Means)
- Modélisation prédictive avec Random Forest
- Visualisation des classements de produits

### 3. LLM pour Enrichissement et Synthèse
Un module qui exploite les Grands Modèles de Langage (LLM) pour enrichir l'analyse avec des insights stratégiques et des recommandations. Ce composant utilise le raisonnement Chain of Thought (CoT) pour fournir une analyse structurée et des recommandations actionnables.

**Fonctionnalités clés:**
- Cadre d'analyse Chain of Thought
- Interface interactive Streamlit
- Visualisation de données avec Plotly
- Recommandations stratégiques pour la tarification, l'inventaire et le marketing
- Export des traces de raisonnement pour la transparence

### 4. Architecture Responsable avec Model Context Protocol
Un cadre de sécurité et d'éthique qui implémente le Model Context Protocol (MCP) pour garantir une utilisation responsable de l'IA. Ce composant fournit la traçabilité, la gestion des permissions et l'isolation des opérations pour l'ensemble du pipeline.

**Fonctionnalités clés:**
- Journalisation complète des requêtes dans une base de données SQLite
- Gestion des permissions avec différents niveaux d'accès
- Architecture modulaire avec composants MCP
- Capacités d'audit

## Pipeline DevOps

Le projet inclut également un pipeline DevOps complet avec:

1. **Dockerisation** des trois composants principaux
2. **CI/CD avec GitHub Actions** pour les tests automatisés et le déploiement
3. **Pipeline Kubeflow** pour l'orchestration des tâches ML
4. **Déploiement Kubernetes local** avec Minikube

## Technologies Utilisées
- **Python**: Langage de programmation principal
- **Pandas/NumPy**: Manipulation et analyse de données
- **Scikit-learn**: Algorithmes d'apprentissage automatique
- **Transformers (Hugging Face)**: Intégration LLM
- **Streamlit**: Interface utilisateur interactive
- **Plotly**: Visualisation de données
- **SQLite**: Journalisation d'audit
- **Docker/Kubernetes**: Conteneurisation et orchestration
- **Kubeflow**: Pipelines ML

## Démarrage
Chaque composant possède son propre fichier README avec des instructions d'installation et d'utilisation spécifiques. Veuillez consulter les répertoires des composants individuels pour des informations détaillées.