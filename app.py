import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from recommendation_2 import recommend_recipe  # fungsi rekomendasi eksternal
from penjelasan import show_info  # Mengimpor fungsi show_info
from About import about_me  # Mengimpor fungsi about_me

# ------------------ CONFIG ------------------ #
st.set_page_config(layout="wide")
st.title("🍽️ Aplikasi Analisis & Rekomendasi Resep")

# ------------------ LOAD DATA ------------------ #
st.sidebar.header("📁 Data")
resep = pd.read_csv("cluster final.csv")
df_recipe_revised = pd.read_csv("Revisi Resep Kostum Nutrisi.csv")
consumer_profile = pd.read_csv("Profil Konsumen.csv")

# ------------------ TAB SELEKTOR ------------------ #
tab0, tab1, tab2 = st.tabs(["ℹ️ Tentang Saya", "📊 Segmentasi Resep", "🎯 Rekomendasi Resep"])

# ------------------ TAB 0: TENTANG SAYA ------------------ #
with tab0:
    about_me()  # Menampilkan informasi tentang diri pengembang dari about.py

# ------------------ TAB 1: SEGMENTASI ------------------ #
with tab1:
    st.subheader("📍 Visualisasi Segmentasi Resep Berdasarkan Klaster")

    # Fitur numerik
    resep['num_ingredients'] = resep['ingredients_list'].apply(len)
    fitur = resep[['total_calories_estimated', 'loves', 'num_ingredients']]

    # Standarisasi
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(fitur)

    # Slider klaster
    k = st.slider("🔢 Pilih jumlah klaster", min_value=2, max_value=10, value=4)
    kmeans = KMeans(n_clusters=k, random_state=42)
    resep['cluster'] = kmeans.fit_predict(X_scaled)

    # Label klaster
    cluster_means = resep.groupby('cluster')[['total_calories_estimated', 'loves', 'num_ingredients']].mean()
    labels = []
    for i in range(k):
        row = cluster_means.loc[i]
        if row['total_calories_estimated'] > cluster_means['total_calories_estimated'].mean():
            if row['loves'] > cluster_means['loves'].mean():
                labels.append("Favorit Kalori Tinggi")
            else:
                labels.append("Kalori Tinggi")
        else:
            if row['loves'] > cluster_means['loves'].mean():
                labels.append("Favorit Sehat")
            else:
                labels.append("Sehat")
    resep['segment_label'] = resep['cluster'].apply(lambda x: labels[x])

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    resep['pca1'] = X_pca[:, 0]
    resep['pca2'] = X_pca[:, 1]

    # Visualisasi
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=resep, x='pca1', y='pca2', hue='segment_label', palette='tab10', ax=ax1)
    ax1.set_title("Distribusi Resep Berdasarkan Klaster")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(resep[['total_calories_estimated', 'loves', 'num_ingredients', 'cluster']].corr(), annot=True, cmap='coolwarm', ax=ax2)
    st.subheader("📈 Korelasi Antar Fitur")
    st.pyplot(fig2)

    st.subheader("🔍 Lihat Data Berdasarkan Klaster")
    selected_label = st.selectbox("Pilih segmen klaster:", sorted(resep['segment_label'].unique()))
    filtered_df = resep[resep['segment_label'] == selected_label]
    st.dataframe(filtered_df[['title', 'total_calories_estimated', 'loves', 'num_ingredients', 'segment_label']].reset_index(drop=True))

# ------------------ TAB 2: REKOMENDASI ------------------ #
with tab2:
    st.subheader("🎯 Rekomendasi Resep Berdasarkan Preferensi Pengguna")

    user_id = st.selectbox("Pilih User ID", consumer_profile['user_id'])
    user = consumer_profile[consumer_profile['user_id'] == user_id].iloc[0]

    # Info user
    st.markdown(f"**Gender**: {user['gender']}  \n"
                f"**Kelompok Umur**: {user['age_group']}  \n"
                f"**Suka Makanan Tradisional**: {user['prefer_traditional']}  \n"
                f"**Suka Makanan Sehat**: {user['prefer_healthy']}")

    recs = recommend_recipe(user, df_recipe_revised)

    st.subheader("🍽️ Rekomendasi Resep untuk Anda")
    if not recs.empty:
        for _, row in recs.iterrows():
            st.markdown(f"### {row['title']}")
            st.write(f"❤️ Disukai oleh {row['loves']} orang")
            st.write(f"🔥 Kalori Perkiraan: {row['total_calories_estimated']} kcal")
            st.markdown("---")
    else:
        st.warning("Tidak ada resep yang cocok dengan preferensi Anda.")
