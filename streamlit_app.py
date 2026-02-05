"""
Application Streamlit pour l'analyse PySpark des données employés
================================================================

Interface interactive pour visualiser et explorer les données avec PySpark.
"""

# IMPORTANT: Configuration Java AVANT tout import PySpark
# Nécessaire pour Python 3.12+ (distutils) et Java 17+ (Security Manager)
import os

# Configuration des options Java pour compatibilité avec Java 17+
# Ces options doivent être définies AVANT que Spark ne démarre la JVM
os.environ["_JAVA_OPTIONS"] = (
    "-Djava.security.manager=allow "
    "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
    "--add-opens=java.base/java.lang=ALL-UNNAMED "
    "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
    "--add-opens=java.base/java.util=ALL-UNNAMED "
    "--add-opens=java.base/java.nio=ALL-UNNAMED "
    "--add-opens=java.base/sun.security.action=ALL-UNNAMED "
    "--add-opens=java.base/javax.security.auth=ALL-UNNAMED"
)

# Import setuptools.dist pour fournir distutils (supprimé en Python 3.12)
import setuptools.dist  # noqa: F401

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, min, max, stddev, corr

# Configuration de la page
st.set_page_config(
    page_title="Analyse PySpark - Employés",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_spark_session():
    """Crée et met en cache une session Spark"""
    spark = SparkSession.builder \
        .appName("Streamlit - Analyse Dataset Employés") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.ui.showConsoleProgress", "false") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


@st.cache_data
def load_data_pandas(_spark, file_path):
    """Charge les données et les convertit en Pandas DataFrame"""
    df_spark = _spark.read.csv(file_path, header=True, inferSchema=True)
    return df_spark.toPandas()


@st.cache_data
def compute_correlations(_spark, file_path):
    """Calcule les corrélations entre variables numériques"""
    df = _spark.read.csv(file_path, header=True, inferSchema=True)
    
    correlations = {
        "Salaire-Expérience": df.stat.corr("salary", "experience_years"),
        "Satisfaction-Performance": df.stat.corr("satisfaction_score", "performance_rating"),
        "Âge-Expérience": df.stat.corr("age", "experience_years"),
        "Salaire-Performance": df.stat.corr("salary", "performance_rating"),
        "Âge-Salaire": df.stat.corr("age", "salary"),
        "Expérience-Performance": df.stat.corr("experience_years", "performance_rating"),
    }
    return correlations


@st.cache_data
def compute_department_stats(_spark, file_path):
    """Calcule les statistiques par département avec PySpark"""
    df = _spark.read.csv(file_path, header=True, inferSchema=True)
    
    dept_stats = df.groupBy("department") \
        .agg(
            count("*").alias("nombre_employes"),
            avg("salary").alias("salaire_moyen"),
            avg("age").alias("age_moyen"),
            avg("experience_years").alias("experience_moyenne"),
            avg("satisfaction_score").alias("satisfaction_moyenne"),
            avg("performance_rating").alias("performance_moyenne"),
            min("salary").alias("salaire_min"),
            max("salary").alias("salaire_max"),
            stddev("salary").alias("salaire_ecart_type")
        ) \
        .orderBy(col("salaire_moyen").desc())
    
    return dept_stats.toPandas()


@st.cache_data
def compute_gender_stats(_spark, file_path):
    """Calcule les statistiques par genre avec PySpark"""
    df = _spark.read.csv(file_path, header=True, inferSchema=True)
    
    gender_stats = df.groupBy("gender") \
        .agg(
            count("*").alias("nombre_employes"),
            avg("salary").alias("salaire_moyen"),
            avg("satisfaction_score").alias("satisfaction_moyenne"),
            avg("performance_rating").alias("performance_moyenne")
        )
    
    return gender_stats.toPandas()


def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Analyse PySpark - Dataset Employés</h1>', unsafe_allow_html=True)
    
    # Initialiser Spark
    spark = get_spark_session()
    
    # Chemin des données
    data_path = os.path.join(os.path.dirname(__file__), "data", "employee_data.csv")
    
    if not os.path.exists(data_path):
        st.error(f"❌ Fichier de données non trouvé: {data_path}")
        return
    
    # Charger les données
    with st.spinner("Chargement des données avec PySpark..."):
        df = load_data_pandas(spark, data_path)
        dept_stats = compute_department_stats(spark, data_path)
        gender_stats = compute_gender_stats(spark, data_path)
        correlations = compute_correlations(spark, data_path)
    
    # Sidebar - Filtres
    st.sidebar.header("🔍 Filtres")
    
    # Filtre par département
    departments = ["Tous"] + sorted(df["department"].unique().tolist())
    selected_dept = st.sidebar.selectbox("Département", departments)
    
    # Filtre par genre
    genders = ["Tous"] + sorted(df["gender"].unique().tolist())
    selected_gender = st.sidebar.selectbox("Genre", genders)
    
    # Filtre par âge
    age_range = st.sidebar.slider(
        "Tranche d'âge",
        min_value=int(df["age"].min()),
        max_value=int(df["age"].max()),
        value=(int(df["age"].min()), int(df["age"].max()))
    )
    
    # Filtre par salaire
    salary_range = st.sidebar.slider(
        "Tranche de salaire ($)",
        min_value=int(df["salary"].min()),
        max_value=int(df["salary"].max()),
        value=(int(df["salary"].min()), int(df["salary"].max()))
    )
    
    # Appliquer les filtres
    df_filtered = df.copy()
    if selected_dept != "Tous":
        df_filtered = df_filtered[df_filtered["department"] == selected_dept]
    if selected_gender != "Tous":
        df_filtered = df_filtered[df_filtered["gender"] == selected_gender]
    df_filtered = df_filtered[
        (df_filtered["age"] >= age_range[0]) & 
        (df_filtered["age"] <= age_range[1]) &
        (df_filtered["salary"] >= salary_range[0]) &
        (df_filtered["salary"] <= salary_range[1])
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"📋 **{len(df_filtered)}** employés sélectionnés sur **{len(df)}**")
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Vue d'ensemble", 
        "🏢 Analyse par Département",
        "📊 Distributions",
        "🔗 Corrélations",
        "📋 Données brutes"
    ])
    
    # ================= TAB 1: Vue d'ensemble =================
    with tab1:
        st.header("Vue d'ensemble")
        
        # Métriques principales
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="👥 Employés",
                value=len(df_filtered),
                delta=f"{len(df_filtered) - len(df)} vs total" if len(df_filtered) != len(df) else None
            )
        
        with col2:
            avg_salary = df_filtered["salary"].mean()
            st.metric(
                label="💰 Salaire moyen",
                value=f"${avg_salary:,.0f}"
            )
        
        with col3:
            avg_age = df_filtered["age"].mean()
            st.metric(
                label="📅 Âge moyen",
                value=f"{avg_age:.1f} ans"
            )
        
        with col4:
            avg_satisfaction = df_filtered["satisfaction_score"].mean()
            st.metric(
                label="😊 Satisfaction",
                value=f"{avg_satisfaction:.2f}/10"
            )
        
        with col5:
            avg_performance = df_filtered["performance_rating"].mean()
            st.metric(
                label="⭐ Performance",
                value=f"{avg_performance:.2f}/5"
            )
        
        st.markdown("---")
        
        # Graphiques de synthèse
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribution des employés par département")
            dept_count = df_filtered.groupby("department").size().reset_index(name="count")
            fig_dept = px.pie(
                dept_count, 
                values="count", 
                names="department",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_dept.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_dept, use_container_width=True)
        
        with col2:
            st.subheader("Distribution par genre")
            gender_count = df_filtered.groupby("gender").size().reset_index(name="count")
            fig_gender = px.bar(
                gender_count,
                x="gender",
                y="count",
                color="gender",
                color_discrete_map={"M": "#1f77b4", "F": "#e377c2"},
                text="count"
            )
            fig_gender.update_traces(textposition='outside')
            fig_gender.update_layout(showlegend=False)
            st.plotly_chart(fig_gender, use_container_width=True)
        
        # Top performers
        st.subheader("⭐ Top 10 des employés les plus performants")
        top_performers = df_filtered.nlargest(10, "performance_rating")[
            ["id", "age", "gender", "department", "salary", "experience_years", "satisfaction_score", "performance_rating"]
        ]
        st.dataframe(
            top_performers.style.background_gradient(subset=["performance_rating"], cmap="Greens"),
            use_container_width=True
        )
    
    # ================= TAB 2: Analyse par Département =================
    with tab2:
        st.header("Analyse par Département")
        
        # Statistiques par département (utilise les données calculées avec PySpark)
        st.subheader("📊 Statistiques par département (calculées avec PySpark)")
        st.dataframe(
            dept_stats.style.format({
                "salaire_moyen": "${:,.2f}",
                "salaire_min": "${:,.0f}",
                "salaire_max": "${:,.0f}",
                "salaire_ecart_type": "${:,.2f}",
                "age_moyen": "{:.1f}",
                "experience_moyenne": "{:.1f}",
                "satisfaction_moyenne": "{:.2f}",
                "performance_moyenne": "{:.2f}"
            }).background_gradient(subset=["salaire_moyen"], cmap="Blues"),
            use_container_width=True
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Salaire moyen par département")
            fig_salary = px.bar(
                dept_stats.sort_values("salaire_moyen", ascending=True),
                x="salaire_moyen",
                y="department",
                orientation="h",
                color="salaire_moyen",
                color_continuous_scale="Blues",
                text=dept_stats.sort_values("salaire_moyen", ascending=True)["salaire_moyen"].apply(lambda x: f"${x:,.0f}")
            )
            fig_salary.update_traces(textposition='outside')
            fig_salary.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_salary, use_container_width=True)
        
        with col2:
            st.subheader("Satisfaction moyenne par département")
            fig_satisfaction = px.bar(
                dept_stats.sort_values("satisfaction_moyenne", ascending=True),
                x="satisfaction_moyenne",
                y="department",
                orientation="h",
                color="satisfaction_moyenne",
                color_continuous_scale="Greens",
                text=dept_stats.sort_values("satisfaction_moyenne", ascending=True)["satisfaction_moyenne"].apply(lambda x: f"{x:.2f}")
            )
            fig_satisfaction.update_traces(textposition='outside')
            fig_satisfaction.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_satisfaction, use_container_width=True)
        
        # Box plot des salaires par département
        st.subheader("Distribution des salaires par département")
        fig_box = px.box(
            df_filtered,
            x="department",
            y="salary",
            color="department",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    
    # ================= TAB 3: Distributions =================
    with tab3:
        st.header("Distributions des variables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribution des âges")
            fig_age = px.histogram(
                df_filtered,
                x="age",
                nbins=20,
                color_discrete_sequence=["#1f77b4"],
                marginal="box"
            )
            fig_age.update_layout(showlegend=False)
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            st.subheader("Distribution des salaires")
            fig_sal = px.histogram(
                df_filtered,
                x="salary",
                nbins=25,
                color_discrete_sequence=["#2ca02c"],
                marginal="box"
            )
            fig_sal.update_layout(showlegend=False)
            st.plotly_chart(fig_sal, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Distribution de l'expérience")
            fig_exp = px.histogram(
                df_filtered,
                x="experience_years",
                nbins=20,
                color_discrete_sequence=["#ff7f0e"],
                marginal="box"
            )
            fig_exp.update_layout(showlegend=False)
            st.plotly_chart(fig_exp, use_container_width=True)
        
        with col4:
            st.subheader("Distribution des scores de satisfaction")
            fig_sat = px.histogram(
                df_filtered,
                x="satisfaction_score",
                nbins=20,
                color_discrete_sequence=["#9467bd"],
                marginal="box"
            )
            fig_sat.update_layout(showlegend=False)
            st.plotly_chart(fig_sat, use_container_width=True)
        
        # Scatter plot interactif
        st.markdown("---")
        st.subheader("🔍 Explorer les relations entre variables")
        
        numeric_cols = ["age", "salary", "experience_years", "satisfaction_score", "performance_rating"]
        
        col_x, col_y, col_color = st.columns(3)
        with col_x:
            x_axis = st.selectbox("Axe X", numeric_cols, index=2)
        with col_y:
            y_axis = st.selectbox("Axe Y", numeric_cols, index=1)
        with col_color:
            color_by = st.selectbox("Couleur par", ["department", "gender", "performance_rating"])
        
        fig_scatter = px.scatter(
            df_filtered,
            x=x_axis,
            y=y_axis,
            color=color_by,
            hover_data=["id", "department", "salary", "performance_rating"],
            size="salary",
            size_max=15,
            color_discrete_sequence=px.colors.qualitative.Set1 if color_by != "performance_rating" else None,
            color_continuous_scale="Viridis" if color_by == "performance_rating" else None
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # ================= TAB 4: Corrélations =================
    with tab4:
        st.header("Analyse des corrélations (calculées avec PySpark)")
        
        # Afficher les corrélations calculées par PySpark
        st.subheader("📐 Corrélations entre variables numériques")
        
        col1, col2, col3 = st.columns(3)
        
        corr_items = list(correlations.items())
        for i, (name, value) in enumerate(corr_items):
            col = [col1, col2, col3][i % 3]
            with col:
                color = "normal" if abs(value) < 0.3 else ("off" if value < 0 else "inverse")
                st.metric(
                    label=name,
                    value=f"{value:.3f}",
                    delta="Forte" if abs(value) > 0.5 else ("Modérée" if abs(value) > 0.3 else "Faible"),
                    delta_color=color
                )
        
        st.markdown("---")
        
        # Matrice de corrélation visuelle
        st.subheader("🔥 Matrice de corrélation (Heatmap)")
        
        numeric_df = df_filtered[["age", "salary", "experience_years", "satisfaction_score", "performance_rating"]]
        corr_matrix = numeric_df.corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            labels=dict(color="Corrélation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto"
        )
        fig_corr.update_layout(height=500)
        
        # Ajouter les valeurs dans les cellules
        for i, row in enumerate(corr_matrix.values):
            for j, val in enumerate(row):
                fig_corr.add_annotation(
                    x=j, y=i,
                    text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(color="white" if abs(val) > 0.5 else "black", size=12)
                )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Interprétation
        st.subheader("💡 Interprétation des corrélations")
        st.markdown("""
        - **Corrélation positive forte (> 0.7)** : Les variables augmentent ensemble
        - **Corrélation positive modérée (0.3 - 0.7)** : Tendance positive
        - **Corrélation faible (-0.3 - 0.3)** : Peu de relation linéaire
        - **Corrélation négative modérée (-0.7 - -0.3)** : Tendance inverse
        - **Corrélation négative forte (< -0.7)** : Les variables évoluent en sens inverse
        """)
    
    # ================= TAB 5: Données brutes =================
    with tab5:
        st.header("Données brutes")
        
        # Options d'affichage
        col1, col2 = st.columns(2)
        with col1:
            show_all = st.checkbox("Afficher toutes les colonnes", value=True)
        with col2:
            n_rows = st.slider("Nombre de lignes à afficher", 10, 100, 25)
        
        if show_all:
            display_cols = df_filtered.columns.tolist()
        else:
            display_cols = st.multiselect(
                "Sélectionner les colonnes",
                df_filtered.columns.tolist(),
                default=["id", "age", "department", "salary", "performance_rating"]
            )
        
        # Tri
        sort_by = st.selectbox("Trier par", display_cols)
        sort_order = st.radio("Ordre", ["Décroissant", "Croissant"], horizontal=True)
        
        df_display = df_filtered[display_cols].sort_values(
            sort_by, 
            ascending=(sort_order == "Croissant")
        ).head(n_rows)
        
        st.dataframe(df_display, use_container_width=True)
        
        # Téléchargement
        st.download_button(
            label="📥 Télécharger les données filtrées (CSV)",
            data=df_filtered.to_csv(index=False).encode('utf-8'),
            file_name="employee_data_filtered.csv",
            mime="text/csv"
        )
        
        # Statistiques descriptives
        st.subheader("📊 Statistiques descriptives")
        st.dataframe(df_filtered.describe().T.style.format("{:.2f}"), use_container_width=True)


if __name__ == "__main__":
    main()
