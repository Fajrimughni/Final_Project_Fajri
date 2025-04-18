import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from recommendation_2 import recommend_recipe, prepare_recipe_data
from penjelasan import show_info
from About import about_me
from Music import add_background_music  # Mengimpor fungsi dari music.py

# ------------------ CONFIG ------------------ #
st.set_page_config(layout="wide")
st.title("🍽️ Aplikasi Analisis & Rekomendasi Resep")

# ------------------ MENAMBAHKAN MUSIK Latar ------------------ #
# URL langsung untuk file musik di Google Drive
music_url = "https://drive.google.com/uc?id=1nHFARzdqJjtL5sbfuc2E462ke36oDx26" 

# Memanggil fungsi untuk menambahkan musik latar
add_background_music(music_url)

# ------------------ LOAD DATA ------------------ #
st.sidebar.header("📁 Data")
df_cluster = pd.read_csv("cluster final.csv")
df_recipe_revised = pd.read_csv("Revisi Resep Kostum Nutrisi.csv")
consumer_profile = pd.read_csv("Profil Konsumen.csv")

# ------------------ DATA PREPROCESSING ------------------ #
df_cluster = prepare_recipe_data(df_cluster)
df_recipe_revised = prepare_recipe_data(df_recipe_revised)

# ------------------ TAB SELEKTOR ------------------ #
tab0, tab1, tab2 = st.tabs(["ℹ️ Tentang Saya", "📊 Segmentasi Resep", "🎯 Rekomendasi Resep"])

# ------------------ TAB 0: TENTANG SAYA ------------------ #
with tab0:
    about_me()

# ------------------ TAB 1: SEGMENTASI ------------------ #
with tab1:
    st.subheader("📍 Visualisasi Segmentasi Resep Berdasarkan Klaster")

    fitur = df_cluster[['total_calories_estimated', 'loves', 'num_ingredients']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(fitur)

    k = st.slider("🔢 Pilih jumlah klaster", min_value=2, max_value=10, value=4)
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_cluster['cluster'] = kmeans.fit_predict(X_scaled)

    cluster_means = df_cluster.groupby('cluster')[['total_calories_estimated', 'loves', 'num_ingredients']].mean()
    labels = []
    for i in range(k):
        row = cluster_means.loc[i]
        if row['total_calories_estimated'] > cluster_means['total_calories_estimated'].mean():
            labels.append("Favorit Kalori Tinggi" if row['loves'] > cluster_means['loves'].mean() else "Kalori Tinggi")
        else:
            labels.append("Favorit Sehat" if row['loves'] > cluster_means['loves'].mean() else "Sehat")
    df_cluster['segment_label'] = df_cluster['cluster'].apply(lambda x:_
