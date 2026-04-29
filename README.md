# BMP TECH - Data Hub

Application Streamlit pour la gestion et l'analyse de données BMP TECH.

## 📋 Description

Interface de gestion de données pour BMP TECH dans le cadre du TP inf232. L'application propose deux fonctionnalités principales :

- **Saisie de Données** : Interface de saisie et d'enregistrement des données
- **Dashboard Analytique** : Tableau de bord analytique avec visualisations interactives

## 🛠️ Technologies

- **Streamlit** : Framework d'application web Python
- **Pandas** : Manipulation et analyse de données
- **Plotly** : Visualisations interactives

## 📦 Installation

1. Créer un environnement virtuel (optionnel mais recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 🚀 Lancement

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 📁 Structure du projet

```
bmp_tech_app_v1/
├── app.py              # Application principale Streamlit
├── requirements.txt     # Dépendances Python
├── construction.jpeg    # Image de fond
└── venv/               # Environnement virtuel
```

## ⚙️ Configuration

Le fichier `requirements.txt` contient les dépendances nécessaires :
- streamlit
- pandas
- plotly

## 📝 Auteur

Développé dans le cadre du TP inf232. par minkoulou minkoulou benoit pascal