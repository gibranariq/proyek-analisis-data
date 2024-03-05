import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import datetime as dt
import streamlit as st

sns.set(style='dark')

# Load Data
hour_df = pd.read_csv("../dashboard/hour.csv")

# Rename kolom
hour_df = hour_df.rename(columns={'weathersit':'weather',
                       'yr':'year',
                       'mnth':'month',
                       'hr':'hour',
                       'hum':'humidity',
                       'cnt':'count',
                       'dteday':'dateday'})


# Drop kolom yang tidak dipakai
drop_col= ['instant', 'windspeed', 'atemp', 'humidity']
hour_df.drop(columns=drop_col, inplace=True)


# Mengganti tipe data yang salah
hour_df["dateday"] = pd.to_datetime(hour_df["dateday"])

hour_df = hour_df.rename(columns={'weathersit':'weather',
                       'yr':'year',
                       'mnth':'month',
                       'hr':'hour',
                       'hum':'humidity',
                       'cnt':'count'})

# Mengubah tipe data beberapa kolom menjadi category
cols = ['season' , 'month', 'holiday' , 'weekday' , 'workingday' , 'weather']
for col in cols :
    hour_df[col] = hour_df[col].astype('category')

# Mengubah detail keterangan agar lebih mudah dipahami
season_map = {
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
}
weekday_map = {
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
}
weather_map = {
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Extreme/Severe Weather'
}

hour_df['season'] = hour_df['season'].map(season_map)
hour_df['weekday'] = hour_df['weekday'].map(weekday_map)
hour_df['weather'] = hour_df['weather'].map(weather_map)

def lease_day_df(df):
    daily_lease_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_lease_df

def lease_registered_df(df):
    registered_lease_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_lease_df

def lease_casual_df(df):
    casual_lease_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_lease_df

def lease_weekday_df(df):
    weekday_lease_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_lease_df

def lease_workingday_df(df):
    workingday_lease_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_lease_df

def lease_holiday_df(df):
    holiday_lease_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_lease_df

def lease_season_df(df):
    season_lease_df = df.groupby(by='season').agg({
        'count': 'sum'
    })
    return season_lease_df

def lease_weather_df(df):
    weather_lease_df = df.groupby(by='weather').agg({
        'count': 'sum'
    })
    return weather_lease_df

def lease_jam_df(df):
    jam_lease_df = df.groupby(by='hour').agg({
        'count': 'sum'
    })
    return jam_lease_df



datetime_cols = ["dateday"]
hour_df.sort_values(by="dateday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_cols:
   hour_df[column] = pd.to_datetime(hour_df[column])

# Filter data
min_date = hour_df["dateday"].min()
max_date = hour_df["dateday"].max()

# Membuat sidebar
st.sidebar.title("Belajar Analsisis Data")
with st.sidebar:
    #Menambahkan logo perusahaan
    st.image("../dashboard/sepeda.png")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Membuat slider untuk range jam/waktu
    jam_awal, jam_akhir = st.slider('Tentukan range jam', 0, 23, (0, 23))

# Penyesuaian dataset sesuai range date, suhu, dan jam
main_df = hour_df[(hour_df["dateday"] >= str(start_date)) & (hour_df["dateday"] <= str(end_date))]
main_df = main_df[(main_df["hour"] >= jam_awal) & (main_df["hour"] <= jam_akhir)]

# Membuat Dataframe
df_daily_lease = lease_day_df(main_df)
df_registered_lease = lease_registered_df(main_df)
df_casual_lease = lease_casual_df(main_df)
df_weekday_lease = lease_weekday_df(main_df)
df_workingday_lease = lease_workingday_df(main_df)
df_holiday_lease = lease_holiday_df(main_df)
df_weather_lease = lease_weather_df(main_df)
df_jam_lease = lease_jam_df(main_df)
df_season_lease = lease_season_df(main_df)

# FULL DASHBOARD

#header
st.title('Share the Bike 🚲💨')

#Description
st.write("**Selamat datang di dashboard analisis Bike Sharing Dataset.**")
st.write("")
st.write("")

st.header("Sewa Harian")
col1, col2, = st.columns(2)

with col1:
    casual_lease = df_casual_lease["casual"].sum()
    st.markdown(f"Total Pengguna Biasa: **{casual_lease}**")

with col2:
    registered_lease = df_registered_lease["registered"].sum()
    st.markdown(f"Total Pengguna Terdaftar: **{registered_lease}**")

# Pertanyaan Bisnis 1
st.subheader("Pengaruh Cuaca di setiap Jamnya terhadap Peminatan Sewa Sepeda")
fig, ax = plt.subplots(figsize=(25, 10))
sns.pointplot(data=main_df, x='hour', y='count', hue='weather', ax=ax)
st.pyplot(fig)
with st.expander("Penjelasannya Kak"):
    st.caption("Cuaca memiliki pengaruh signifikan terhadap keputusan pengguna untuk menggunakan sepeda. Cuaca yang cerah dan cenderung berawan cenderung lebih disukai oleh pengguna sepeda, dibandingkan dengan cuaca yang hujan atau bersalju, atau bahkan cuaca ekstrim. Hal ini terbukti dengan adanya lonjakan aktivitas penyewaan sepeda pada jam-jam tertentu ketika cuaca terang (sekitar Jam 6 hingga 9 pagi dan Jam 16 hingga 19 sore), yang menunjukkan bahwa pengguna sepeda lebih memilih untuk bersepeda pada saat cuaca dalam kondisi yang menyenangkan. Analisis ini juga mengungkapkan bahwa cuaca ekstrim atau berat sangat jarang terjadi, yang tercermin dari sedikitnya titik data yang tercatat untuk cuaca ekstrim dalam rentang jam tertentu. Meskipun demikian, adanya titik data cuaca ekstrim pada jam 1 siang serta pada Jam 16 dan 18 sore menunjukkan bahwa ada kecenderungan bagi beberapa pengguna sepeda untuk tetap menggunakan sepeda meskipun cuaca tidak mendukung. Ini bisa diinterpretasikan sebagai indikasi bahwa sebagian pengguna sepeda memiliki komitmen yang kuat terhadap kegiatan bersepeda mereka, meskipun dihadapkan dengan kondisi cuaca yang tidak ideal.")


# Pertanyaan Bisnis 2
st.subheader("Musim dengan Peminatan Sewa Sepeda Tertinggi")
fig, ax = plt.subplots(figsize=(25,10))
sns.barplot(data=main_df, x='season', y='count', ax=ax, palette='Set2')
st.pyplot(fig)
with st.expander("Penjelasannya Kak"):
    st.caption("Preferensi pengguna sepeda cenderung berubah-ubah sepanjang musim. Dapat dilihat bahwa musim gugur (fall) menjadi musim yang paling diminati oleh orang-orang untuk menggunakan sepeda, diikuti oleh musim panas (summer) yang juga menarik minat yang signifikan. Fenomena ini mungkin terkait dengan perubahan kondisi cuaca dan lingkungan selama musim tersebut. Misalnya, musim gugur sering kali memberikan kondisi cuaca yang sejuk dan nyaman bagi pengguna sepeda, sementara musim panas menawarkan hari-hari cerah dan panas yang ideal untuk bersepeda di luar ruangan. Faktor-faktor seperti panjangnya hari, kejernihan udara, dan keindahan alam selama musim tersebut juga dapat berperan dalam menarik minat pengguna sepeda. ")


# Pertanyaan Bisnis 3
st.subheader("Hubungan Pengguna Registered dan Casual dalam Penggunaan saat Weekday, Holiday, dan Workingday")
pivot_table = hour_df.pivot_table(index='weekday', columns=['holiday', 'workingday'], values=['registered', 'casual'], aggfunc='sum')

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='g', linewidths=0.5, linecolor='black')

