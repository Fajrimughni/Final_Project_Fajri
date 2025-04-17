import streamlit as st

def show_info():
    st.markdown("""
    ### ℹ️ Informasi Aplikasi

    Aplikasi ini terdiri dari **dua bagian utama**:

    1. **Segmentasi Resep Berdasarkan Klaster**  
       Menyediakan visualisasi dan pengelompokan resep ke dalam segmen seperti *"Favorit Kalori Tinggi"*, *"Favorit Sehat"*, dll berdasarkan fitur nutrisi, popularitas (jumlah disukai), dan jumlah bahan.

    2. **Sistem Rekomendasi Resep**  
       Sistem ini hanya berlaku untuk **pengguna yang sudah ada (existing users)** berdasarkan data pada _Profil Konsumen_.  
       Rekomendasi diberikan berdasarkan **preferensi pengguna**, seperti kesukaan terhadap makanan sehat atau tradisional.

    > Sistem rekomendasi menggunakan pendekatan *similar search* dari profil pengguna terhadap kumpulan resep yang telah dinormalisasi dan dianalisis sebelumnya.
    """)
