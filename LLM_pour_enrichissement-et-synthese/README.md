# Analyseur Chain of Thought (CoT) - Étape 5 : Enrichissement et Synthèse avec LLM



Ce dépôt contient l'implémentation de l'étape 5 du projet, qui utilise un modèle de langage large (LLM) pour enrichir l'analyse des données produits et générer des recommandations stratégiques basées sur un raisonnement structuré (Chain of Thought).

## 📋 Description

L'objectif de cette étape est d'analyser un ensemble de données produits (extraites via scraping dans les étapes précédentes) et de produire des insights et recommandations exploitables. L'approche utilise un raisonnement explicite (Chain of Thought) pour structurer l'analyse, et une interface conversationnelle Streamlit pour interagir avec les résultats.

## ✨ Fonctionnalités principales

- **Chargement et validation des données** : Vérification des colonnes requises et de la qualité des données
- **Analyse CoT** : Analyse structurée en 4 étapes (observation, identification des patterns, analyse des corrélations, évaluation des implications)
- **Recommandations stratégiques** : Suggestions basées sur le raisonnement pour le pricing, les vendeurs, l'inventaire, et le marketing
- **Résumé exécutif** : Synthèse claire des insights et recommandations
- **Interface Streamlit** : Interface utilisateur interactive avec visualisations (via Plotly) et chat conversationnel
- **Export de la trace de raisonnement** : Documentation complète des étapes de raisonnement en JSON

## 🛠️ Technologies utilisées

### Langages et Frameworks
- **Python 3.8+** : Langage principal pour l'analyse et l'interface
- **Streamlit** : Framework pour l'interface utilisateur interactive et conversationnelle
- **Pandas** : Manipulation et analyse des données
- **NumPy** : Calculs numériques pour l'analyse statistique
- **Plotly** : Visualisations interactives (histogrammes, graphiques en barres, scatter plots)

### Bibliothèques ML/LLM
- **Transformers (Hugging Face)** : Pipeline de génération de texte pour le raisonnement CoT (modèle DialoGPT-medium)
- **TensorFlow** : Utilisé en arrière-plan pour gérer les avertissements et les calculs liés au modèle
- **LangChain (optionnel)** : Non utilisé directement dans ce code, mais mentionné comme outil potentiel pour orchestrer des appels complexes à des LLMs

### Autres outils
- **JSON** : Pour l'exportation des traces de raisonnement
- **Datetime** : Gestion des horodatages pour la traçabilité
- **OS** : Gestion des chemins de fichiers
- **Warnings** : Gestion des avertissements pour une exécution propre

## 📋 Prérequis

Pour exécuter ce projet, assurez-vous d'avoir les dépendances suivantes installées :

```
python>=3.8
streamlit>=1.20.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.10.0
transformers>=4.30.0
tensorflow>=2.10.0
```

## 🚀 Installation

### 1. Cloner le dépôt
```bash
git clone <url-du-dépôt>
cd <nom-du-dépôt>
```

