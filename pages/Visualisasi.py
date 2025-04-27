from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
from sumber import df
from datetime import datetime

st.set_page_config(layout='wide')

df_analisis = df.copy()
del df_analisis['Agen']
del df_analisis['Timestamp']
del df_analisis['Tanggal Lahir']
del df_analisis['Asal Kampus']
del df_analisis['Tanggal']

with st.container(border=True):
    st.title(':green[Visualisasi Data menggunakan Pygwalker]')

###########################################################################################
# Import your data

 
pyg_app = StreamlitRenderer(df_analisis)
 
pyg_app.explorer()

