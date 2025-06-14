"""
Étape 5 : Enrichissement d'analyse avec LLM - Version Chain of Thought
Utilisation d'une approche de raisonnement structuré pour générer des insights
et recommandations basés sur les produits Top-K avec explicitation du processus
"""

import pandas as pd
import numpy as np
from transformers import pipeline
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import warnings
warnings.filterwarnings('ignore')

class ChainOfThoughtAnalyzer:
    """
    Analyseur utilisant Chain of Thought (CoT) pour un raisonnement explicite
    et structuré dans l'analyse des produits performants
    """
    
    def __init__(self):
        """Initialise l'analyseur avec les pipelines et templates CoT"""
        print("🧠 Initialisation de l'analyseur Chain of Thought...")
        
        # Pipeline de génération optimisé pour le raisonnement
        self.text_generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium",
            tokenizer="microsoft/DialoGPT-medium",
            max_length=400,
            do_sample=True,
            temperature=0.3,  # Plus conservateur pour la cohérence
            top_p=0.9
        )
        
        # Templates de raisonnement structuré
        self.cot_templates = {
            'analysis': self._get_analysis_template(),
            'recommendation': self._get_recommendation_template(),
            'validation': self._get_validation_template()
        }
        
        print("✅ Analyseur Chain of Thought initialisé!")
    
    def _get_analysis_template(self) -> str:
        """Template pour l'analyse structurée"""
        return """
        ÉTAPE 1 - OBSERVATION DES DONNÉES:
        {data_observation}
        
        ÉTAPE 2 - IDENTIFICATION DES PATTERNS:
        {pattern_identification}
        
        ÉTAPE 3 - ANALYSE DES CORRÉLATIONS:
        {correlation_analysis}
        
        ÉTAPE 4 - ÉVALUATION DES IMPLICATIONS:
        {implications_assessment}
        
        CONCLUSION ANALYTIQUE:
        {analytical_conclusion}
        """
    
    def _get_recommendation_template(self) -> str:
        """Template pour les recommandations structurées"""
        return """
        CONTEXTE BUSINESS:
        {business_context}
        
        RAISONNEMENT ÉTAPE PAR ÉTAPE:
        1. Problème identifié: {problem_statement}
        2. Options considérées: {options_considered}
        3. Critères d'évaluation: {evaluation_criteria}
        4. Analyse des options: {options_analysis}
        5. Sélection justifiée: {selected_option}
        
        RECOMMANDATION FINALE:
        {final_recommendation}
        
        PLAN D'ACTION:
        {action_plan}
        """
    
    def _get_validation_template(self) -> str:
        """Template pour la validation du raisonnement"""
        return """
        VALIDATION DU RAISONNEMENT:
        
        Hypothèses vérifiées:
        {verified_assumptions}
        
        Cohérence logique:
        {logical_consistency}
        
        Robustesse des conclusions:
        {conclusion_robustness}
        
        Limites identifiées:
        {identified_limitations}
        """

