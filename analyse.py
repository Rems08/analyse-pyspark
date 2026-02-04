"""
Analyse PySpark d'un dataset Kaggle
====================================

Ce script réalise une analyse complète d'un dataset en utilisant PySpark.
Il inclut:
- Chargement des données
- Exploration et statistiques descriptives
- Analyses par groupes
- Corrélations
- Visualisations
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, min, max, stddev, corr
from pyspark.sql.types import DoubleType, IntegerType
import sys


def create_spark_session():
    """Crée et configure une session Spark"""
    spark = SparkSession.builder \
        .appName("Analyse Dataset Kaggle") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def load_data(spark, file_path):
    """Charge les données depuis un fichier CSV"""
    print(f"\n{'='*60}")
    print("CHARGEMENT DES DONNÉES")
    print(f"{'='*60}")
    
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    print(f"✓ Données chargées avec succès depuis: {file_path}")
    print(f"  Nombre de lignes: {df.count()}")
    print(f"  Nombre de colonnes: {len(df.columns)}")
    
    return df


def explore_data(df):
    """Explore les données et affiche les informations de base"""
    print(f"\n{'='*60}")
    print("EXPLORATION DES DONNÉES")
    print(f"{'='*60}")
    
    print("\n📊 Structure du dataset:")
    df.printSchema()
    
    print("\n📋 Aperçu des données (5 premières lignes):")
    df.show(5, truncate=False)
    
    print("\n🔢 Statistiques descriptives:")
    df.describe().show()


def analyze_by_groups(df):
    """Analyse les données par groupes"""
    print(f"\n{'='*60}")
    print("ANALYSE PAR GROUPES")
    print(f"{'='*60}")
    
    # Analyse par département
    print("\n📈 Statistiques par département:")
    dept_stats = df.groupBy("department") \
        .agg(
            count("*").alias("nombre_employes"),
            avg("salary").alias("salaire_moyen"),
            avg("age").alias("age_moyen"),
            avg("experience_years").alias("experience_moyenne"),
            avg("satisfaction_score").alias("satisfaction_moyenne"),
            avg("performance_rating").alias("performance_moyenne")
        ) \
        .orderBy(col("salaire_moyen").desc())
    
    dept_stats.show(truncate=False)
    
    # Analyse par genre
    print("\n👥 Statistiques par genre:")
    gender_stats = df.groupBy("gender") \
        .agg(
            count("*").alias("nombre_employes"),
            avg("salary").alias("salaire_moyen"),
            avg("satisfaction_score").alias("satisfaction_moyenne"),
            avg("performance_rating").alias("performance_moyenne")
        )
    
    gender_stats.show(truncate=False)
    
    # Distribution par département
    print("\n📊 Distribution des employés par département:")
    dept_count = df.groupBy("department") \
        .agg(count("*").alias("nombre_employes")) \
        .orderBy(col("nombre_employes").desc())
    
    dept_count.show(truncate=False)


def calculate_correlations(df):
    """Calcule les corrélations entre variables numériques"""
    print(f"\n{'='*60}")
    print("ANALYSE DES CORRÉLATIONS")
    print(f"{'='*60}")
    
    numeric_cols = ["age", "salary", "experience_years", "satisfaction_score", "performance_rating"]
    
    print("\n📐 Corrélations entre variables numériques:")
    print("-" * 60)
    
    # Corrélation entre salaire et expérience
    corr_salary_exp = df.stat.corr("salary", "experience_years")
    print(f"Corrélation Salaire-Expérience: {corr_salary_exp:.3f}")
    
    # Corrélation entre satisfaction et performance
    corr_sat_perf = df.stat.corr("satisfaction_score", "performance_rating")
    print(f"Corrélation Satisfaction-Performance: {corr_sat_perf:.3f}")
    
    # Corrélation entre âge et expérience
    corr_age_exp = df.stat.corr("age", "experience_years")
    print(f"Corrélation Âge-Expérience: {corr_age_exp:.3f}")
    
    # Corrélation entre salaire et performance
    corr_salary_perf = df.stat.corr("salary", "performance_rating")
    print(f"Corrélation Salaire-Performance: {corr_salary_perf:.3f}")


def advanced_analysis(df):
    """Réalise des analyses avancées"""
    print(f"\n{'='*60}")
    print("ANALYSES AVANCÉES")
    print(f"{'='*60}")
    
    # Employés à haute performance
    print("\n⭐ Employés à haute performance (performance >= 4.5):")
    high_performers = df.filter(col("performance_rating") >= 4.5)
    print(f"Nombre: {high_performers.count()}")
    high_performers.select("id", "age", "department", "salary", "performance_rating") \
        .orderBy(col("performance_rating").desc()) \
        .show(5, truncate=False)
    
    # Analyse des salaires
    print("\n💰 Analyse des salaires:")
    salary_ranges = df.groupBy("department") \
        .agg(
            min("salary").alias("salaire_min"),
            max("salary").alias("salaire_max"),
            avg("salary").alias("salaire_moyen")
        ) \
        .orderBy(col("salaire_moyen").desc())
    
    salary_ranges.show(truncate=False)
    
    # Taux de satisfaction par département
    print("\n😊 Satisfaction moyenne par département:")
    satisfaction_by_dept = df.groupBy("department") \
        .agg(
            avg("satisfaction_score").alias("satisfaction_moyenne"),
            count("*").alias("nombre_employes")
        ) \
        .orderBy(col("satisfaction_moyenne").desc())
    
    satisfaction_by_dept.show(truncate=False)


def generate_summary(df):
    """Génère un résumé de l'analyse"""
    print(f"\n{'='*60}")
    print("RÉSUMÉ DE L'ANALYSE")
    print(f"{'='*60}")
    
    total_employees = df.count()
    avg_salary = df.agg(avg("salary")).collect()[0][0]
    avg_age = df.agg(avg("age")).collect()[0][0]
    avg_satisfaction = df.agg(avg("satisfaction_score")).collect()[0][0]
    avg_performance = df.agg(avg("performance_rating")).collect()[0][0]
    
    print(f"""
📊 Vue d'ensemble du dataset:
   - Nombre total d'employés: {total_employees}
   - Salaire moyen: ${avg_salary:,.2f}
   - Âge moyen: {avg_age:.1f} ans
   - Score de satisfaction moyen: {avg_satisfaction:.2f}/10
   - Note de performance moyenne: {avg_performance:.2f}/5
   
🏢 Départements: {df.select("department").distinct().count()}
👥 Distribution par genre: {df.groupBy("gender").count().count()} catégories
    """)
    
    # Insights clés
    print("💡 Insights clés:")
    
    # Département avec le meilleur salaire
    best_paid_dept = df.groupBy("department") \
        .agg(avg("salary").alias("avg_sal")) \
        .orderBy(col("avg_sal").desc()) \
        .first()
    print(f"   - Département le mieux payé: {best_paid_dept['department']} (${best_paid_dept['avg_sal']:,.2f})")
    
    # Département avec la meilleure satisfaction
    best_satisfaction_dept = df.groupBy("department") \
        .agg(avg("satisfaction_score").alias("avg_sat")) \
        .orderBy(col("avg_sat").desc()) \
        .first()
    print(f"   - Département avec la meilleure satisfaction: {best_satisfaction_dept['department']} ({best_satisfaction_dept['avg_sat']:.2f}/10)")


def main():
    """Fonction principale"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         ANALYSE PYSPARK - DATASET KAGGLE                   ║
    ║                                                            ║
    ║    Étude complète d'un dataset d'employés                  ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Créer la session Spark
    spark = create_spark_session()
    
    try:
        # Chemin du fichier de données
        data_path = "data/employee_data.csv"
        
        # Charger les données
        df = load_data(spark, data_path)
        
        # Explorer les données
        explore_data(df)
        
        # Analyser par groupes
        analyze_by_groups(df)
        
        # Calculer les corrélations
        calculate_correlations(df)
        
        # Analyses avancées
        advanced_analysis(df)
        
        # Générer le résumé
        generate_summary(df)
        
        print(f"\n{'='*60}")
        print("✓ ANALYSE TERMINÉE AVEC SUCCÈS")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'analyse: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Arrêter la session Spark
        spark.stop()


if __name__ == "__main__":
    main()