### 2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```
streamlit==1.20.0
pandas==1.5.3
numpy==1.23.5
plotly==5.10.0
transformers==4.30.2
tensorflow==2.10.0
```

## 📁 Structure du dépôt

```
├── cot_analysis.py                          # Script principal pour l'analyse CoT
├── app_streamlit.py                # Interface Streamlit pour l'interaction conversationnelle
├── top_produits_attractifs.csv      # Exemple de fichier de données (non inclus, à fournir)
├── rapport_cot_20250611_173142.txt
├── cot_reasoning_trace_20250611_173142.json
└── README.md                        
```

## 🏃‍♂️ Comment exécuter le code

### 1. Préparer les données

Fournissez un fichier CSV nommé `top_produits_attractifs.csv` avec les colonnes suivantes :
- **titre** : Nom du produit (chaîne de caractères)
- **prix** : Prix du produit (nombre)
- **note_moyenne** : Note moyenne des avis (nombre)
- **vendeur** : Nom du vendeur (chaîne de caractères)
- **disponibilite** : Statut de disponibilité (ex : "En stock", "Rupture")
- **score_global** : Score synthétique calculé (nombre)

Placez ce fichier dans le répertoire racine du projet.

### 2. Exécuter l'analyseur principal

Pour lancer l'analyse complète avec exportation des résultats :

```bash
python cot_analysis.py
```

Cela exécutera l'analyse Chain of Thought complète, affichera un résumé exécutif, et exportera la trace de raisonnement dans un fichier JSON (`cot_reasoning_trace_*.json`).
Un rapport simplifié sera également généré sous la forme `rapport_cot_*.txt`.

### 3. Lancer l'interface Streamlit

Pour interagir avec l'analyseur via l'interface conversationnelle :

```bash
streamlit run app_streamlit.py
```

- Une interface web s'ouvrira dans votre navigateur
- Uploadez le fichier CSV via la barre latérale
- Posez des questions dans la zone de chat (ex : "Analyse les prix", "Quels sont mes meilleurs vendeurs ?")
- Consultez les visualisations interactives et les recommandations générées

## 🤖 Pipeline Transformers utilisé

Le pipeline de Transformers (Hugging Face) est utilisé dans la classe `ChainOfThoughtAnalyzer` pour générer un raisonnement textuel structuré.

### Détails du pipeline

- **Modèle** : `microsoft/DialoGPT-medium`
  - Type : Modèle de dialogue basé sur GPT-2, pré-entraîné pour la génération de texte conversationnel
  - Taille : Moyen (~355M paramètres), adapté pour un équilibre entre performance et ressources

- **Tâche** : `text-generation`
  - Utilisé pour générer des réponses textuelles cohérentes dans le cadre du raisonnement CoT

- **Configuration** :
  - `max_length=400` : Limite la longueur des réponses générées à 400 tokens
  - `do_sample=True` : Active l'échantillonnage pour introduire une certaine variabilité
  - `temperature=0.3` : Faible température pour des réponses conservatrices et cohérentes
  - `top_p=0.9` : Filtrage par probabilité cumulative pour améliorer la qualité du texte

### Rôle dans le projet

Le pipeline est intégré dans la méthode `__init__` de `ChainOfThoughtAnalyzer` pour initialiser un générateur de texte capable de produire des analyses structurées. Il est utilisé pour remplir des templates de raisonnement CoT en générant des explications textuelles basées sur les données analysées.

### Exemple d'utilisation
```python
self.text_generator = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-medium",
    tokenizer="microsoft/DialoGPT-medium",
    max_length=400,
    do_sample=True,
    temperature=0.3,
    top_p=0.9
)
```

### Limites

- Le modèle DialoGPT-medium est optimisé pour le dialogue et peut nécessiter un réglage fin pour des analyses plus spécifiques au domaine
- La génération peut être limitée par la qualité des prompts fournis (prompt engineering)
- Les performances dépendent des ressources matérielles (GPU recommandé pour une exécution rapide)

## 💬 Utilisation de l'interface Streamlit

### Fonctionnalités

- **Upload de fichier** : Chargez un fichier CSV pour lancer l'analyse
- **Chat conversationnel** : Posez des questions sur les prix, les vendeurs, les stocks, ou demandez des recommandations
- **Visualisations** : Graphiques interactifs (distribution des prix, scores par vendeur, relation prix-performance)
- **Analyse complète** : Bouton pour générer une analyse CoT détaillée avec recommandations

### Exemples de requêtes

- "Analyse les prix de mes produits"
- "Quels sont mes meilleurs vendeurs ?"
- "Donne-moi des recommandations marketing"
- "Comment optimiser mon inventaire ?"

  ### interface chat
  ![Capture d’écran 2025-06-11 190835](https://github.com/user-attachments/assets/ffd0c7b8-9bbb-463f-b33b-8d08a478d4bd)
  ![Capture d’écran 2025-06-11 190917](https://github.com/user-attachments/assets/aa968827-a7f6-445b-9be9-448afb228e3f)
  ![Capture d’écran 2025-06-11 191018](https://github.com/user-attachments/assets/62cd1938-dd79-430a-b541-bfff7e2ea085)





## 🔮 Prochaines étapes

- **Intégration avec Kubeflow** : Connecter l'analyseur aux pipelines ML des étapes précédentes
- **Ajout de MCP** : Implémenter le Model Context Protocol pour une interaction responsable (étape 6)
- **Tests automatisés** : Ajouter des tests unitaires pour valider les composants

## 🤝 Contribution

1. Forkez le dépôt
2. Créez une branche pour vos modifications (`git checkout -b feature/nouvelle-fonction`)
3. Commitez vos changements (`git commit -m "Ajout de nouvelle fonctionnalité"`)
4. Poussez votre branche (`git push origin feature/nouvelle-fonction`)
5. Créez une Pull Request

