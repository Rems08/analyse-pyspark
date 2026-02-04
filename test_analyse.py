"""
Tests basiques pour valider l'analyse PySpark
"""

from pyspark.sql import SparkSession
import os
import sys


def test_spark_session():
    """Test de création de session Spark"""
    print("Test 1: Création de session Spark...", end=" ")
    try:
        spark = SparkSession.builder \
            .appName("Test") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        spark.stop()
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_data_loading():
    """Test de chargement des données"""
    print("Test 2: Chargement des données...", end=" ")
    spark = None
    try:
        spark = SparkSession.builder \
            .appName("Test") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        
        data_path = "data/employee_data.csv"
        if not os.path.exists(data_path):
            print(f"✗ FAIL: Fichier {data_path} non trouvé")
            return False
        
        df = spark.read.csv(data_path, header=True, inferSchema=True)
        row_count = df.count()
        col_count = len(df.columns)
        
        if row_count > 0 and col_count == 8:
            print(f"✓ PASS ({row_count} lignes, {col_count} colonnes)")
            return True
        else:
            print(f"✗ FAIL: Dimensions incorrectes ({row_count} lignes, {col_count} colonnes)")
            return False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    finally:
        if spark:
            spark.stop()


def test_data_structure():
    """Test de la structure des données"""
    print("Test 3: Vérification de la structure...", end=" ")
    spark = None
    try:
        spark = SparkSession.builder \
            .appName("Test") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        
        df = spark.read.csv("data/employee_data.csv", header=True, inferSchema=True)
        
        expected_columns = ["id", "age", "gender", "salary", "department", 
                          "experience_years", "satisfaction_score", "performance_rating"]
        
        if set(df.columns) == set(expected_columns):
            print("✓ PASS")
            return True
        else:
            print(f"✗ FAIL: Colonnes attendues: {expected_columns}, trouvées: {df.columns}")
            return False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    finally:
        if spark:
            spark.stop()


def test_aggregations():
    """Test des agrégations"""
    print("Test 4: Test des agrégations...", end=" ")
    spark = None
    try:
        spark = SparkSession.builder \
            .appName("Test") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        
        df = spark.read.csv("data/employee_data.csv", header=True, inferSchema=True)
        
        # Test agrégation par département
        dept_count = df.groupBy("department").count().count()
        
        if dept_count > 0:
            print(f"✓ PASS ({dept_count} départements)")
            return True
        else:
            print("✗ FAIL: Agrégation échouée")
            return False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    finally:
        if spark:
            spark.stop()


def test_correlations():
    """Test du calcul de corrélations"""
    print("Test 5: Test des corrélations...", end=" ")
    spark = None
    try:
        spark = SparkSession.builder \
            .appName("Test") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        
        df = spark.read.csv("data/employee_data.csv", header=True, inferSchema=True)
        
        # Test calcul de corrélation
        corr = df.stat.corr("salary", "experience_years")
        
        if corr is not None and -1 <= corr <= 1:
            print(f"✓ PASS (corrélation: {corr:.3f})")
            return True
        else:
            print("✗ FAIL: Corrélation invalide")
            return False
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    finally:
        if spark:
            spark.stop()


def main():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("TESTS DE VALIDATION - ANALYSE PYSPARK")
    print("="*60 + "\n")
    
    tests = [
        test_spark_session,
        test_data_loading,
        test_data_structure,
        test_aggregations,
        test_correlations
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"RÉSULTATS: {passed}/{total} tests réussis")
    print("="*60 + "\n")
    
    if passed == total:
        print("✓ Tous les tests sont passés avec succès!")
        sys.exit(0)
    else:
        print(f"✗ {total - passed} test(s) échoué(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