plt.xlabel('Holiday, Workingday')
plt.ylabel('Weekday')

st.pyplot(plt)
with st.expander("Penjelasannya Kak"):
    st.caption("Pengguna casual lebih banyak menyewa sepeda pada saat bukan hari kerja (Sabtu dan Minggu) dibanding saat hari kerja (Senin - Jumat). Di mana perbandingannya cukup jauh, yaitu dua kali lebih banyak dari hari kerja. Pengguna registered lebih banyak menyewa sepeda saat hari kerja dibanding hari libur. Namun, perbedaannya tidak terlalu jauh tidak seperti pengguna casual. Pengguna casual dan registered sama-sama jarang menyewa sepeda di saat hari libur nasional pada akhir pekan (Sabtu - Minggu) Pengguna casual dan registered sama-sama tidak menyewa sepeda di saat hari libur nasional pada hari biasa (Senin - Jumat)")

# Pertanyaan Bisnis 4
st.subheader('Pengaruh Temperatur terhadap Penggunaan Sepeda pada Jam-jam Tertentu')

plt.figure(figsize=(10, 6))
sns.scatterplot(data=hour_df, x='temp', y='count', hue='hour', palette='viridis')
plt.xlabel('Suhu (C)')
plt.ylabel('Jumlah Pengguna Sepeda')
plt.legend(title='Jam')
st.pyplot(plt)
with st.expander("Penjelasannya Kak"):
    st.caption("Ada kecenderungan penggunaan sepeda yang meningkat seiring dengan peningkatan suhu. Hal ini dapat diartikan bahwa cuaca yang lebih hangat cenderung mendorong orang untuk lebih aktif menggunakan sepeda. Observasi ini juga diperkuat oleh fakta bahwa pada jam-jam yang tergolong sebagai jam-jam terpanas dalam sehari, khususnya sekitar pukul 14:00 hingga 17:00, penggunaan sepeda mencapai puncaknya. Hal ini kemungkinan besar disebabkan oleh kondisi cuaca yang lebih nyaman dan mendukung untuk bersepeda pada saat tersebut, seperti suhu yang hangat namun tidak terlalu panas, serta cahaya matahari yang menyenangkan untuk aktivitas di luar ruangan. Dengan demikian, data ini menunjukkan bahwa faktor suhu memainkan peran penting dalam memengaruhi tingkat aktivitas bersepeda masyarakat, dengan cuaca yang lebih hangat cenderung menjadi dorongan untuk bersepeda yang lebih aktif.")






