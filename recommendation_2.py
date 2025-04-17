# recommend.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def recommend_recipe(user, df_recipe_revised, top_n=5):
    # Ambil preferensi user (contoh: suka makanan sehat)
    prefer_healthy = user['prefer_healthy']
    prefer_traditional = user['prefer_traditional']

    # Filter resep sesuai preferensi (opsional)
    df_filtered = df_recipe_revised.copy()
    if prefer_healthy == 'Yes':
        df_filtered = df_filtered[df_filtered['health_score'] >= df_filtered['health_score'].median()]
    if prefer_traditional == 'Yes':
        df_filtered = df_filtered[df_filtered['is_traditional'] == True]

    # Ambil fitur untuk similarity
    features = ['total_calories_estimated', 'loves', 'num_ingredients']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_filtered[features])

    # Hitung kemiripan antar resep
    similarity_matrix = cosine_similarity(X_scaled)

    # Asumsikan user menyukai satu atau beberapa resep, kita pilih yang paling populer dulu
    favorite_index = df_filtered['loves'].idxmax()

    similar_indices = similarity_matrix[favorite_index].argsort()[::-1][1:top_n+1]
    recommendations = df_filtered.iloc[similar_indices]

    return recommendations
