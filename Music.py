import streamlit as st

# Fungsi untuk menambahkan musik latar
def add_background_music(music_url):
    # Menambahkan musik latar dengan URL file
    st.audio(music_url, format="audio/mp3")
