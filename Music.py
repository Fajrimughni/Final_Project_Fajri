import streamlit as st

# Fungsi untuk menambahkan musik latar
def add_background_music(music_url):
    st.audio(music_url, format="audio/mp3")

# URL file musik (pastikan URL ini dapat diakses publik)
music_url = "https://drive.google.com/uc?export=download&id=1nHFARzdqJjtL5sbfuc2E462ke36oDx26"

# Memanggil fungsi untuk menambahkan musik latar
add_background_music(music_url)
