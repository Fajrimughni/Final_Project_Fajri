import streamlit as st

def recommend_recipe(user, df_recipe):
    # Contoh aturan sederhana:
    traditional = user['prefer_traditional'] == 'Yes'
    healthy = user['prefer_healthy'] == 'Yes'

    df_filtered = df_recipe.copy()

    if healthy:
        df_filtered = df_filtered[df_filtered['total_calories_estimated'] < 500]

    if traditional:
        df_filtered = df_filtered[df_filtered['title'].str.contains('Ayam|Nasi|Soto|Goreng', case=False)]

    # Urutkan berdasarkan popularitas
    df_filtered = df_filtered.sort_values(by='loves', ascending=False)


    return df_filtered.head(5)  # top 5 rekomendasi



