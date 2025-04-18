import pandas as pd
import ast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def recommend_recipe(user, df_recipe, top_n=5):
    # Tambahkan kolom num_ingredients jika belum ada
    if 'num_ingredients' not in df_recipe.columns:
        df_recipe['num_ingredients'] = df_recipe['ingredients_list'].apply(
            lambda x: len(ast.literal_eval(x)) if isinstance(x, str) and x.startswith("[") else 0
        )

    # Preferensi user
    prefer_healthy = user['prefer_healthy']
    prefer_traditional = user['prefer_traditional']

    # Filter data berdasarkan preferensi user
    df_filtered = df_recipe.copy()
    
    # Filter sehat
    if 'health_score' in df_filtered.columns and prefer_healthy == 'Yes':
        median_health = df_filtered['health_score'].median()
        df_filtered = df_filtered[df_filtered['health_score'] >= median_health]
    
    # Filter tradisional
    if 'is_traditional' in df_filtered.columns and prefer_traditional == 'Yes':
        df_filtered = df_filtered[df_filtered['is_traditional'] == True]

    # Kalau kosong, kembalikan kosong
    if df_filtered.empty:
        return pd.DataFrame()

    # Fitur numerik untuk similarity
    features = ['total_calories_estimated', 'loves', 'num_ingredients']
    available_features = [f for f in features if f in df_filtered.columns]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_filtered[available_features])

    # Hitung cosine similarity antar resep
    similarity_matrix = cosine_similarity(X_scaled)

    # Asumsikan user suka resep paling populer
    fav_idx = df_filtered['loves'].idxmax()
    fav_pos = df_filtered.index.get_loc(fav_idx)

    # Ambil top_n resep paling mirip (kecuali dirinya sendiri)
    similar_indices = similarity_matrix[fav_pos].argsort()[::-1][1:top_n+1]
    recommendations = df_filtered.iloc[similar_indices]

    return recommendations.reset_index(drop=True)