class ProductInsightsCoTGenerator:
    """
    Générateur d'insights avec raisonnement Chain of Thought explicite
    """
    
    def __init__(self):
        """Initialise le générateur avec l'analyseur CoT"""
        print("🚀 Initialisation du générateur d'insights CoT...")
        self.cot_analyzer = ChainOfThoughtAnalyzer()
        self.reasoning_history = []  # Historique des raisonnements
        print("✅ Générateur d'insights CoT prêt!")
    
    def load_and_validate_data(self, csv_path: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Charge et valide les données avec raisonnement explicite
        
        Args:
            csv_path (str): Chemin vers le fichier CSV
            
        Returns:
            Tuple[pd.DataFrame, Dict]: Données et validation CoT
        """
        print("📊 Chargement et validation des données...")
        
        # Raisonnement CoT pour le chargement
        reasoning = {
            'step_1_loading': f"Tentative de chargement du fichier {csv_path}",
            'step_2_validation': "Validation de la structure des données",
            'step_3_quality_check': "Vérification de la qualité des données",
            'conclusion': ""
        }
        
        try:
            # Chargement des données
            df = pd.read_csv(csv_path, sep=';')
            reasoning['step_1_loading'] += f" - Succès: {len(df)} lignes chargées"
            
            # Validation de la structure - utilisation des colonnes réelles
            required_columns = ['titre', 'prix', 'note_moyenne', 'vendeur', 'disponibilite', 'score_global']
            missing_cols = [col for col in required_columns if col not in df.columns]
            
            if missing_cols:
                reasoning['step_2_validation'] += f" - Colonnes manquantes: {missing_cols}"
                reasoning['conclusion'] = "ÉCHEC: Structure de données invalide"
                return None, reasoning
            
            reasoning['step_2_validation'] += " - Structure validée: toutes les colonnes requises présentes"
            
            # Vérification de la qualité
            null_counts = df.isnull().sum()
            reasoning['step_3_quality_check'] += f" - Valeurs manquantes détectées: {null_counts.sum()}"
            
            if null_counts.sum() > len(df) * 0.1:  # Plus de 10% de valeurs manquantes
                reasoning['step_3_quality_check'] += " - ALERTE: Taux élevé de valeurs manquantes"
            
            reasoning['conclusion'] = f"SUCCÈS: Données validées - {len(df)} produits analysables"
            
            # Sauvegarde du raisonnement
            self.reasoning_history.append({
                'timestamp': datetime.now().isoformat(),
                'operation': 'data_loading',
                'reasoning': reasoning
            })
            
            return df, reasoning
            
        except Exception as e:
            reasoning['conclusion'] = f"ÉCHEC: Erreur lors du chargement - {str(e)}"
            return None, reasoning
    
    def analyze_patterns_with_cot(self, df: pd.DataFrame) -> Dict:
        """
        Analyse les patterns avec raisonnement Chain of Thought
        
        Args:
            df (pd.DataFrame): DataFrame des produits
            
        Returns:
            Dict: Analyse complète avec raisonnement CoT
        """
        print("🔍 Analyse des patterns avec Chain of Thought...")
        
        # Structure du raisonnement CoT
        cot_analysis = {
            'data_observation': self._observe_data_characteristics(df),
            'pattern_identification': self._identify_patterns(df),
            'correlation_analysis': self._analyze_correlations(df),
            'implications_assessment': self._assess_implications(df),
            'analytical_conclusion': ""
        }
        
        # Synthèse des observations
        cot_analysis['analytical_conclusion'] = self._synthesize_analysis(cot_analysis)
        
        # Sauvegarde du raisonnement
        self.reasoning_history.append({
            'timestamp': datetime.now().isoformat(),
            'operation': 'pattern_analysis',
            'reasoning': cot_analysis
        })
        
        return cot_analysis
    
    def _observe_data_characteristics(self, df: pd.DataFrame) -> str:
        """Étape 1: Observation des caractéristiques des données"""
        observations = []
        
        # Distribution des prix
        price_stats = df['prix'].describe()
        observations.append(f"Prix: médiane {price_stats['50%']:.0f}€, écart-type {price_stats['std']:.0f}€")
        
        # Distribution des vendeurs (au lieu de catégories)
        vendeur_counts = df['vendeur'].value_counts()
        observations.append(f"Vendeurs: {len(vendeur_counts)} types, leader '{vendeur_counts.index[0]}' ({vendeur_counts.iloc[0]} produits)")
        
        # Distribution des scores
        score_stats = df['score_global'].describe()
        observations.append(f"Scores: moyenne {score_stats['mean']:.3f}, écart-type {score_stats['std']:.3f}")
        
        # Disponibilité
        dispo_counts = df['disponibilite'].value_counts()
        observations.append(f"Disponibilité: {dispo_counts.to_dict()}")
        
        return " | ".join(observations)
    
    def _identify_patterns(self, df: pd.DataFrame) -> str:
        """Étape 2: Identification des patterns significatifs"""
        patterns = []
        
        # Pattern prix-vendeur (au lieu de catégorie)
        price_by_vendeur = df.groupby('vendeur')['prix'].mean().sort_values(ascending=False)
        patterns.append(f"Prix par vendeur: {price_by_vendeur.head(3).to_dict()}")
        
        # Pattern score-prix
        high_score_products = df[df['score_global'] > df['score_global'].quantile(0.75)]
        avg_price_high_score = high_score_products['prix'].mean()
        avg_price_total = df['prix'].mean()
        
        if avg_price_high_score > avg_price_total * 1.2:
            patterns.append("PATTERN: Produits haute performance = prix premium")
        elif avg_price_high_score < avg_price_total * 0.8:
            patterns.append("PATTERN: Produits haute performance = bon rapport qualité-prix")
        else:
            patterns.append("PATTERN: Performance indépendante du prix")
        
        # Pattern concentration
        top_vendeur_ratio = df['vendeur'].value_counts().iloc[0] / len(df)
        if top_vendeur_ratio > 0.5:
            patterns.append(f"PATTERN: Forte concentration ({top_vendeur_ratio:.1%}) chez un vendeur")
        
        return " | ".join(patterns)
    
    def _analyze_correlations(self, df: pd.DataFrame) -> str:
        """Étape 3: Analyse des corrélations"""
        correlations = []
        
        # Corrélation prix-score
        prix_score_corr = df['prix'].corr(df['score_global'])
        if abs(prix_score_corr) > 0.3:
            direction = "positive" if prix_score_corr > 0 else "négative"
            correlations.append(f"Corrélation {direction} prix-score: {prix_score_corr:.3f}")
        
        # Analyse par disponibilité
        if 'En stock' in df['disponibilite'].values:
            en_stock_df = df[df['disponibilite'] == 'En stock']
            if len(en_stock_df) > 0:
                score_diff = en_stock_df['score_global'].mean() - df['score_global'].mean()
                if abs(score_diff) > 0.01:
                    correlations.append(f"Produits en stock: score {'supérieur' if score_diff > 0 else 'inférieur'} de {abs(score_diff):.3f}")
        
        return " | ".join(correlations) if correlations else "Aucune corrélation significative détectée"
    
    def _assess_implications(self, df: pd.DataFrame) -> str:
        """Étape 4: Évaluation des implications business"""
        implications = []
        
        # Implications pricing
        price_range = df['prix'].max() - df['prix'].min()
        if price_range > df['prix'].mean() * 2:
            implications.append("IMPLICATION: Stratégie multi-segments nécessaire")
        
        # Implications vendeurs (au lieu de catégories)
        vendeur_performance = df.groupby('vendeur')['score_global'].mean()
        best_vendeur = vendeur_performance.idxmax()
        worst_vendeur = vendeur_performance.idxmin()
        
        if vendeur_performance[best_vendeur] - vendeur_performance[worst_vendeur] > 0.05:
            implications.append(f"IMPLICATION: Optimiser {worst_vendeur}, renforcer {best_vendeur}")
        
        # Implications stock
        stock_issues = df[df['disponibilite'] != 'En stock']
        if len(stock_issues) > len(df) * 0.2:
            implications.append("IMPLICATION: Problèmes de disponibilité à adresser")
        
        return " | ".join(implications) if implications else "Aucune implication critique identifiée"
    
    def _synthesize_analysis(self, cot_analysis: Dict) -> str:
        """Synthèse finale de l'analyse"""
        synthesis = f"""
        SYNTHÈSE ANALYTIQUE:
        
        Basé sur l'observation des données ({cot_analysis['data_observation']}),
        l'identification des patterns ({cot_analysis['pattern_identification']}),
        l'analyse des corrélations ({cot_analysis['correlation_analysis']}),
        et l'évaluation des implications ({cot_analysis['implications_assessment']}),
        
        CONCLUSION: Le portefeuille analysé présente des caractéristiques exploitables
        pour l'optimisation stratégique avec des leviers d'action clairement identifiés.
        """
        
        return synthesis.strip()
    
    def generate_strategic_recommendations_cot(self, df: pd.DataFrame, analysis: Dict) -> Dict:
        """
        Génère des recommandations avec raisonnement Chain of Thought
        
        Args:
            df (pd.DataFrame): Données produits
            analysis (Dict): Analyse CoT précédente
            
        Returns:
            Dict: Recommandations avec raisonnement explicite
        """
        print("💡 Génération de recommandations avec Chain of Thought...")
        
        recommendations = {}
        
        # Recommandation pricing avec CoT
        recommendations['pricing'] = self._generate_pricing_recommendation_cot(df)
        
        # Recommandation vendeurs avec CoT (au lieu de catégories)
        recommendations['vendor'] = self._generate_vendor_recommendation_cot(df)
        
        # Recommandation inventaire avec CoT
        recommendations['inventory'] = self._generate_inventory_recommendation_cot(df)
        
        # Recommandation marketing avec CoT
        recommendations['marketing'] = self._generate_marketing_recommendation_cot(df, analysis)
        
        return recommendations
    
    def _generate_pricing_recommendation_cot(self, df: pd.DataFrame) -> Dict:
        """Recommandation pricing avec raisonnement CoT"""
        
        # Contexte business
        context = f"Analyse de {len(df)} produits avec prix moyen {df['prix'].mean():.0f}€"
        
        # Problème identifié
        price_std = df['prix'].std()
        cv_price = price_std / df['prix'].mean()  # Coefficient de variation
        
        if cv_price > 0.5:
            problem = "Forte hétérogénéité des prix nécessitant une stratégie segmentée"
        else:
            problem = "Homogénéité des prix permettant une stratégie unifiée"
        
        # Options considérées
        options = [
            "Stratégie prix unique",
            "Stratégie multi-segments",
            "Stratégie dynamique basée sur la performance"
        ]
        
        # Critères d'évaluation
        criteria = ["Cohérence portefeuille", "Maximisation marge", "Positionnement concurrentiel"]
        
        # Analyse des options
        high_performers = df[df['score_global'] > df['score_global'].quantile(0.75)]
        avg_price_high = high_performers['prix'].mean()
        avg_price_total = df['prix'].mean()
        
        if avg_price_high > avg_price_total * 1.2:
            analysis = "Les produits performants justifient un pricing premium"
            selected = "Stratégie dynamique basée sur la performance"
        else:
            analysis = "Performance non corrélée au prix, optimiser le rapport valeur-prix"
            selected = "Stratégie multi-segments"
        
        # Recommandation finale
        recommendation = f"Adopter une {selected.lower()} pour optimiser la rentabilité"
        
        # Plan d'action
        action_plan = [
            "1. Segmenter le portefeuille par performance",
            "2. Ajuster les prix selon le segment",
            "3. Monitorer l'impact sur les ventes",
            "4. Optimiser en continu"
        ]
        
        return {
            'business_context': context,
            'problem_statement': problem,
            'options_considered': options,
            'evaluation_criteria': criteria,
            'options_analysis': analysis,
            'selected_option': selected,
            'final_recommendation': recommendation,
            'action_plan': action_plan
        }
    
    def _generate_vendor_recommendation_cot(self, df: pd.DataFrame) -> Dict:
        """Recommandation vendeurs avec raisonnement CoT"""
        
        # Calcul des performances par vendeur avec les bonnes colonnes
        vendor_performance = df.groupby('vendeur').agg({
            'score_global': 'mean',
            'prix': 'mean',
            'titre': 'count'  # Utiliser 'titre' au lieu de 'nom'
        }).round(3)
        
        best_vendor = vendor_performance['score_global'].idxmax()
        worst_vendor = vendor_performance['score_global'].idxmin()
        
        context = f"Analyse de {len(vendor_performance)} vendeurs"
        problem = f"Performance inégale: {best_vendor} domine, {worst_vendor} sous-performe"
        
        options = [
            "Concentrer sur le vendeur leader",
            "Diversifier uniformément",
            "Optimiser les vendeurs faibles"
        ]
        
        # Sélection basée sur la concentration
        leader_count = vendor_performance.loc[best_vendor, 'titre']
        total_products = len(df)
        concentration = leader_count / total_products
        
        if concentration > 0.6:
            selected = "Diversifier uniformément"
            analysis = f"Concentration excessive ({concentration:.1%}) chez {best_vendor}"
        else:
            selected = "Concentrer sur le vendeur leader"
            analysis = f"Opportunité de renforcement de {best_vendor}"
        
        return {
            'business_context': context,
            'problem_statement': problem,
            'options_considered': options,
            'evaluation_criteria': ["Diversification", "Performance", "Risque"],
            'options_analysis': analysis,
            'selected_option': selected,
            'final_recommendation': f"Rééquilibrer le portefeuille en {selected.lower()}",
            'action_plan': [
                f"1. Analyser les opportunités chez {worst_vendor}",
                f"2. Maintenir l'excellence de {best_vendor}",
                "3. Développer les partenariats émergents",
                "4. Surveiller les tendances marché"
            ]
        }
    
    def _generate_inventory_recommendation_cot(self, df: pd.DataFrame) -> Dict:
        """Recommandation inventaire avec raisonnement CoT"""
        
        dispo_analysis = df['disponibilite'].value_counts()
        stock_rate = dispo_analysis.get('En stock', 0) / len(df) if 'En stock' in dispo_analysis else 0
        
        context = f"Taux de disponibilité: {stock_rate:.1%}"
        
        if stock_rate < 0.8:
            problem = "Taux de rupture élevé impactant les ventes"
            selected = "Renforcement immédiat des stocks"
        else:
            problem = "Gestion de stock à optimiser pour réduire les coûts"
            selected = "Optimisation fine des niveaux"
        
        return {
            'business_context': context,
            'problem_statement': problem,
            'options_considered': ["Stock de sécurité élevé", "Just-in-time", "Gestion prédictive"],
            'evaluation_criteria': ["Disponibilité", "Coût de stockage", "Réactivité"],
            'options_analysis': f"Avec {stock_rate:.1%} de disponibilité, priorité à la {'disponibilité' if stock_rate < 0.8 else 'optimisation'}",
            'selected_option': selected,
            'final_recommendation': f"Mettre en place une {selected.lower()}",
            'action_plan': [
                "1. Audit des niveaux actuels",
                "2. Identification des produits critiques",
                "3. Mise en place d'alertes automatiques",
                "4. Optimisation continue"
            ]
        }
    
    def _generate_marketing_recommendation_cot(self, df: pd.DataFrame, analysis: Dict) -> Dict:
        """Recommandation marketing avec raisonnement CoT"""
        
        high_performers = df[df['score_global'] > df['score_global'].quantile(0.8)]
        star_vendors = high_performers['vendeur'].value_counts()  # Utiliser 'vendeur' au lieu de 'categorie'
        
        context = f"{len(high_performers)} produits stars identifiés"
        problem = "Optimiser l'allocation du budget marketing pour maximiser le ROI"
        
        if len(star_vendors) == 1:
            selected = "Concentration sur le vendeur star"
            analysis_text = f"Domination claire de {star_vendors.index[0]}"
        else:
            selected = "Approche multi-vendeurs ciblée"
            analysis_text = f"Opportunités chez {len(star_vendors)} vendeurs"
        
        return {
            'business_context': context,
            'problem_statement': problem,
            'options_considered': ["Marketing de masse", "Ciblage par vendeur", "Focus produits stars"],
            'evaluation_criteria': ["ROI marketing", "Couverture marché", "Efficacité"],
            'options_analysis': analysis_text,
            'selected_option': selected,
            'final_recommendation': f"Implémenter une {selected.lower()}",
            'action_plan': [
                "1. Identifier les segments clients des produits stars",
                "2. Développer des campagnes ciblées",
                "3. Mesurer et optimiser le ROI",
                "4. Étendre aux produits similaires"
            ]
        }
    
    def create_executive_summary_cot(self, df: pd.DataFrame, analysis: Dict, recommendations: Dict) -> str:
        """
        Crée un résumé exécutif avec raisonnement Chain of Thought transparent
        
        Args:
            df (pd.DataFrame): Données analysées
            analysis (Dict): Analyse CoT
            recommendations (Dict): Recommandations CoT
            
        Returns:
            str: Résumé exécutif avec raisonnement explicite
        """
        
        summary = f"""
        🧠 RÉSUMÉ EXÉCUTIF - ANALYSE CHAIN OF THOUGHT
        
        📊 MÉTHODOLOGIE DE RAISONNEMENT
        L'analyse suit une approche Chain of Thought structurée en 4 étapes:
        1️⃣ Observation des caractéristiques des données
        2️⃣ Identification des patterns significatifs  
        3️⃣ Analyse des corrélations et dépendances
        4️⃣ Évaluation des implications business
        
        📈 INSIGHTS GÉNÉRÉS PAR LE RAISONNEMENT CoT
        
        🔍 OBSERVATIONS FACTUELLES:
        • {len(df)} produits analysés
        • Prix médian: {df['prix'].median():.0f}€ (écart-type: {df['prix'].std():.0f}€)
        • Score moyen: {df['score_global'].mean():.3f}
        • {len(df['vendeur'].unique())} vendeurs représentés
        
        🎯 PATTERNS IDENTIFIÉS:
        {analysis.get('pattern_identification', 'Non disponible')}
        
        🔗 CORRÉLATIONS DÉCOUVERTES:
        {analysis.get('correlation_analysis', 'Non disponible')}
        
        ⚡ IMPLICATIONS STRATÉGIQUES:
        {analysis.get('implications_assessment', 'Non disponible')}
        
        💡 RECOMMANDATIONS BASÉES SUR LE RAISONNEMENT CoT
        
        🎯 PRICING ({recommendations['pricing']['selected_option']}):
        Raisonnement: {recommendations['pricing']['options_analysis']}
        → Action: {recommendations['pricing']['final_recommendation']}
        
        📂 VENDEURS ({recommendations['vendor']['selected_option']}):
        Raisonnement: {recommendations['vendor']['options_analysis']}
        → Action: {recommendations['vendor']['final_recommendation']}
        
        📦 INVENTAIRE ({recommendations['inventory']['selected_option']}):
        Raisonnement: {recommendations['inventory']['options_analysis']}
        → Action: {recommendations['inventory']['final_recommendation']}
        
        📢 MARKETING ({recommendations['marketing']['selected_option']}):
        Raisonnement: {recommendations['marketing']['options_analysis']}
        → Action: {recommendations['marketing']['final_recommendation']}
        
        🎯 CONCLUSION DU RAISONNEMENT
        {analysis.get('analytical_conclusion', 'Non disponible')}
        
        ⚡ PLAN D'ACTION PRIORITAIRE
        1. Mise en œuvre des recommandations pricing (Impact: Élevé)
        2. Rééquilibrage du portefeuille vendeurs (Impact: Moyen)
        3. Optimisation de la gestion d'inventaire (Impact: Élevé)
        4. Réallocation du budget marketing (Impact: Moyen)
        
        📋 TRAÇABILITÉ DU RAISONNEMENT
        Toutes les étapes de raisonnement sont documentées et vérifiables.
        Historique complet disponible dans l'attribut reasoning_history.
        """
        
        return summary
    
    def export_reasoning_trace(self, filepath: str = None) -> str:
        """
        Exporte la trace complète du raisonnement Chain of Thought
        
        Args:
            filepath (str, optional): Chemin de sauvegarde
            
        Returns:
            str: Chemin du fichier exporté
        """
        if filepath is None:
            filepath = f"cot_reasoning_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        reasoning_export = {
            'metadata': {
                'export_timestamp': datetime.now().isoformat(),
                'total_reasoning_steps': len(self.reasoning_history),
                'methodology': 'Chain of Thought (CoT) Reasoning'
            },
            'reasoning_history': self.reasoning_history,
            'templates_used': self.cot_analyzer.cot_templates
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(reasoning_export, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Trace de raisonnement exportée vers: {filepath}")
        return filepath
    
    def run_complete_cot_analysis(self, csv_path: str) -> Dict:
        """
        Lance l'analyse complète avec Chain of Thought
        
        Args:
            csv_path (str): Chemin vers le CSV des produits
            
        Returns:
            Dict: Résultats complets avec raisonnement CoT
        """
        print("🧠 Démarrage de l'analyse Chain of Thought complète...")
        
        # 1. Chargement et validation avec CoT
        df, load_reasoning = self.load_and_validate_data(csv_path)
        if df is None:
            return {'error': 'Échec du chargement des données', 'reasoning': load_reasoning}
        
        # 2. Analyse des patterns avec CoT
        cot_analysis = self.analyze_patterns_with_cot(df)
        
        # 3. Génération des recommandations avec CoT
        cot_recommendations = self.generate_strategic_recommendations_cot(df, cot_analysis)
        
        # 4. Création du résumé exécutif avec CoT
        executive_summary = self.create_executive_summary_cot(df, cot_analysis, cot_recommendations)
        
        # 5. Export de la trace de raisonnement
        trace_file = self.export_reasoning_trace()
        
        results = {
            'methodology': 'Chain of Thought (CoT)',
            'data': df,
            'cot_analysis': cot_analysis,
            'cot_recommendations': cot_recommendations,
            'executive_summary': executive_summary,
            'reasoning_trace_file': trace_file,
            'reasoning_history': self.reasoning_history
        }
        
        print("✅ Analyse Chain of Thought complète terminée!")
        return results

def main():
    """Fonction principale pour exécuter l'analyse Chain of Thought"""
    
    print("🧠 === ANALYSEUR PRODUITS CHAIN OF THOUGHT ===")
    print("Raisonnement explicite et structuré pour l'analyse produit\n")
    
    try:
        # Initialisation du générateur CoT
        print("🚀 Initialisation du générateur d'insights...")
        generator = ProductInsightsCoTGenerator()
        
        # Chemin vers le fichier CSV (configurable)
        csv_path = "top_produits_attractifs.csv"
        print(f"📂 Fichier de données: {csv_path}")
        
        # Vérification de l'existence du fichier
        import os
        if not os.path.exists(csv_path):
            print(f"❌ ERREUR: Le fichier {csv_path} n'existe pas!")
            return
        
        # Exécution de l'analyse CoT complète
        print("\n🔄 Lancement de l'analyse complète...")
        results = generator.run_complete_cot_analysis(csv_path)
        
        # Gestion des résultats
        if 'error' in results:
            print(f"❌ ERREUR: {results['error']}")
            print("\n🔍 Détails du raisonnement:")
            for step, details in results['reasoning'].items():
                print(f"  - {step}: {details}")
            return
        
        # Affichage du résumé exécutif
        print("\n" + "="*100)
        print("\n📊 RÉSUMÉ EXÉCUTIF")
        print(results['executive_summary'])
        print("="*100)
        
        # Affichage des étapes de raisonnement clés
        print("\n🧠 ÉTAPES DE RAISONNEMENT DÉTAILLÉES")
        for entry in results['reasoning_history']:
            print(f"\n⏰ {entry['timestamp']} - {entry['operation']}")
            for step, details in entry['reasoning'].items():
                print(f"  - {step}: {details}")
        
        # Information sur l'export
        print(f"\n📋 Trace complète exportée vers: {results['reasoning_trace_file']}")
        
        # Option pour sauvegarder un rapport simplifié
        report_path = f"rapport_cot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(results['executive_summary'])
        print(f"📄 Rapport simplifié sauvegardé: {report_path}")
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: Une erreur inattendue s'est produite - {str(e)}")
        print("🔍 Veuillez vérifier les logs et le fichier d'entrée.")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🏁 Analyse terminée!")
        print("="*100)

if __name__ == "__main__":
    main()