import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from sumber import df

st.set_page_config(layout='wide')

df_dashboard = df.copy()
del df_dashboard['Agen']
del df_dashboard['Timestamp']
del df_dashboard['Tanggal Lahir']
###########################################################################################
# HEADER
with st.container(border=True):
    with st.container(border=True):
        with st.container(border=True):
            st.header(":green[Karakteristik Responden]")

# with st.expander('Data Mikro'):
#     a = df_dashboard.columns.tolist()
#     st.write(a)

    
# # METRIK
# kol1a, kol1b, kol1c = st.columns(3)
# with kol1a:
#     with st.container(border=True):
#         with st.success(""):
#             with st.container(border=True):
#                 st.write(':green[Tempat Lahir]')
#                 tempatlahir = px.pie(df_dashboard, values='Responden', names='Tempat Lahir')
#                 st.plotly_chart(tempatlahir)

# with kol1b:
#     with st.container(border=True):
#         with st.container(border=True):
#             st.write(':blue[Laki-laki]')
#             st.title(f':blue[{total_laki}]')

# with kol1c:
#     with st.container(border=True):
#         with st.container(border=True):
#             st.write(':orange[Perempuan]')
#             st.title(f':orange[{total_perempuan}]')

# #######################################################################################

# # Progres Harian
# progres = px.bar(harian, x='Tanggal', y='Responden')
# progres.update_layout(
#     xaxis_tickformat="%d %b %Y"  # Format tanggal: Hari Bulan Tahun (e.g., 22 Apr 2025)
# )

# perpostat = px.pie(df_dashboard, values='Responden', names='Asal Kampus')
# perpostat.update_layout(legend=dict(
#     orientation="h",
#     yanchor="bottom",
#     y=-0.2,
#     xanchor="center",
#     x=0.5
# ))

# # Progres per Postat
# kol2a, kol2b = st.columns(2)

# with kol2a:
#     with st.container(border=True):
#         st.success('Capaian Responden per Hari')
#         st.plotly_chart(progres, use_container_width=True)

# with kol2b:
#     with st.container(border=True):
#         st.warning('Capaian Responden per Pojok Statistik')
#         st.plotly_chart(perpostat, use_container_width=True)

# #######################################################################################
# with st.expander('Progres Berdasarkan Postat'):
#     kol1a, kol1b, kol1c = st.columns(3)

#     def tampilkan_data_kampus(nama_kampus, kolom):
#         with kolom:
#             with st.container(border=True):
#                 st.write(nama_kampus)
#                 respon_kampus = rekap_kampus[rekap_kampus['Asal Kampus'] == nama_kampus]['Responden'].iloc[0] if nama_kampus in rekap_kampus['Asal Kampus'].values else 0
#                 st.header(respon_kampus)

#     tampilkan_data_kampus('Universitas Padjadjaran', kol1a)
#     tampilkan_data_kampus('Universitas Katolik Parahyangan', kol1b)
#     tampilkan_data_kampus('Institut Pertanian Bogor', kol1c)

#     kol2a, kol2b, kol2c, kol2d = st.columns(4)

#     tampilkan_data_kampus('Universitas Indonesia', kol2a)
#     tampilkan_data_kampus('Universitas Islam Bandung', kol2b)
#     tampilkan_data_kampus('Universitas Siliwangi', kol2c)
#     tampilkan_data_kampus('Universitas Pelita Bangsa', kol2d)
        
# ########################################################################################
# rekap_agen = df_dashboard.groupby(['Asal Kampus', 'Agen'])['Responden'].count().reset_index()

# monev_batang = px.bar(rekap_agen, y='Agen', x='Responden', orientation='h')

# monev_trimep = px.treemap(rekap_agen, path=['Asal Kampus', 'Agen'], values='Responden')

# kola, kolb = st.columns(2)

# with kola:
#     with st.container(border=True):
#         st.success('Capaian per Agen')
#         st.plotly_chart(monev_batang, use_container_width=True)

# with kolb:
#     with st.container(border=True):
#         st.warning('Capaian per Pojok Statistik')
#         st.plotly_chart(monev_trimep, use_container_width=True)

st.subheader('', divider='rainbow')        
st.info('Tim Pembina Pojok Statistik @ BPS Provinsi Jawa Barat')