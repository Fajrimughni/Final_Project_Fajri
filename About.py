import streamlit as st
def about_me():
    st.subheader('My Name is Fajri Mughni')
    st.write('My motto is Veni, Vidi, Amavi')
    st.write('A geologist experiencing background in cross-disciplinary field, which involved in applications of data science in geology (oil and gas industry), disaster management research, geological field surveys in the areas of groundwater and the oil and gas sector.')
    st.write('Proficient in some technological and operational areas, including Geological Mappping, GIS and SQL-programming software, also Operating Network Attached Storage/NAS.')
    st.title("Contact Me")
    st.write("I appreciate the opportunity to communicate in person and am also pleased to connect through the following links:")

    # LinkedIn
    st.markdown(
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/fajrimughni/)"
    )

    # GitHub
    st.markdown(
        "[![GitHub](https://img.shields.io/badge/GitHub-Profile-black)](https://github.com/Fajrimughni)"
    )

    # Email
    st.write("📧 Email: fajriilhammughni@gmail.com")