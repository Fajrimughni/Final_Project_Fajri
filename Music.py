import streamlit as st

# Fungsi untuk menambahkan musik latar
def add_background_music():
    music_url = "https://drive.google.com/uc?id=1nHFARzdqJjtL5sbfuc2E462ke36oDx26"  
    st.audio(music_url, format="audio/mp3")

# Memanggil fungsi
add_background_music()
