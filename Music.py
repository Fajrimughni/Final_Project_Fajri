import streamlit as st

# URL file musik yang sudah diubah
music_url = "https://drive.google.com/uc?id=1nHFARzdqJjtL5sbfuc2E462ke36oDx26"

# Menambahkan musik latar
st.audio(music_url, format="audio/mp3", autoplay=True)
