import pandas as pd
import streamlit as st
from datetime import datetime

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

def hitung_umur(lahir):
    today = datetime.today()
    age = today.year - lahir.year - ((today.month, today.day) < (lahir.month, lahir.day))
    return age

# Konversi kolom 'Tanggal Lahir' ke tipe datetime (PASTIKAN BARIS INI ADA)
df['Tanggal Lahir'] = pd.to_datetime(df['Tanggal Lahir'], format='%m/%d/%Y')

# Hitung umur
df['Umur'] = df['Tanggal Lahir'].apply(hitung_umur)