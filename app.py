import streamlit as st
import pandas as pd
from recommend import recommend_recipe  # fungsi yang kita buat

# Load data
df_recipe_revised = pd.read_csv("Revisi Resep Kostum Nutrisi.csv")
consumer_profile = pd.read_csv("Profil Konsumen.csv")

st.title("🍲 Rekomendasi Resep Berdasarkan Preferensi")

# Pilih pengguna
user_id = st.selectbox("Pilih User ID", consumer_profile['user_id'])

# Ambil data user
user = consumer_profile[consumer_profile['user_id'] == user_id].iloc[0]

# Tampilkan info user
st.subheader("👤 Profil Pengguna")
st.write(f"Gender: {user['gender']}")
st.write(f"Kelompok Umur: {user['age_group']}")
st.write(f"Suka Makanan Tradisional: {user['prefer_traditional']}")
st.write(f"Suka Makanan Sehat: {user['prefer_healthy']}")

# Rekomendasi
st.subheader("🍽️ Rekomendasi Resep untuk Anda")

recs = recommend_recipe(user, df_recipe_revised)

if not recs.empty:
    for _, row in recs.iterrows():
        st.markdown(f"### {row['title']}")
        st.write(f"❤️ Disukai oleh {row['loves']} orang")
        st.write(f"🔥 Kalori Perkiraan: {row['total_calories_estimated']} kcal")
        st.markdown("---")
else:
    st.warning("Tidak ada resep yang cocok dengan preferensi Anda.")
    
    
