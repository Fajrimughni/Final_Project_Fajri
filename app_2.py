import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Segmentasi Resep Berdasarkan Klaster")

# Baca file langsung dari lokal
st.info("📁 Menggunakan file 'cluster_final.csv' yang tersedia di direktori.")
resep = pd.read_csv("cluster final.csv")

# Proses fitur
resep['num_ingredients'] = resep['ingredients_list'].apply(len)
fitur = resep[['total_calories_estimated', 'loves', 'num_ingredients']]

# Standarisasi
scaler = StandardScaler()
X_scaled = scaler.fit_transform(fitur)

# Pilih jumlah klaster
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
st.subheader("📍 Visualisasi PCA 2D")
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=resep, x='pca1', y='pca2', hue='segment_label', palette='tab10', ax=ax1)
ax1.set_xlabel("PCA 1")
ax1.set_ylabel("PCA 2")
ax1.set_title("Distribusi Resep Berdasarkan Klaster")
st.pyplot(fig1)

st.subheader("📈 Korelasi Antar Fitur")
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.heatmap(resep[['total_calories_estimated', 'loves', 'num_ingredients', 'cluster']].corr(), annot=True, cmap='coolwarm', ax=ax2)
st.pyplot(fig2)

st.subheader("🔍 Lihat Data Berdasarkan Klaster")
selected_label = st.selectbox("Pilih segmen klaster:", sorted(resep['segment_label'].unique()))
filtered_df = resep[resep['segment_label'] == selected_label]
st.dataframe(filtered_df[['title', 'total_calories_estimated', 'loves', 'num_ingredients', 'segment_label']].reset_index(drop=True))