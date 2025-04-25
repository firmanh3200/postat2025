import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout='wide')

SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQqnVCJkYL6-nHK4Bt6JMDLAGHygCbpRb3vOmuXLOpO5D7qGFiR84InumQY8HjEjVTDbKfcsxIx2a9k/pub?gid=152263470&single=true&output=csv'

@st.cache_data(ttl=600) # Refresh data setiap 10 menit
def load_data(url):
    """
    Membaca data dari Google Sheets sebagai CSV dan mengembalikan DataFrame.
    """
    csv_data = pd.read_csv(url)
    return csv_data

df = load_data(SHEET_URL)

df = df.rename(columns={'Dengan ini saya menyatakan bahwa data yang diberikan sesuai dengan kondisi yang sebenarnya, diisi tanpa paksaan dan dengan penuh kesadaran, serta dapat digunakan untuk tujuan penelitian.': 'Responden', 
                        'Nama Lengkap Agen Pojok Statistik': 'Agen', 
                        'Tempat Tinggal saat ini': 'Domisili', 
                        'Besaran Uang Kuliah Tunggal (UKT) (Ribu Rupiah)': 'UKT', 
                        'Rata-rata pengeluaran transportasi per hari (Rp)': 'Transport', 'Rata-rata pengeluaran makan/ jajan per hari (Rp)': 'Jajan', 'Rata-rata pengeluaran internet per bulan (Rp)': 'Internet', 
                        'Apakah melakukan usaha/ bisnis untuk memperoleh penghasilan?': 'Bisnis', 
                        'Platform online yang paling sering diakses dalam seminggu terakhir': 'Platform', 
                        'Operator seluler yang digunakan': 'Operator', 
                        'Rencana setelah lulus kuliah': 'Rencana', 
                        'Alamat website BPS': 'Website BPS', 
                        'Alamat website BPS Provinsi Jawa Barat': 'Website BPS Jabar', 
                        'Menu yang paling sering diakses di website BPS': 'Menu Web', 
                        'Subjek yang paling sering diakses di website BPS': 'Subjek Web', 'Menyaksikan Rilis Berita Resmi Statistik BPS Provinsi Jawa Barat': 'Rilis BRS', 
                        'Indikator statistik yang rutin dirilis oleh BPS Provinsi Jawa Barat': 'Indikator BPS', 
                        'Apakah di kampus Anda sudah tersedia Ruang Pojok Statistik': 'Ruang Postat', 
                        'Alamat Pojok Statistik Virtual': 'PSV', 
                        'Menu yang paling disukai dari Pojok Statistik Virtual': 'Menu PSV', 'Data yang diperlukan untuk tugas/ penelitian/ skripsi/ tesis/ disertasi': 'Kebutuhan Data', 
                        'Jenis Kelamin': 'Gender'})

df['Responden'] = df['Responden'].replace('Setuju',1)
# Konversi kolom 'TimeStamp' ke tipe datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Ekstrak tanggal (sebagai tipe datetime.date)
df['Tanggal'] = df['Timestamp'].dt.date

total_respon = df['Responden'].count()

# Hitung jumlah responden berdasarkan jenis kelamin
total_laki = df[df['Gender'] == 'Laki-laki']['Responden'].count()
total_perempuan = df[df['Gender'] == 'Perempuan']['Responden'].count()

rekap_kampus = df.groupby(['Asal Kampus'])['Responden'].count().reset_index()
harian = df.groupby(['Tanggal'])['Responden'].count().reset_index()

#Konversi 'Tanggal' ke datetime setelah Groupby
harian['Tanggal'] = pd.to_datetime(harian['Tanggal'])

def hitung_umur(lahir):
    today = datetime.today()
    age = today.year - lahir.year - ((today.month, today.day) < (lahir.month, lahir.day))
    return age

# Konversi kolom 'Tanggal Lahir' ke tipe datetime (PASTIKAN BARIS INI ADA)
df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], format='%m/%d/%Y')

# Hitung umur
df['Umur'] = df['Tanggal Lahir'].apply(hitung_umur)

###########################################################################################
# HEADER
with st.container(border=True):
    st.header("Monitoring Survei Mahasiswa Pojok Statistik")
    st.subheader("Provinsi Jawa Barat")
    st.success('Tanggal 23 - 26 April 2025')

# METRIK
kol1a, kol1b, kol1c = st.columns(3)
with kol1a:
    with st.container(border=True):
        with st.success(""):
            with st.container(border=True):
                st.write(':green[Jumlah Responden]')
                st.title(f':green[{total_respon}]')

with kol1b:
    with st.container(border=True):
        with st.container(border=True):
            st.write(':blue[Laki-laki]')
            st.title(f':blue[{total_laki}]')

with kol1c:
    with st.container(border=True):
        with st.container(border=True):
            st.write(':orange[Perempuan]')
            st.title(f':orange[{total_perempuan}]')

#######################################################################################

# Progres Harian
progres = px.bar(harian, x='Tanggal', y='Responden')
progres.update_layout(
    xaxis_tickformat="%d %b %Y"  # Format tanggal: Hari Bulan Tahun (e.g., 22 Apr 2025)
)

perpostat = px.pie(df, values='Responden', names='Asal Kampus')
perpostat.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.2,
    xanchor="center",
    x=0.5
))

# Progres per Postat
kol2a, kol2b = st.columns(2)

with kol2a:
    with st.container(border=True):
        st.success('Capaian Responden per Hari')
        st.plotly_chart(progres, use_container_width=True)

with kol2b:
    with st.container(border=True):
        st.warning('Capaian Responden per Pojok Statistik')
        st.plotly_chart(perpostat, use_container_width=True)

#######################################################################################
with st.expander('Progres Berdasarkan Postat'):
    kol1a, kol1b, kol1c = st.columns(3)

    def tampilkan_data_kampus(nama_kampus, kolom):
        with kolom:
            with st.container(border=True):
                st.write(nama_kampus)
                respon_kampus = rekap_kampus[rekap_kampus['Asal Kampus'] == nama_kampus]['Responden'].iloc[0] if nama_kampus in rekap_kampus['Asal Kampus'].values else 0
                st.header(respon_kampus)

    tampilkan_data_kampus('Universitas Padjadjaran', kol1a)
    tampilkan_data_kampus('Universitas Katolik Parahyangan', kol1b)
    tampilkan_data_kampus('Institut Pertanian Bogor', kol1c)

    kol2a, kol2b, kol2c, kol2d = st.columns(4)

    tampilkan_data_kampus('Universitas Indonesia', kol2a)
    tampilkan_data_kampus('Universitas Islam Bandung', kol2b)
    tampilkan_data_kampus('Universitas Siliwangi', kol2c)
    tampilkan_data_kampus('Universitas Pelita Bangsa', kol2d)
        
########################################################################################
rekap_agen = df.groupby(['Asal Kampus', 'Agen'])['Responden'].count().reset_index()

monev_batang = px.bar(rekap_agen, y='Agen', x='Responden', orientation='h')

monev_trimep = px.treemap(rekap_agen, path=['Asal Kampus', 'Agen'], values='Responden')

kola, kolb = st.columns(2)

with kola:
    with st.container(border=True):
        st.success('Capaian per Agen')
        st.plotly_chart(monev_batang, use_container_width=True)

with kolb:
    with st.container(border=True):
        st.warning('Capaian per Pojok Statistik')
        st.plotly_chart(monev_trimep, use_container_width=True)

st.subheader('', divider='rainbow')        
st.info('Tim Pembina Pojok Statistik @ BPS Provinsi Jawa Barat')