import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def prepare_recipe_data(df):
    # Hitung jumlah bahan jika belum ada
    if 'num_ingredients' not in df.columns:
        df['num_ingredients'] = df['ingredients_list'].apply(lambda x: len(eval(x)) if isinstance(x, str) else 0)
    return df

def recommend_recipe(user, df_recipe, top_n=5):
    # Pastikan num_ingredients sudah ada
    df_recipe = prepare_recipe_data(df_recipe.copy())

    # Preferensi user
    prefer_healthy = user['prefer_healthy']
    prefer_traditional = user['prefer_traditional']

    # Filter berdasarkan preferensi
    if 'health_score' in df_recipe.columns and prefer_healthy == 'Yes':
        median_health = df_recipe['health_score'].median()
        df_recipe = df_recipe[df_recipe['health_score'] >= median_health]

    if 'is_traditional' in df_recipe.columns and prefer_traditional == 'Yes':
        df_recipe = df_recipe[df_recipe['is_traditional'] == True]

    # Jika hasil kosong
    if df_recipe.empty:
        return pd.DataFrame()

    # Fitur numerik
    features = ['total_calories_estimated', 'loves', 'num_ingredients']
    available_features = [f for f in features if f in df_recipe.columns]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_recipe[available_features])

    # Hitung kemiripan
    similarity_matrix = cosine_similarity(X_scaled)
    fav_idx = df_recipe['loves'].idxmax()
    fav_pos = df_recipe.index.get_loc(fav_idx)

    similar_indices = similarity_matrix[fav_pos].argsort()[::-1][1:top_n+1]
    recommendations = df_recipe.iloc[similar_indices]

    return recommendations.reset_index(drop=True)
