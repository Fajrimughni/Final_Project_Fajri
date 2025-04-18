import streamlit as st

def add_background_music(music_file):
    st.audio(music_file, format="audio/mp3", autoplay=True)


