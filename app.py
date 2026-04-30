import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
# scipy remplacé par calcul numpy

# ─── Configuration de la page ────────────────────────────────────────────────
st.set_page_config(
    page_title="BMP TECH - Data Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Style CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background-color: #0f1117; }

/* Métriques personnalisées */
.metric-card {
    background: linear-gradient(135deg, #1e2130 0%, #252836 100%);
    border: 1px solid #2d3149;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.metric-card .label {
    font-size: 0.78rem;
    color: #8b8fa8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
.metric-card .value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-top: 4px;
}
.metric-card .delta {
    font-size: 0.82rem;
    color: #63b3ed;
    margin-top: 2px;
}

/* Stat box */
.stat-box {
    background: #1a1d2e;
    border: 1px solid #2a2d42;
    border-left: 4px solid #667eea;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 0;
}
.stat-box .stat-label { color: #8b8fa8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; }
.stat-box .stat-value { color: #e2e8f0; font-size: 1.15rem; font-weight: 600; margin-top: 3px; }

/* Section headers */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #667eea;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    border-bottom: 2px solid #667eea33;
    padding-bottom: 8px;
    margin: 20px 0 14px 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d0f1a !important;
    border-right: 1px solid #1e2030;
}
[data-testid="stSidebar"] * { color: #c8cde4 !important; }

/* Bouton */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    height: 2.8em;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white !important;
    font-weight: 600;
    border: none;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Alertes */
.stAlert { border-radius: 8px; }

div[data-baseweb="select"] > div { background-color: #1a1d2e !important; border-color: #2d3149 !important; }
input, textarea { background-color: #1a1d2e !important; border-color: #2d3149 !important; color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Données de démonstration ─────────────────────────────────────────────────
DEMO_DATA = [
    {"Date": datetime(2024,1,15), "Projet": "ATECHO IMMOBILIER",    "Budget": 850000,  "Statut": "Terminé",    "Responsable": "Jean K."},
    {"Date": datetime(2024,2,3),  "Projet": "SABC - Site Web",       "Budget": 320000,  "Statut": "Terminé",    "Responsable": "Marie T."},
    {"Date": datetime(2024,2,28), "Projet": "MTN Mobile App",        "Budget": 1200000, "Statut": "En cours",   "Responsable": "Paul N."},
    {"Date": datetime(2024,3,10), "Projet": "Campost ERP",           "Budget": 2500000, "Statut": "En cours",   "Responsable": "Jean K."},
    {"Date": datetime(2024,4,5),  "Projet": "Boulangerie Express",   "Budget": 150000,  "Statut": "Terminé",    "Responsable": "Alice B."},
    {"Date": datetime(2024,4,20), "Projet": "Orange Money Dashboard","Budget": 980000,  "Statut": "En attente", "Responsable": "Paul N."},
    {"Date": datetime(2024,5,8),  "Projet": "Ministère Education",   "Budget": 3200000, "Statut": "En cours",   "Responsable": "Marie T."},
    {"Date": datetime(2024,5,25), "Projet": "Afriland First Bank",   "Budget": 1750000, "Statut": "En attente", "Responsable": "Jean K."},
    {"Date": datetime(2024,6,12), "Projet": "UBA Cameroun",          "Budget": 620000,  "Statut": "Annulé",     "Responsable": "Alice B."},
    {"Date": datetime(2024,7,1),  "Projet": "CANAL+ Afrique",        "Budget": 4100000, "Statut": "En cours",   "Responsable": "Paul N."},
    {"Date": datetime(2024,7,18), "Projet": "Douala Smart City",     "Budget": 5500000, "Statut": "En attente", "Responsable": "Jean K."},
    {"Date": datetime(2024,8,5),  "Projet": "Ecole Polytechnique",   "Budget": 890000,  "Statut": "Terminé",    "Responsable": "Marie T."},
]

# ─── Initialisation session ────────────────────────────────────────────────────
if 'data_db' not in st.session_state:
    st.session_state.data_db = pd.DataFrame(columns=["Date","Projet","Budget","Statut","Responsable"])

# ─── Couleurs des statuts ──────────────────────────────────────────────────────
STATUT_COLORS = {
    "Terminé":    "#48bb78",
    "En cours":   "#667eea",
    "En attente": "#f6ad55",
    "Annulé":     "#fc8181"
}
PLOTLY_TEMPLATE = "plotly_dark"

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🚀 BMP TECH")
    st.markdown("*Data Intelligence Hub*")
    st.markdown("---")
    menu = st.radio("Navigation", [
        "📝 Saisie de Données",
        "📊 Dashboard",
        "📐 Analyse Statistique",
        "📈 Évolution Temporelle"
    ])
    st.markdown("---")

    # Charger données démo
    if st.button("⚡ Charger données démo"):
        st.session_state.data_db = pd.DataFrame(DEMO_DATA)
        st.success("Données démo chargées !")

    # Upload CSV
    st.markdown("**Importer un CSV**")
    uploaded = st.file_uploader("", type=["csv"], label_visibility="collapsed")
    if uploaded:
        try:
            df_import = pd.read_csv(uploaded)
            df_import["Date"] = pd.to_datetime(df_import["Date"])
            st.session_state.data_db = df_import
            st.success(f"{len(df_import)} lignes importées !")
        except Exception as e:
            st.error(f"Erreur : {e}")

    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.caption(f"🗄️ {len(st.session_state.data_db)} enregistrement(s)")

# ─── Helper : vérifier données ────────────────────────────────────────────────
def check_data():
    if st.session_state.data_db.empty:
        st.warning("⚠️ Base de données vide. Utilisez **Saisie de Données** ou chargez la démo via la sidebar.")
        return False
    return True

df = st.session_state.data_db.copy()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — SAISIE DE DONNÉES
# ══════════════════════════════════════════════════════════════════════════════
if menu == "📝 Saisie de Données":
    st.title("📝 Saisie de Données")

    with st.expander("➕ Nouveau projet", expanded=True):
        with st.form("form_saisie"):
            c1, c2 = st.columns(2)
            with c1:
                nom_projet  = st.text_input("Nom du Projet / Client", placeholder="Ex: ATECHO IMMOBILIER")
                budget      = st.number_input("Budget (FCFA)", min_value=0, step=5000, value=0)
                responsable = st.text_input("Responsable", placeholder="Nom du tech")
            with c2:
                date_saisie = st.date_input("Date", datetime.now())
                statut      = st.selectbox("Statut", ["En attente","En cours","Terminé","Annulé"])

            if st.form_submit_button("💾 Enregistrer"):
                if nom_projet:
                    row = {"Date": date_saisie, "Projet": nom_projet,
                           "Budget": budget, "Statut": statut, "Responsable": responsable}
                    st.session_state.data_db = pd.concat(
                        [st.session_state.data_db, pd.DataFrame([row])], ignore_index=True)
                    st.success(f"✅ '{nom_projet}' enregistré !")
                    st.rerun()
                else:
                    st.error("Le nom du projet est obligatoire.")

    st.markdown("---")
    st.subheader("📋 Données enregistrées")

    if not st.session_state.data_db.empty:
        df_display = st.session_state.data_db.copy()
        df_display["Budget"] = df_display["Budget"].apply(lambda x: f"{x:,.0f} FCFA")

        # Filtres rapides
        fc1, fc2 = st.columns(2)
        with fc1:
            f_statut = st.multiselect("Filtrer par statut", options=["En attente","En cours","Terminé","Annulé"])
        with fc2:
            f_resp = st.multiselect("Filtrer par responsable",
                                    options=st.session_state.data_db["Responsable"].dropna().unique().tolist())

        df_filtered = st.session_state.data_db.copy()
        if f_statut: df_filtered = df_filtered[df_filtered["Statut"].isin(f_statut)]
        if f_resp:   df_filtered = df_filtered[df_filtered["Responsable"].isin(f_resp)]

        st.dataframe(df_filtered, use_container_width=True)

        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Télécharger CSV", csv,
                           file_name=f"bmp_tech_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime="text/csv")

        # Suppression
        with st.expander("🗑️ Supprimer un enregistrement"):
            idx = st.number_input("Index à supprimer", min_value=0,
                                   max_value=len(st.session_state.data_db)-1, step=1)
            if st.button("Supprimer cette ligne"):
                st.session_state.data_db = st.session_state.data_db.drop(index=idx).reset_index(drop=True)
                st.success("Ligne supprimée.")
                st.rerun()
    else:
        st.info("Aucune donnée. Ajoutez un projet ou chargez la démo.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard Analytique")
    if not check_data(): st.stop()

    total_budget    = df["Budget"].sum()
    count_projets   = len(df)
    projets_finis   = len(df[df["Statut"] == "Terminé"])
    budget_moyen    = df["Budget"].mean()
    taux_completion = projets_finis / count_projets * 100 if count_projets else 0

    # KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    for col, label, val in zip(
        [k1, k2, k3, k4, k5],
        ["Projets Totaux","Budget Global","Projets Terminés","Budget Moyen","Taux Completion"],
        [f"{count_projets}",
         f"{total_budget:,.0f} FCFA",
         f"{projets_finis}",
         f"{budget_moyen:,.0f} FCFA",
         f"{taux_completion:.1f}%"]
    ):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Graphiques rangée 1
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.markdown('<div class="section-title">Répartition par Statut</div>', unsafe_allow_html=True)
        statut_counts = df["Statut"].value_counts().reset_index()
        statut_counts.columns = ["Statut","Count"]
        fig_pie = px.pie(statut_counts, names="Statut", values="Count", hole=0.45,
                         color="Statut",
                         color_discrete_map=STATUT_COLORS,
                         template=PLOTLY_TEMPLATE)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               legend=dict(font=dict(color="#c8cde4")),
                               margin=dict(t=20,b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with r1c2:
        st.markdown('<div class="section-title">Budget par Projet</div>', unsafe_allow_html=True)
        df_bar = df.sort_values("Budget", ascending=True).tail(10)
        fig_bar = px.bar(df_bar, x="Budget", y="Projet", orientation="h",
                         color="Statut", color_discrete_map=STATUT_COLORS,
                         template=PLOTLY_TEMPLATE)
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               xaxis=dict(gridcolor="#1e2030"), yaxis=dict(gridcolor="#1e2030"),
                               margin=dict(t=20,b=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    # Graphiques rangée 2
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown('<div class="section-title">Budget par Responsable</div>', unsafe_allow_html=True)
        df_resp = df.groupby("Responsable")["Budget"].sum().reset_index().sort_values("Budget", ascending=False)
        fig_resp = px.bar(df_resp, x="Responsable", y="Budget",
                          color="Budget", color_continuous_scale="Viridis",
                          template=PLOTLY_TEMPLATE)
        fig_resp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                xaxis=dict(gridcolor="#1e2030"), yaxis=dict(gridcolor="#1e2030"),
                                margin=dict(t=20,b=20))
        st.plotly_chart(fig_resp, use_container_width=True)

    with r2c2:
        st.markdown('<div class="section-title">Distribution des Budgets</div>', unsafe_allow_html=True)
        fig_hist = px.histogram(df, x="Budget", nbins=12, color_discrete_sequence=["#667eea"],
                                 template=PLOTLY_TEMPLATE)
        fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                xaxis=dict(gridcolor="#1e2030"), yaxis=dict(gridcolor="#1e2030"),
                                margin=dict(t=20,b=20))
        st.plotly_chart(fig_hist, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYSE STATISTIQUE
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📐 Analyse Statistique":
    st.title("📐 Analyse Statistique Approfondie")
    if not check_data(): st.stop()

    df_num = df.copy()
    df_num["Date_num"] = pd.to_datetime(df_num["Date"]).astype(np.int64) // 10**9  # timestamp
    df_num["Budget_MFCFA"] = df_num["Budget"] / 1_000_000

    budgets = df["Budget"].dropna()

    # ── 1. Statistiques descriptives ──────────────────────────────────────────
    st.markdown('<div class="section-title">📊 Statistiques Descriptives — Budget</div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    stats_items = [
        ("Moyenne",          f"{budgets.mean():,.0f} FCFA"),
        ("Médiane",          f"{budgets.median():,.0f} FCFA"),
        ("Mode",             f"{budgets.mode().iloc[0]:,.0f} FCFA" if not budgets.mode().empty else "—"),
        ("Étendue",          f"{budgets.max() - budgets.min():,.0f} FCFA"),
        ("Variance",         f"{budgets.var():,.0f}"),
        ("Écart-type",       f"{budgets.std():,.0f} FCFA"),
        ("Coeff. Variation", f"{(budgets.std()/budgets.mean()*100):.1f}%"),
        ("Asymétrie (Skew)", f"{budgets.skew():.3f}"),
        ("Kurtosis",         f"{budgets.kurt():.3f}"),
        ("Min",              f"{budgets.min():,.0f} FCFA"),
        ("Max",              f"{budgets.max():,.0f} FCFA"),
        ("Total",            f"{budgets.sum():,.0f} FCFA"),
    ]

    cols = st.columns(4)
    for i, (label, val) in enumerate(stats_items):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">{label}</div>
                <div class="stat-value">{val}</div>
            </div>""", unsafe_allow_html=True)

    # Quartiles
    st.markdown("**Quartiles**")
    q_cols = st.columns(4)
    for i, (q, label) in enumerate([(0.25,"Q1 (25%)"),(0.5,"Q2 / Médiane (50%)"),(0.75,"Q3 (75%)"),(1.0,"Q4 (100%)")]):
        q_cols[i].markdown(f"""
        <div class="stat-box">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{budgets.quantile(q):,.0f} FCFA</div>
        </div>""", unsafe_allow_html=True)

    # ── 2. Corrélation ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🔗 Analyse de Corrélation</div>', unsafe_allow_html=True)

    df_num["Index_projet"] = range(len(df_num))
    df_corr_cols = df_num[["Budget_MFCFA", "Date_num", "Index_projet"]].rename(
        columns={"Budget_MFCFA":"Budget (MFCFA)", "Date_num":"Date (timestamp)", "Index_projet":"Index projet"})
    corr_matrix = df_corr_cols.corr()

    cc1, cc2 = st.columns([1, 1.4])

    with cc1:
        st.markdown("**Matrice de corrélation (valeurs)**")
        st.dataframe(corr_matrix.round(4).style.background_gradient(cmap="RdYlGn", vmin=-1, vmax=1),
                     use_container_width=True)

        # Pearson Budget vs Date (calcul numpy, sans scipy)
        if len(df_num) >= 3:
            x = df_num["Date_num"].values
            y = df_num["Budget"].values
            r_val = np.corrcoef(x, y)[0, 1]
            # p-value via t-distribution approchée
            n = len(x)
            t_stat = r_val * np.sqrt((n - 2) / (1 - r_val**2 + 1e-12))
            # approximation p-value two-tailed (distribution t)
            from math import lgamma, exp, pi as PI
            def t_pvalue(t, df):
                """p-value two-tailed approchée (série de Beta incomplète)."""
                x_val = df / (df + t * t)
                # Régularisation via lgamma
                lbeta = lgamma(df / 2) + lgamma(0.5) - lgamma((df + 1) / 2)
                # Intégration numérique simple (50 pas)
                steps = 500
                dt = x_val / steps
                s = 0.0
                for i in range(steps):
                    xi = (i + 0.5) * dt
                    s += (xi ** (df / 2 - 1)) * ((1 - xi) ** (-0.5))
                p = exp(np.log(max(s * dt, 1e-300)) - lbeta)
                return min(max(p, 0.0), 1.0)
            p_val = t_pvalue(abs(t_stat), n - 2)
            st.markdown(f"""
            <div class="stat-box" style="margin-top:12px">
                <div class="stat-label">Corrélation Pearson (Budget ~ Date) — calcul numpy</div>
                <div class="stat-value">r = {r_val:.4f}  |  t = {t_stat:.4f}  |  p ≈ {p_val:.4f}</div>
                <div class="delta" style="color:#8b8fa8; font-size:0.78rem; margin-top:4px">
                    {'Corrélation significative (p < 0.05)' if p_val < 0.05 else 'Corrélation non significative'}
                </div>
            </div>""", unsafe_allow_html=True)

    with cc2:
        fig_heat = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale="RdYlGn",
            zmin=-1, zmax=1,
            text=corr_matrix.round(3).values,
            texttemplate="%{text}",
            textfont={"size": 13},
            hoverongaps=False
        ))
        fig_heat.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=20,b=20,l=20,r=20),
            height=280
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # ── 3. Box Plot + Violin ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📦 Distribution des Budgets par Statut</div>', unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        fig_box = px.box(df, x="Statut", y="Budget", color="Statut",
                          points="all", color_discrete_map=STATUT_COLORS,
                          template=PLOTLY_TEMPLATE)
        fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               xaxis=dict(gridcolor="#1e2030"), yaxis=dict(gridcolor="#1e2030"),
                               margin=dict(t=20,b=20), showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    with bc2:
        fig_vio = px.violin(df, x="Statut", y="Budget", color="Statut",
                             box=True, points="all",
                             color_discrete_map=STATUT_COLORS,
                             template=PLOTLY_TEMPLATE)
        fig_vio.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               xaxis=dict(gridcolor="#1e2030"), yaxis=dict(gridcolor="#1e2030"),
                               margin=dict(t=20,b=20), showlegend=False)
        st.plotly_chart(fig_vio, use_container_width=True)

    # ── 4. Scatter Budget vs Index (régression linéaire) ──────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📉 Régression Linéaire — Budget dans le temps</div>', unsafe_allow_html=True)

    if len(df_num) >= 3:
        df_scatter = df_num.sort_values("Date_num").reset_index(drop=True)
        df_scatter["Ordre"] = range(len(df_scatter))
        m, b = np.polyfit(df_scatter["Ordre"], df_scatter["Budget"], 1)
        df_scatter["Tendance"] = m * df_scatter["Ordre"] + b

        fig_reg = go.Figure()
        fig_reg.add_trace(go.Scatter(
            x=df_scatter["Projet"], y=df_scatter["Budget"],
            mode="markers", name="Projets",
            marker=dict(size=10, color="#667eea",
                        line=dict(width=1, color="#c0c8ff")),
        ))
        fig_reg.add_trace(go.Scatter(
            x=df_scatter["Projet"], y=df_scatter["Tendance"],
            mode="lines", name=f"Tendance (pente={m:,.0f} FCFA/projet)",
            line=dict(color="#f6ad55", width=2, dash="dot")
        ))
        fig_reg.update_layout(
            template=PLOTLY_TEMPLATE,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickangle=-30, gridcolor="#1e2030"),
            yaxis=dict(gridcolor="#1e2030"),
            legend=dict(font=dict(color="#c8cde4")),
            margin=dict(t=20,b=60)
        )
        st.plotly_chart(fig_reg, use_container_width=True)

        r2 = np.corrcoef(df_scatter["Ordre"], df_scatter["Budget"])[0,1]**2
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-label">Résultats de la régression linéaire</div>
            <div class="stat-value">Pente : {m:,.0f} FCFA/projet &nbsp;|&nbsp; Ordonnée à l'origine : {b:,.0f} FCFA &nbsp;|&nbsp; R² = {r2:.4f}</div>
        </div>""", unsafe_allow_html=True)

    # ── 5. Statistiques par responsable ───────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">👤 Statistiques par Responsable</div>', unsafe_allow_html=True)

    df_resp_stats = df.groupby("Responsable")["Budget"].agg(
        Projets="count",
        Total="sum",
        Moyenne="mean",
        Variance="var",
        Ecart_type="std",
        Min="min",
        Max="max"
    ).reset_index()
    df_resp_stats["Coeff_Variation(%)"] = (df_resp_stats["Ecart_type"] / df_resp_stats["Moyenne"] * 100).round(1)
    df_resp_stats = df_resp_stats.round(0)
    st.dataframe(df_resp_stats.style.format({
        "Total": "{:,.0f}","Moyenne": "{:,.0f}","Variance": "{:,.0f}",
        "Ecart_type": "{:,.0f}","Min": "{:,.0f}","Max": "{:,.0f}"
    }), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ÉVOLUTION TEMPORELLE
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📈 Évolution Temporelle":
    st.title("📈 Évolution Temporelle")
    if not check_data(): st.stop()

    df_time = df.copy()
    df_time["Date"] = pd.to_datetime(df_time["Date"])
    df_time = df_time.sort_values("Date")
    df_time["Mois"]            = df_time["Date"].dt.to_period("M").astype(str)
    df_time["Budget_cumul"]    = df_time["Budget"].cumsum()
    df_time["Budget_mobile3"]  = df_time["Budget"].rolling(3, min_periods=1).mean()

    # ── 1. Chronologie des budgets ────────────────────────────────────────────
    st.markdown('<div class="section-title">📅 Chronologie des Investissements</div>', unsafe_allow_html=True)

    fig_time = make_subplots(rows=2, cols=1, shared_xaxes=True,
                              subplot_titles=("Budget par projet", "Budget cumulatif"),
                              vertical_spacing=0.1)
    fig_time.add_trace(go.Bar(
        x=df_time["Projet"], y=df_time["Budget"],
        name="Budget",
        marker_color=[STATUT_COLORS.get(s,"#667eea") for s in df_time["Statut"]],
        showlegend=False
    ), row=1, col=1)
    fig_time.add_trace(go.Scatter(
        x=df_time["Projet"], y=df_time["Budget_mobile3"],
        mode="lines+markers", name="Moy. mobile (3)",
        line=dict(color="#f6ad55", width=2), marker=dict(size=6)
    ), row=1, col=1)
    fig_time.add_trace(go.Scatter(
        x=df_time["Projet"], y=df_time["Budget_cumul"],
        mode="lines+markers+text", name="Cumulatif",
        line=dict(color="#48bb78", width=2),
        fill="tozeroy", fillcolor="rgba(72,187,120,0.1)",
        marker=dict(size=5)
    ), row=2, col=1)
    fig_time.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=-30, gridcolor="#1e2030"),
        xaxis2=dict(tickangle=-30, gridcolor="#1e2030"),
        yaxis=dict(gridcolor="#1e2030"),
        yaxis2=dict(gridcolor="#1e2030"),
        legend=dict(font=dict(color="#c8cde4")),
        height=500, margin=dict(t=40,b=80)
    )
    st.plotly_chart(fig_time, use_container_width=True)

    # ── 2. Agrégation mensuelle ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📆 Agrégation Mensuelle</div>', unsafe_allow_html=True)

    df_monthly = df_time.groupby("Mois").agg(
        Budget_total=("Budget","sum"),
        Nb_projets=("Projet","count"),
        Budget_moyen=("Budget","mean")
    ).reset_index()

    mc1, mc2 = st.columns(2)

    with mc1:
        fig_m1 = px.bar(df_monthly, x="Mois", y="Budget_total",
                         color="Budget_total", color_continuous_scale="Viridis",
                         title="Budget total / mois",
                         template=PLOTLY_TEMPLATE, text_auto=".2s")
        fig_m1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              xaxis=dict(tickangle=-30, gridcolor="#1e2030"),
                              yaxis=dict(gridcolor="#1e2030"), margin=dict(t=50,b=50))
        st.plotly_chart(fig_m1, use_container_width=True)

    with mc2:
        fig_m2 = px.line(df_monthly, x="Mois", y="Budget_moyen",
                          markers=True, title="Budget moyen / mois",
                          template=PLOTLY_TEMPLATE,
                          color_discrete_sequence=["#667eea"])
        fig_m2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              xaxis=dict(tickangle=-30, gridcolor="#1e2030"),
                              yaxis=dict(gridcolor="#1e2030"), margin=dict(t=50,b=50))
        st.plotly_chart(fig_m2, use_container_width=True)

    # ── 3. Évolution par statut (area chart) ──────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Évolution du Budget par Statut (Mensuel)</div>', unsafe_allow_html=True)

    df_statut_monthly = df_time.groupby(["Mois","Statut"])["Budget"].sum().reset_index()
    fig_area = px.area(df_statut_monthly, x="Mois", y="Budget", color="Statut",
                        color_discrete_map=STATUT_COLORS,
                        template=PLOTLY_TEMPLATE)
    fig_area.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=-30, gridcolor="#1e2030"),
        yaxis=dict(gridcolor="#1e2030"),
        legend=dict(font=dict(color="#c8cde4")),
        margin=dict(t=20,b=60)
    )
    st.plotly_chart(fig_area, use_container_width=True)

    # ── 4. Gantt simplifié ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📌 Vue Gantt des Projets</div>', unsafe_allow_html=True)

    df_gantt = df_time.copy()
    df_gantt["Fin_estimee"] = df_gantt["Date"] + timedelta(days=30)
    fig_gantt = px.timeline(
        df_gantt, x_start="Date", x_end="Fin_estimee",
        y="Projet", color="Statut",
        color_discrete_map=STATUT_COLORS,
        template=PLOTLY_TEMPLATE
    )
    fig_gantt.update_yaxes(autorange="reversed")
    fig_gantt.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#1e2030"),
        legend=dict(font=dict(color="#c8cde4")),
        margin=dict(t=20,b=20),
        height=max(350, len(df_gantt)*30)
    )
    st.plotly_chart(fig_gantt, use_container_width=True)