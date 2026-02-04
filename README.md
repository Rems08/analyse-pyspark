# Analyse PySpark - Dataset Kaggle

![PySpark](https://img.shields.io/badge/PySpark-3.5+-orange.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

## 📖 Description

Ce projet réalise une analyse complète d'un dataset en utilisant **Apache PySpark**. Il démontre l'utilisation de PySpark pour l'exploration de données, les statistiques descriptives, les analyses par groupes, et les corrélations.

## 🎯 Objectifs

- Charger et explorer un dataset type Kaggle
- Réaliser des statistiques descriptives avec PySpark
- Analyser les données par groupes (départements, genre)
- Calculer des corrélations entre variables
- Générer des insights business

## 📊 Dataset

Le dataset utilisé contient des données d'employés avec les informations suivantes:
- **id**: Identifiant unique de l'employé
- **age**: Âge de l'employé
- **gender**: Genre (M/F)
- **salary**: Salaire annuel
- **department**: Département (IT, HR, Sales, Marketing)
- **experience_years**: Années d'expérience
- **satisfaction_score**: Score de satisfaction (0-10)
- **performance_rating**: Note de performance (0-5)

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Java 8 ou supérieur (requis pour PySpark)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## 💻 Utilisation

Exécutez le script d'analyse principal:

```bash
python analyse.py
```

## 📈 Analyses réalisées

Le script effectue les analyses suivantes:

1. **Exploration des données**
   - Structure du dataset
   - Aperçu des premières lignes
   - Statistiques descriptives

2. **Analyse par groupes**
   - Statistiques par département
   - Statistiques par genre
   - Distribution des employés

3. **Corrélations**
   - Salaire vs Expérience
   - Satisfaction vs Performance
   - Âge vs Expérience
   - Salaire vs Performance

4. **Analyses avancées**
   - Employés à haute performance
   - Analyse des fourchettes de salaires
   - Taux de satisfaction par département

5. **Résumé et insights clés**
   - Vue d'ensemble du dataset
   - Insights business

## 📁 Structure du projet

```
analyse-pyspark/
├── analyse.py              # Script principal d'analyse
├── data/
│   └── employee_data.csv   # Dataset d'exemple
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
└── .gitignore             # Fichiers à ignorer
```

## 🔍 Exemple de sortie

Le script génère une sortie complète avec:
- Statistiques descriptives des variables numériques
- Tableaux d'agrégation par département et genre
- Corrélations entre variables
- Insights clés sur les données

## 📝 Méthodologie

L'analyse utilise les capacités distribuées de PySpark pour:
- Traiter efficacement de grands volumes de données
- Effectuer des agrégations et groupements
- Calculer des statistiques en parallèle
- Optimiser les performances avec le lazy evaluation

## 🛠️ Technologies utilisées

- **PySpark**: Framework de traitement distribué
- **Python**: Langage de programmation
- **Pandas**: Manipulation de données (optionnel)
- **Matplotlib/Seaborn**: Visualisations (optionnel)

## 📚 Ressources

- [Documentation PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Apache Spark](https://spark.apache.org/)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

## 👤 Auteur

Rems08

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.