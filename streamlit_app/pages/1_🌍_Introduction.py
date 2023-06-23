import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Introduction", page_icon="🌍")


st.markdown("# Project Introduction")

st.write("The successful development and distribution of COVID-19 vaccines around the world have become a pivotal moment in the fight against the pandemic. With millions of doses administered worldwide, it is essential for public health services to keep track of the vaccination progress to monitor immunisation efforts. By consolidating vaccination data and being able to organise it in a structural manner, it is easier to assess the impact of immunisation campaigns and identify areas for improvement. If done right, we can leverage data-driven insights to combat the future pandemic and protect communities through widespread vaccination.")


st.write("With that spirit in mind, throughout this project, our team attempted to build a working and robust database for the task of vaccine distribution from the beginning. We feel that this topic is especially relevant in today’s context, given how countries across the globe have been distributing vaccinations to its people in response to the deadly COVID-19 pandemic.")


st.markdown(
"""
For this project, we:
- Designed the database with the help of Unified Modelling Language (UML) diagrams,
- Implemented the database,
- Performed data cleansing,
- Conducted preliminary data analysis.

While we acknowledge that real world data and systems are going to be much more complex and messy, this project aims to model real world systems as closely as possible.
"""
)
