import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st



def plot_dataframe(data):
    df = pd.DataFrame(
        {
            "name": ["Roadmap", "Extras", "Issues"],
            "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
            "stars": [np.random.randint(0, 1000) for _ in range(3)],
            "views_history": [[np.random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
        }
    )
    st.dataframe(
        df,
        column_config={
            "name": "App name",
            "stars": st.column_config.NumberColumn(
                "Github Stars",
                help="Number of stars on GitHub",
                format="%d ⭐",
            ),
            "url": st.column_config.LinkColumn("App URL"),
            "views_history": st.column_config.LineChartColumn(
                "Views (past 30 days)", y_min=0, y_max=5000
            ),
        },
        hide_index=True,
    )

def home_page():
    st.markdown("<h1 style='text-align: center;'>📈 T-Corp Portfolio 📈</h1>", unsafe_allow_html=True)

    st.markdown("<h2><br>Contexte</br></h2>", unsafe_allow_html=True)
    st.markdown("Bienvenue sur le dashboard de la T-Corp parce que ici on brasse de la moula 💲💲💲")
    st.markdown("Chacun d'entre nous a plus en plus de comptes et l'objectif ici est de centraliser nos assets afin de visualiser leurs performances et répartitions 📈📉")

    st.markdown("<h2><br>Features</br></h2>", unsafe_allow_html=True)
    st.markdown("""
    * Synthètisation des assets de chacun : action, etf, crypto, livret, etc (Google Spreadsheet)
    * Récupération des données de bourse en temps réel (API Yahoo Finance)
    * Tableau récapitulatif des assets (titre, quantité, prix achat, prix actuel, variation 24h ,etc)
    * Evolution des assets  
    * Répartition des assets
    """)

    st.markdown("<h2><br>Coming soon...</br></h2>", unsafe_allow_html=True)
    st.markdown("""
    * Plus de figures d'analyse : répartition par secteur, zone géographique,etc
    * Affichage de news sur les actions suivies
    * Lien clickable vers le cours des actions
    * Possibilité de prise en compte d'investissement régulier / DCA (ex: investissement mensuel 150€ dans S&P500)
    * Scraping de données externes : immo, PER, assurance vie sous gestion, etc
    * Outils d'analyse de portefeuille et de gestion de risque : scikit-portfolio 
    * Outils de forecasting
    * Ajout des revenues / dépenses personnelles ?
    """)


def person_page(data_assets, data_prices, name):
    # Dum debug values
    total_value = 10000
    data_assets['Valeur totale'] = 50
    profit_loss = 5
    delta = round(profit_loss/total_value, 2) * 100

    # Title
    st.markdown("<h1 style='text-align: center;'>📈 T-Corp Portfolio 📈</h1>", unsafe_allow_html=True)

    # Création de deux colonnes pour net worth + profit/loss 24h
    col1_sub, col2_sub = st.columns(2)
    with col1_sub:
        st.markdown(f"<h2 style='text-align: center;'>Portfolio: {total_value}€</h2>", unsafe_allow_html=True)
    with col2_sub:
        st.metric(label="24h Profit/Loss", value=f"{profit_loss} €", delta=f"{delta} %")

    # Affichage du tableau des assets
    st.subheader('Détails des Assets')
    st.write(data_assets)

    # Création de deux colonnes pour les figures Line-Chart des valeurs et Pie-Chart de répartition
    col1_fig, col2_fig = st.columns(2)

    # Création du stacked line chart pour l'évolution du portfolio
    # Placeholder, à remplacer par vos données et votre logique de graphique
    with col1_fig:
        st.subheader('Évolution du Portfolio')
        # Créer un lineplot avec Plotly
        fig = px.line(np.random.randn(100, 2), title="Évolution de la Valeur sur le Temps")
        st.plotly_chart(fig)

    # Création du pie chart pour la répartition du portfolio
    # Placeholder, à remplacer par vos données et votre logique de graphique
    with col2_fig:
        st.subheader('Répartition du Portfolio')
        # Créer un piechart avec Plotly
        fig = px.pie(data_assets, names="Titre", values="Valeur totale", title="Répartition des Valeurs par Catégorie")
        st.plotly_chart(fig)



