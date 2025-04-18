import streamlit as st
import base64

def set_header_background(image_path="PRACTICE PHOTOSHOP-2.png"):
    """Menampilkan gambar sebagai header di bagian atas halaman Streamlit."""
    
    # Konversi gambar menjadi Base64
    def get_base64(file_path):
        with open(file_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return encoded

    base64_image = get_base64(image_path)

    # CSS untuk menampilkan gambar sebagai header
    st.markdown(
        f"""
        <style>
        .header-container {{
            background: url(data:image/png;base64,{base64_image}) no-repeat center top;
            background-size: cover;
            height: 200px; /* Sesuaikan tinggi header sesuai kebutuhan */
            width: 100%;
        }}
        </style>
        <div class="header-container"></div>
        """,
        unsafe_allow_html=True
    )