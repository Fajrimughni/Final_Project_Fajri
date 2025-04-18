import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans  # Pastikan impor KMeans ada di sini
from recommendation_2 import recommend_recipe  # fungsi rekomendasi eksternal
from penjelasan import show_info  # Mengimpor fungsi show_info
from About import about_me  # Mengimpor fungsi about_me


# ------------------ CONFIG ------------------ #
st.set_page_config(layout="wide")
st.title("🍽️ Aplikasi Analisis & Rekomendasi Resep")

# ------------------ LOAD DATA ------------------ #
st.sidebar.header("📁 Data")
df_cluster = pd.read_csv("cluster final.csv")
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
    df_cluster['num_ingredients'] = df_cluster['ingredients_list'].apply(lambda x: len(eval(x)) if isinstance(x, str) else 0)
    fitur = df_cluster[['total_calories_estimated', 'loves', 'num_ingredients']]

    # Standarisasi
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(fitur)

    # Slider klaster
    k = st.slider("🔢 Pilih jumlah klaster", min_value=2, max_value=10, value=4)
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_cluster['cluster'] = kmeans.fit_predict(X_scaled)

    # Label klaster
    cluster_means = df_cluster.groupby('cluster')[['total_calories_estimated', 'loves', 'num_ingredients']].mean()
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
    df_cluster['segment_label'] = df_cluster['cluster'].apply(lambda x: labels[x])

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df_cluster['pca1'] = X_pca[:, 0]
    df_cluster['pca2'] = X_pca[:, 1]

    # Visualisasi
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df_cluster, x='pca1', y='pca2', hue='segment_label', palette='tab10', ax=ax1)
    ax1.set_title("Distribusi Resep Berdasarkan Klaster")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(df_cluster[['total_calories_estimated', 'loves', 'num_ingredients', 'cluster']].corr(), annot=True, cmap='coolwarm', ax=ax2)
    st.subheader("📈 Korelasi Antar Fitur")
    st.pyplot(fig2)

    st.subheader("🔍 Lihat Data Berdasarkan Klaster")
    selected_label = st.selectbox("Pilih segmen klaster:", sorted(df_cluster['segment_label'].unique()))
    filtered_df = df_cluster[df_cluster['segment_label'] == selected_label]
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

    # Filter data berdasarkan preferensi user
    df_filtered = df_recipe_revised.copy()

    # Filter sehat
    if 'health_score' in df_filtered.columns and user['prefer_healthy'] == 'Yes':
        median_health = df_filtered['health_score'].median()
        df_filtered = df_filtered[df_filtered['health_score'] >= median_health]

    # Filter tradisional
    if 'is_traditional' in df_filtered.columns and user['prefer_traditional'] == 'Yes':
        df_filtered = df_filtered[df_filtered['is_traditional'] == True]

    # Kalau kosong, kembalikan kosong
    if df_filtered.empty:
        st.warning("Tidak ada resep yang cocok dengan preferensi Anda.")
    else:
        # Fitur numerik untuk similarity
        features = ['total_calories_estimated', 'loves', 'num_ingredients']
        available_features = [f for f in features if f in df_filtered.columns]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_filtered[available_features])

        # Hitung cosine similarity antar resep
        similarity_matrix = cosine_similarity(X_scaled)

        # Ambil resep favorit
        fav_idx = df_filtered['loves'].idxmax()
        fav_pos = df_filtered.index.get_loc(fav_idx)

        # Ambil top_n resep paling mirip (kecuali dirinya sendiri)
        top_n = 5
        similar_indices = similarity_matrix[fav_pos].argsort()[::-1][1:top_n+1]
        recommendations = df_filtered.iloc[similar_indices]

        st.subheader("🍽️ Rekomendasi Resep untuk Anda")
        for _, row in recommendations.iterrows():
            st.markdown(f"### {row['title']}")
            st.write(f"❤️ Disukai oleh {row['loves']} orang")
            st.write(f"🔥 Kalori Perkiraan: {row['total_calories_estimated']} kcal")
            st.markdown("---")