# Analyse PySpark - Dataset Kaggle

![PySpark](https://img.shields.io/badge/PySpark-3.5+-orange.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)

## 📖 Description

Ce projet réalise une analyse complète d'un dataset en utilisant **Apache PySpark**. Il démontre l'utilisation de PySpark pour l'exploration de données, les statistiques descriptives, les analyses par groupes, et les corrélations.

**Nouveau** : Une interface interactive **Streamlit** permet de visualiser et d'explorer les données de manière conviviale.

## 🎯 Objectifs

- Charger et explorer un dataset type Kaggle
- Réaliser des statistiques descriptives avec PySpark
- Analyser les données par groupes (départements, genre)
- Calculer des corrélations entre variables
- Générer des insights business
- **Visualiser les données avec une interface Streamlit interactive**

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
- Java 17 (requis pour PySpark)
- [Mise](https://mise.jdx.dev/) (gestionnaire de tâches)
- Apache Spark (optionnel, pour le mode cluster)

### Installation des dépendances

```bash
# Avec mise (recommandé)
mise run install

# Ou avec pip
pip install -r requirements.txt
```

### Installation de Spark (optionnel)

Pour utiliser le mode cluster avec Master/Workers :

```bash
# macOS avec Homebrew
brew install openjdk@17
brew install apache-spark

# Voir les instructions complètes
mise run install-spark
```

## 💻 Utilisation

### 🌐 Interface Streamlit (recommandé)

Lancez l'application Streamlit pour une exploration interactive des données :

```bash
# Avec mise
mise run streamlit

# Ou directement
streamlit run streamlit_app.py
```

L'interface Streamlit offre :
- **📈 Vue d'ensemble** : Métriques clés et graphiques de synthèse
- **🏢 Analyse par Département** : Statistiques détaillées par département
- **📊 Distributions** : Histogrammes et scatter plots interactifs
- **🔗 Corrélations** : Matrice de corrélation et heatmap
- **📋 Données brutes** : Exploration et export des données

**Filtres disponibles** :
- Département
- Genre
- Tranche d'âge
- Tranche de salaire

### Mode simple (local)

```bash
# Avec mise
mise run analyse

# Ou directement
python analyse.py
```

### Mode interactif

```bash
# Shell PySpark
mise run pyspark-shell

# Jupyter Notebook
mise run notebook
```

## 🎬 Démo : Cluster Spark avec Master et Workers

Cette section décrit la procédure complète pour démarrer un cluster Spark local avec un Master et plusieurs Workers, idéal pour une démonstration du traitement distribué.

### Étape 1 : Vérifier les prérequis

```bash
# Vérifier que Java est installé
java -version

# Vérifier que Spark est installé
spark-shell --version

# Afficher les infos du projet
mise run info
```

### Étape 2 : Démarrer le cluster Spark

**Option A : Démarrage automatique (recommandé)**

```bash
# Démarrer le cluster complet (1 Master + 2 Workers)
mise run spark-cluster-start
```

**Option B : Démarrage manuel étape par étape**

```bash
# Terminal 1 : Démarrer le Master
mise run spark-master-start

# Terminal 2 : Démarrer le Worker 1
mise run spark-worker-start

# Terminal 3 : Démarrer un second Worker (optionnel)
mise run spark-worker-start
```

### Étape 3 : Vérifier le statut du cluster

```bash
# Afficher le statut
mise run spark-cluster-status
```

**Interfaces Web disponibles :**

| Composant | URL |
|-----------|-----|
| 🖥️ Master UI | http://localhost:8080 |
| 👷 Worker 1 UI | http://localhost:8081 |
| 👷 Worker 2 UI | http://localhost:8082 |

### Étape 4 : Exécuter l'analyse sur le cluster

```bash
# Soumettre le job au cluster
mise run analyse-cluster
```

Ou utiliser le shell PySpark connecté au cluster :

```bash
mise run pyspark-shell-cluster
```

### Étape 5 : Observer l'exécution

1. Ouvrez http://localhost:8080 dans votre navigateur
2. Observez les **Workers** enregistrés
3. Cliquez sur **Running Applications** pour voir le job en cours
4. Explorez les **Executors** et les **Stages**

### Étape 6 : Arrêter le cluster

```bash
# Arrêter tout le cluster
mise run spark-cluster-stop
```

### 📋 Résumé des commandes Mise pour le cluster

| Commande | Description |
|----------|-------------|
| `mise run spark-cluster-start` | 🌟 Démarrer Master + 2 Workers |
| `mise run spark-cluster-stop` | 🛑 Arrêter tout le cluster |
| `mise run spark-cluster-status` | 📊 Voir le statut du cluster |
| `mise run spark-master-start` | 🚀 Démarrer uniquement le Master |
| `mise run spark-master-stop` | 🛑 Arrêter le Master |
| `mise run spark-worker-start` | 👷 Démarrer un Worker |
| `mise run spark-worker-stop` | 🛑 Arrêter les Workers |
| `mise run analyse-cluster` | 📊 Exécuter l'analyse sur le cluster |
| `mise run pyspark-shell-cluster` | 🐍 Shell connecté au cluster |

### 💡 Tips pour la démo

1. **Ouvrez le Master UI** avant de lancer le job pour voir les Workers s'enregistrer
2. **Utilisez plusieurs terminaux** pour montrer le démarrage séquentiel
3. **Montrez les logs** dans la console du Worker pendant l'exécution
4. **Comparez les performances** entre mode local et mode cluster

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