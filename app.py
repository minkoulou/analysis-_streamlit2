import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="BMP TECH - Data Hub",
    page_icon="🚀",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION SIDEBAR ---
with st.sidebar:
    st.title("🛠️ BMP TECH")
    st.markdown("---")
    menu = st.radio("Navigation", ["Saisie de Données", "Dashboard Analytique"])
    st.markdown("---")
    st.info("Interface de gestion de données pour BMP TECH.")

# Initialisation de la base de données en session
if 'data_db' not in st.session_state:
    # On initialise avec quelques colonnes pertinentes pour BMP TECH
    st.session_state.data_db = pd.DataFrame(columns=["Date", "Projet", "Budget", "Statut", "Responsable"])

# --- PAGE 1 : SAISIE DE DONNÉES ---
if menu == "Saisie de Données":
    st.header("📝 Collecte de Données")
    st.subheader("Enregistrer un nouveau projet ou une activité")
    
    with st.expander("Ouvrir le formulaire de saisie", expanded=True):
        with st.form("form_saisie"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom_projet = st.text_input("Nom du Projet / Client", placeholder="Ex: ATECHO IMMOBILIER")
                budget = st.number_input("Budget (FCFA)", min_value=0, step=5000, value=0)
                responsable = st.text_input("Responsable", placeholder="Nom du tech")
            
            with col2:
                date_saisie = st.date_input("Date", datetime.now())
                statut = st.selectbox("Statut actuel", ["En attente", "En cours", "Terminé", "Annulé"])
            
            submitted = st.form_submit_button("Enregistrer dans la base")
            
            if submitted:
                if nom_projet:
                    nouvelle_ligne = {
                        "Date": date_saisie,
                        "Projet": nom_projet,
                        "Budget": budget,
                        "Statut": statut,
                        "Responsable": responsable
                    }
                    st.session_state.data_db = pd.concat([st.session_state.data_db, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
                    st.success(f"✅ Données pour '{nom_projet}' enregistrées !")
                else:
                    st.error("Le nom du projet est obligatoire.")

    st.markdown("---")
    st.subheader("📋 Aperçu des données saisies")
    if not st.session_state.data_db.empty:
        st.dataframe(st.session_state.data_db, use_container_width=True)
        
        # Option pour exporter en CSV
        csv = st.session_state.data_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger la base de données (CSV)",
            data=csv,
            file_name=f"export_bmp_tech_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
    else:
        st.info("Aucune donnée enregistrée pour le moment.")

# --- PAGE 2 : DASHBOARD ANALYTIQUE ---
else:
    st.header("📈 Dashboard Analytique")
    
    if st.session_state.data_db.empty:
        st.warning("⚠️ La base de données est vide. Allez dans 'Saisie de Données' pour ajouter des informations.")
    else:
        # Calcul des indicateurs
        total_budget = st.session_state.data_db["Budget"].sum()
        count_projets = len(st.session_state.data_db)
        projets_finis = len(st.session_state.data_db[st.session_state.data_db["Statut"] == "Terminé"])
        
        # Affichage des métriques
        m1, m2, m3 = st.columns(3)
        m1.metric("Projets Totaux", count_projets)
        m2.metric("Budget Global", f"{total_budget:,.0f} FCFA")
        m3.metric("Projets Terminés", projets_finis)
        
        st.markdown("---")
        
        # Graphiques
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📊 Répartition par Statut")
            fig_pie = px.pie(
                st.session_state.data_db, 
                names='Statut', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.subheader("💰 Budget par Projet")
            fig_bar = px.bar(
                st.session_state.data_db, 
                x='Projet', 
                y='Budget', 
                color='Statut',
                text_auto='.2s'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("📅 Évolution temporelle des Budgets")
        df_time = st.session_state.data_db.sort_values("Date")
        fig_line = px.line(df_time, x='Date', y='Budget', markers=True, title="Chronologie des investissements")
        st.plotly_chart(fig_line, use_container_width=True)
