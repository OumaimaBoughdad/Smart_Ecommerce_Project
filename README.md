# F1 Project: E-commerce Data Analysis Pipeline

## Project Overview
This project implements a complete data pipeline for e-commerce product analysis, from web scraping to advanced analytics and responsible AI integration. The pipeline consists of four main components that work together to extract, process, analyze, and present insights from e-commerce product data.

## Components

### 1. Agent Scraping
A flexible web scraping system that extracts product data from multiple e-commerce websites across different categories (books, electronics, clothing, etc.). The scraper collects product details including title, price, availability, rating, and more.

**Key Features:**
- Multi-category and multi-website support
- Flexible CSS selectors for adaptability
- Error handling and logging
- Statistics generation

### 2. Analyse et Sélection des Top-K Produits
A data analysis module that processes the scraped product data to identify the most attractive products based on multiple criteria. This component uses advanced statistical techniques to rank and select the top products.

**Key Features:**
- Data cleaning and preprocessing
- Feature normalization and scoring
- Advanced analytics (PCA, K-Means clustering)
- Predictive modeling with Random Forest
- Visualization of product rankings

### 3. LLM pour Enrichissement et Synthèse
A module that leverages Large Language Models (LLMs) to enrich the analysis with strategic insights and recommendations. This component uses Chain of Thought (CoT) reasoning to provide structured analysis and actionable recommendations.

**Key Features:**
- Chain of Thought analysis framework
- Interactive Streamlit interface
- Data visualization with Plotly
- Strategic recommendations for pricing, inventory, and marketing
- Export of reasoning traces for transparency

### 4. Architecture Responsable avec Model Context Protocol
A security and ethics framework that implements the Model Context Protocol (MCP) to ensure responsible AI usage. This component provides traceability, permission management, and operation isolation for the entire pipeline.

**Key Features:**
- Complete request logging in SQLite database
- Permission management with different access levels
- Modular architecture with MCP components
- Audit capabilities

## Technologies Used
- **Python**: Core programming language
- **Pandas/NumPy**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms
- **Transformers (Hugging Face)**: LLM integration
- **Streamlit**: Interactive user interface
- **Plotly**: Data visualization
- **SQLite**: Audit logging

## Getting Started
Each component has its own README file with specific installation and usage instructions. Please refer to the individual component directories for detailed information:

- [Agent Scraping](./agent_scraping/README.md)
- [Analyse et Sélection des Top-K Produits](./Analyse-et-s-lection-des-Top-K-produits/README.md)
- [LLM pour Enrichissement et Synthèse](./LLM_pour_enrichissement-et-synthese/README.md)
- [Architecture Responsable avec Model Context Protocol](./Architecture_responsable_avec_Model_Context_Protocol-/README.md)

## Project Workflow
1. **Data Collection**: Web scraping of e-commerce products
2. **Data Processing**: Cleaning, normalization, and scoring
3. **Advanced Analysis**: Selection of top products using statistical methods
4. **LLM Enhancement**: Enrichment with AI-powered insights and recommendations
5. **Responsible Deployment**: Implementation of security and ethics framework

## License
Each component includes its own LICENSE file. Please refer to these files for licensing information.