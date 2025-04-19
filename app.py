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
from Music import add_background_music  

# ------------------ CONFIG ------------------ #
st.set_page_config(layout="wide", page_title="Aplikasi Analisis & Rekomendasi Resep", page_icon="🍽️")

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        font-family: 'Consolas', monospace;  /* Menggunakan font Consolas */
    }
    .main {
        background-color: rgba(26, 188, 156, 0.3);  /* Warna hijau toska dengan transparansi 30% */
        font-family: 'Consolas', monospace;
        color: white;
    }
    .header {
        background-color: rgba(22, 160, 133, 0.3);  /* Warna hijau toska lebih gelap dengan transparansi 30% */
        color: white;
        padding: 10px;
        font-size: 32px;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: rgba(26, 188, 156, 0.3);  /* Sidebar dengan warna hijau toska dan transparansi 30% */
    }
    .stButton>button {
        background-color: #e74c3c;
        color: white;
    }
    .stSelectbox select {
        background-color: #ecf0f1;
    }
    .stDataFrame {
        background-color: rgba(236, 240, 241, 0.7);  /* DataFrame dengan latar belakang transparan */
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍽️ Aplikasi Analisis & Rekomendasi Resep")

# Tentukan path file musik
music_url = "https://www.dropbox.com/scl/fi/qwjr1gnphqz2b4okp6l3a/Lady-Gaga-Close-To-You-HipHopKit.com.mp3?rlkey=ne5pn38xrojjyde0jrpzpymrs&st=pjqbg1rs&dl=1"
add_background_music(music_url)

# ------------------ LOAD DATA ------------------ #
df_cluster = pd.read_csv("cluster final.csv")
df_recipe_revised = pd.read_csv("Revisi Resep Kostum Nutrisi.csv")
consumer_profile = pd.read_csv("Profil Konsumen.csv")

# ------------------ DATA PREPROCESSING ------------------ #
df_cluster = prepare_recipe_data(df_cluster)
df_recipe_revised = prepare_recipe_data(df_recipe_revised)

# ------------------ SIDEBAR: PILIHAN ------------------ #
menu_selection = st.sidebar.radio("Pilih Menu", ["Tentang Saya", "Project"])

# ------------------ SIDEBAR: TENTANG SAYA ------------------ #
if menu_selection == "Tentang Saya":
    st.sidebar.header("ℹ️ Tentang Saya")
    about_me()  # Menampilkan fungsi tentang saya di sidebar

# ------------------ SIDEBAR: PROJECT ------------------ #
elif menu_selection == "Project":
    st.sidebar.header("📚 Pilih Project")
    project_selection = st.sidebar.radio(
        "Pilih bagian project:",
        ("Segmentasi Resep", "Rekomendasi Resep")
    )

    # ------------------ SEGMENTASI RESEP ------------------ #
    if project_selection == "Segmentasi Resep":
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
        df_cluster['segment_label'] = df_cluster['cluster'].apply(lambda x: labels[x])

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        df_cluster['pca1'] = X_pca[:, 0]
        df_cluster['pca2'] = X_pca[:, 1]

        # Visualisasi 1
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df_cluster, x='pca1', y='pca2', hue='segment_label', palette='tab10', ax=ax1)
        ax1.set_title("Distribusi Resep Berdasarkan Klaster")
        st.pyplot(fig1)

        # Visualisasi 2
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.heatmap(df_cluster[['total_calories_estimated', 'loves', 'num_ingredients', 'cluster']].corr(), annot=True, cmap='coolwarm', ax=ax2)
        st.subheader("📈 Korelasi Antar Fitur")
        st.pyplot(fig2)

        # Menampilkan Data Berdasarkan Klaster
        st.subheader("🔍 Lihat Data Berdasarkan Klaster")
        selected_label = st.selectbox("Pilih segmen klaster:", sorted(df_cluster['segment_label'].unique()))
        filtered_df = df_cluster[df_cluster['segment_label'] == selected_label]
        st.dataframe(filtered_df[['title', 'total_calories_estimated', 'loves', 'num_ingredients', 'segment_label']].reset_index(drop=True))

    # ------------------ REKOMENDASI RESEP ------------------ #
    elif project_selection == "Rekomendasi Resep":
        st.subheader("🎯 Rekomendasi Resep Berdasarkan Preferensi Pengguna")

        user_id = st.selectbox("Pilih User ID", consumer_profile['user_id'])
        user = consumer_profile[consumer_profile['user_id'] == user_id].iloc[0]

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
