
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard ADABI", layout="wide")
st.title("📊 Tableau de bord - Défi ADABI")

# --- Chargement des données ---
df = pd.read_csv("ventes_clean.csv")
clients = pd.read_csv("clients_clean.csv")

# --- Simulation de date fictive aléatoire (car pas de colonne date) ---
import numpy as np
np.random.seed(0)
df["date_vente"] = pd.date_range("2024-01-01", periods=len(df), freq="D")

# --- Jointure pour ajouter les pays depuis les clients ---
df = df.merge(clients[['id_client', 'pays']], on='id_client', how='left')

# --- Filtres latéraux ---
st.sidebar.header("🎛️ Filtres")

# Magasin
magasins = sorted(df['id_magasin'].dropna().unique())
magasin = st.sidebar.selectbox("Magasin :", magasins)
df = df[df['id_magasin'] == magasin]

# Pays
pays_list = sorted(df['pays'].dropna().unique())
pays = st.sidebar.selectbox("Pays :", pays_list)
df = df[df['pays'] == pays]

# Produit
produits = sorted(df['id_produit'].dropna().unique())
produit = st.sidebar.selectbox("Produit :", produits)
df = df[df['id_produit'] == produit]

# Période
date_min = df['date_vente'].min()
date_max = df['date_vente'].max()
start_date = st.sidebar.date_input("Date de début", date_min)
end_date = st.sidebar.date_input("Date de fin", date_max)
df = df[(df['date_vente'] >= pd.to_datetime(start_date)) & (df['date_vente'] <= pd.to_datetime(end_date))]

# --- KPIs ---
st.subheader("📌 Indicateurs Clés")
col1, col2, col3 = st.columns(3)
col1.metric("Chiffre d'affaires", f"{df['montant_total'].sum():,.0f} FCFA")
col2.metric("Prix unitaire moyen", f"{df['prix_unitaire'].mean():,.0f} FCFA")
col3.metric("Quantité totale", int(df['quantité'].sum()))

# --- Graphique 1 : Répartition des ventes par client ---
st.subheader("👥 Top Clients du produit sélectionné")
top_clients = df['id_client'].value_counts().head(5)
fig1, ax1 = plt.subplots()
top_clients.plot(kind='bar', ax=ax1)
ax1.set_xlabel("ID Client")
ax1.set_ylabel("Nb Achats")
ax1.set_title("Top 5 Clients")
st.pyplot(fig1)

# --- Graphique 2 : Évolution journalière ---
st.subheader("📅 Évolution journalière des ventes")
df_daily = df.groupby("date_vente")["montant_total"].sum()
fig2, ax2 = plt.subplots()
df_daily.plot(ax=ax2)
ax2.set_xlabel("Date")
ax2.set_ylabel("CA journalier")
ax2.set_title("Chiffre d'affaires dans le temps")
st.pyplot(fig2)
