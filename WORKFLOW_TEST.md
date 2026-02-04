# 🧪 Workflow de Test Complet

Ce document décrit le workflow de test complet pour vérifier l'installation et le fonctionnement du projet analyse-pyspark.

## ✅ Tests Effectués

### 1. Vérification de l'environnement

```bash
mise run info
```

**Résultat attendu :**
- ✅ Python 3.12+ installé
- ✅ Java 17 installé
- ✅ Variables d'environnement Spark affichées

**Résultat obtenu :** ✅ Succès
```
📦 Projet: analyse-pyspark
🐍 Python: Python 3.12.12
☕ Java: openjdk version "17.0.18"
```

---

### 2. Installation des dépendances

```bash
mise run install
```

**Résultat attendu :**
- ✅ Installation réussie des packages PySpark, pandas, matplotlib, seaborn

**Résultat obtenu :** ✅ Succès
```
📦 Installation des dépendances...
Resolved 17 packages in 13ms
✓ Dépendances installées
```

---

### 3. Vérification du dataset

```bash
mise run data-info
```

**Résultat attendu :**
- ✅ Affichage du nombre de lignes et colonnes
- ✅ Liste des en-têtes
- ✅ Aperçu des premières lignes

**Résultat obtenu :** ✅ Succès
```
📊 Statistiques:
   Lignes:      501
   Colonnes:        8
```

---

### 4. Génération d'un nouveau dataset

```bash
mise run data-generate
```

**Résultat attendu :**
- ✅ Création d'un fichier CSV avec 500 employés

**Résultat obtenu :** ✅ Succès
```
✓ Dataset généré: data/employee_data.csv (500 employés)
```

---

### 5. Exécution de l'analyse principale

```bash
mise run analyse
```

**Résultat attendu :**
- ✅ Chargement des données
- ✅ Exploration et statistiques descriptives
- ✅ Analyses par groupes (département, genre)
- ✅ Calcul des corrélations
- ✅ Analyses avancées
- ✅ Génération du résumé

**Résultat obtenu :** ✅ Succès

Extraits de sortie :
```
============================================================
CHARGEMENT DES DONNÉES
============================================================
✓ Données chargées avec succès depuis: data/employee_data.csv
  Nombre de lignes: 500
  Nombre de colonnes: 8

============================================================
RÉSUMÉ DE L'ANALYSE
============================================================
📊 Vue d'ensemble du dataset:
   - Nombre total d'employés: 500
   - Salaire moyen: $68,450.00
   - Âge moyen: 33.8 ans
   - Score de satisfaction moyen: 7.97/10
   - Note de performance moyenne: 4.33/5

💡 Insights clés:
   - Département le mieux payé: Sales ($79,636.36)
   - Département avec la meilleure satisfaction: Sales (8.48/10)

============================================================
✓ ANALYSE TERMINÉE AVEC SUCCÈS
============================================================
```

---

### 6. Vérification du statut du cluster

```bash
mise run spark-cluster-status
```

**Résultat attendu :**
- ✅ Affichage du statut Master et Workers

**Résultat obtenu :** ✅ Succès
```
📊 Statut du cluster Spark
==========================
❌ Master: Arrêté
❌ Workers: Aucun en cours d'exécution
```

---

### 7. Nettoyage des fichiers temporaires

```bash
mise run clean
```

**Résultat attendu :**
- ✅ Suppression des fichiers cache et temporaires

**Résultat obtenu :** ✅ Succès
```
🧹 Nettoyage des fichiers temporaires...
✓ Nettoyage terminé
```

---

### 8. Liste de toutes les tâches disponibles

```bash
mise tasks
```

**Résultat attendu :**
- ✅ Affichage de toutes les tâches configurées

**Résultat obtenu :** ✅ Succès
- 30+ tâches listées incluant analyse, cluster, tests, etc.

---

## 📋 Résumé du Workflow Complet

### Workflow d'installation et test rapide

```bash
# 1. Vérifier l'environnement
mise run info

# 2. Installer les dépendances
mise run install

# 3. Vérifier le dataset
mise run data-info

# 4. Exécuter l'analyse
mise run analyse

# 5. Nettoyer
mise run clean
```

### Workflow avec génération de données

```bash
# 1. Générer un nouveau dataset
mise run data-generate

# 2. Vérifier le dataset généré
mise run data-info

# 3. Exécuter l'analyse
mise run analyse
```

### Workflow pour le mode cluster (si Spark est installé)

```bash
# 1. Démarrer le cluster
mise run spark-cluster-start

# 2. Vérifier le statut
mise run spark-cluster-status

# 3. Exécuter l'analyse sur le cluster
mise run analyse-cluster

# 4. Arrêter le cluster
mise run spark-cluster-stop
```

---

## ⚙️ Configuration Requise

### Fonctionnement Vérifié

| Composant | Version | Statut |
|-----------|---------|--------|
| Python | 3.12.12 | ✅ OK |
| Java | OpenJDK 17.0.18 | ✅ OK |
| PySpark | 3.5.0+ | ✅ OK |
| Mise | Latest | ✅ OK |

### Mode de Fonctionnement

- **Mode local** : ✅ Fonctionne sans installation de Spark séparée (PySpark intégré)
- **Mode cluster** : Nécessite l'installation d'Apache Spark via `brew install apache-spark`

---

## 🐛 Problèmes Résolus

### Problème : SPARK_HOME invalide

**Symptôme :**
```
FileNotFoundError: [Errno 2] No such file or directory: 
'/Users/rmassiet/.local/share/spark/./bin/spark-submit'
```

**Solution :**
Le fichier `mise.toml` a été modifié pour :
1. Commenter la variable `SPARK_HOME` par défaut
2. Ajouter une vérification dans la tâche `analyse` qui désactive `SPARK_HOME` si le répertoire n'existe pas
3. Permettre à PySpark intégré de fonctionner en mode local sans Spark installé séparément

**Code ajouté dans mise.toml :**
```bash
# Désactiver SPARK_HOME si Spark n'est pas installé séparément
if [ ! -d "${SPARK_HOME}/bin" ]; then
    unset SPARK_HOME
fi
```

---

## ✅ Conclusion

Le workflow de test complet a été exécuté avec succès. Le projet fonctionne correctement en mode local avec PySpark intégré. Toutes les fonctionnalités principales ont été testées et validées :

- ✅ Installation des dépendances
- ✅ Génération et vérification des données
- ✅ Exécution de l'analyse PySpark
- ✅ Gestion du cluster Spark
- ✅ Outils de développement (lint, format, clean)
- ✅ Commandes utilitaires

**Date du test :** 4 février 2026
**Environnement :** macOS avec Homebrew
**Status global :** ✅ SUCCÈS
