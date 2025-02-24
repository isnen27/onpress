# for some basic operations
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#for visualizations
import matplotlib.pyplot as plt
import math
import seaborn as sns
from pandas import plotting

# for providing path
import os

# from pandas_profiling import ProfileReport
from pandas.plotting import parallel_coordinates
from IPython.display import display, Markdown

# Load dataset
@st.cache_data
@st.cache_data
def load_data():
    df = pd.read_excel('raw_Jan25.xlsx')
    return df
df = load_data()
# Fungsi untuk menghitung work_time
def calculate_work_time(row):
    tap_in = row['tap_in']
    tap_out = row['tap_out']
    
    # Jika tap_out adalah 00:00:00, maka work_time adalah negatif dari tap_in
    if tap_out == datetime.strptime('00:00:00', '%H:%M:%S').time():
        work_time = timedelta(hours=-tap_in.hour, minutes=-tap_in.minute, seconds=-tap_in.second)
    else:
        # Konversi waktu ke datetime untuk perhitungan selisih
        tap_in_dt = datetime.combine(datetime.today(), tap_in)
        tap_out_dt = datetime.combine(datetime.today(), tap_out)
        work_time = tap_out_dt - tap_in_dt
    
    return work_time

# Fungsi untuk menghitung dev_in dengan benar
def calculate_dev_in(tap_in):
    # Target waktu masuk
    target_time = timedelta(hours=7, minutes=0, seconds=0)
    # Konversi tap_in ke timedelta
    actual_time = timedelta(hours=tap_in.hour, minutes=tap_in.minute, seconds=tap_in.second)
    # Hitung selisih waktu
    delta = actual_time - target_time
    return delta
def calculate_dev_ot(work_time):
    # Target waktu kerja
    target_time = timedelta(hours=9, minutes=0, seconds=0)
    
    # Ambil total detik dari work_time
    total_seconds = int(work_time.total_seconds())
    
    # Hitung jam, menit, dan detik
    hours, remainder = divmod(abs(total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Konversi ke timedelta lagi
    actual_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    # Hitung selisih waktu
    delta = actual_time - target_time
    
    # Jika work_time negatif, pertahankan tanda negatif pada delta
    if total_seconds < 0:
        delta = -delta
    
    return delta

# Format untuk menampilkan hanya jam, menit, dan detik
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(abs(total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"-{formatted_time}" if total_seconds < 0 else formatted_time

# Menghitung work_time
df['work_time'] = df.apply(calculate_work_time, axis=1)

# Terapkan perhitungan dev_in yang benar
df['dev_in'] = df['tap_in'].apply(calculate_dev_in)

# Format dev_in agar ditampilkan sebagai waktu (tanpa days)
df['dev_in'] = df['dev_in'].apply(format_timedelta)

# Terapkan perhitungan dev_ot yang benar
df['dev_ot'] = df['work_time'].apply(calculate_dev_ot)

# Format dev_ot agar ditampilkan sebagai waktu (tanpa days)
df['dev_ot'] = df['dev_ot'].apply(format_timedelta)

# Format work_time setelah semua perhitungan selesai
df['work_time'] = df['work_time'].apply(format_timedelta)

# === Langkah 1: Definisikan Fungsi Konversi ke Timedelta ===
def convert_to_timedelta(value):
    if isinstance(value, str) and value.startswith("-"):
        # Jika waktu negatif, hilangkan tanda minus sementara, konversi, lalu jadikan negatif lagi
        td = pd.to_timedelta(value[1:])
        return -td
    else:
        try:
            return pd.to_timedelta(value)
        except:
            return pd.NaT  # Jika gagal, jadikan NaT (Not a Time)

# === Format Hasil Timedelta Tanpa '0 days' ===
def format_timedelta(td):
    if pd.isna(td):
        return 'NaT'
    if isinstance(td, pd.Timedelta):
        total_seconds = int(td.total_seconds())
        if total_seconds < 0:
            total_seconds = abs(total_seconds)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"-{hours:02}:{minutes:02}:{seconds:02}"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return td

def main():
    # Main Page Design
    st.title(':mailbox_with_mail: :blue[onPress]')
    st.header('**:blue[Monitoring Presensi]**')
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Exploratory Data Analysis :", ["- - - - -", 
                                                          "Dashboard", 
                                                          "Monitoring Unit Kerja",
                                                          "Monitoring Data Individu"])
    
    # Menu Functions
    if menu == "- - - - -":
       expand1 = st.expander("onPress")
       expand1.write('''Aplikasi **onPress** adalah sistem informasi yang digunakan dalam proses pengawasan dan pemantauan kehadiran pegawai Biro Perencanaan dan Keuangan.''')
       expand2 = st.expander("Tujuan")
       expand2.write('''Tujuan **onPress** adalah untuk mengetahui tingkat kehadiran, mengidentifikasi pola absensi, dan memastikan bahwa peraturan atau kebijakan yang berkaitan dengan kehadiran diikuti.''')
       expand3 = st.expander("Deviasi Presensi")
       expand3.write('''Deviasi presensi adalah selisih antara waktu *tap in* atau *tap out* dengan standar waktu yang telah ditentukan.

Deviasi jam masuk merupakan selisih waktu *tap in* terhadap **pukul 07.00** sebagai waktu standar jam masuk kerja.

Deviasi jam keluar merupakan selisih waktu *tap out* terhadap **pukul 16.00** sebagai waktu standar jam pulang kerja.
''')
       expand4 = st.expander("Kategori Jam Masuk")
       expand4.write('''Kategori jam masuk merupakan pengelompokkan berdasarkan besaran deviasi jam masuk kerja pegawai. 

Kategori jam masuk sebagai berikut:

1. Kategori 1 : Pegawai yang melakukan *tap in* sebelum pukul 07.00.
2. Kategori 2 : Pegawai yang melakukan *tap in* pukul 07.01 - 07.30 dengan deviasi masuk kantor antara 1 - 30 menit.
3. Kategori 3 : Pegawai yang melakukan *tap in* pukul 07.31 - 08.00 dengan deviasi masuk kantor antara 31 - 60 menit.
4. Kategori 4 : Pegawai yang melakukan *tap in* setelah pukul 08.00, tidak dalam status penugasan luar kantor atau cuti sehingga terhitung terlambat masuk kantor.
5. Kategori 5 : Pegawai yang tidak melakukan *tap in* atau melakukan *tap in* dalam rentang waktu presensi, dengan status penugasan luar kantor atau cuti.''')
       expand5 = st.expander("Kategori Jam Keluar")
       expand5.write('''Kategori jam masuk merupakan pengelompokkan berdasarkan besaran deviasi jam masuk kerja pegawai. 

Kategori jam masuk sebagai berikut:

1. Kategori 0 : Pegawai yang melakukan *tap out* sebelum pukul 16.00 tidak dalam status penugasan luar kantor atau cuti sehingga terhitung pulang lebih cepat.
2. Kategori 1 : Pegawai yang melakukan *tap out* pukul 16.00 - 17.00 dengan deviasi pulang kantor antara 1 - 60 menit.
3. Kategori 2 : Pegawai yang melakukan *tap out* pukul 17.01 - 18.00 dengan deviasi pulang kantor antara 61 - 120 menit.
4. Kategori 3 : Pegawai yang melakukan *tap out* pukul 18.01 - 19.00 dengan deviasi pulang kantor antara 121 - 180 menit.
5. Kategori 4 : Pegawai yang melakukan *tap out* setelah pukul 19.00 dengan deviasi pulang kantor diatas 180 menit.
6. Kategori 5 : Pegawai yang tidak melakukan *tap out* atau melakukan *tap out* dalam rentang waktu presensi, dengan status penugasan luar kantor atau cuti.''')
    if menu == "Dashboard":
       # === Input Pilihan Bulan ===
       bulan_dict = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
            }
       bulan_options = list(bulan_dict.keys())
       selected_month = st.selectbox("Pilih Bulan:", bulan_options, format_func=lambda x: bulan_dict[x])

       # === Filter DataFrame Berdasarkan Bulan yang Dipilih ===
       df_month = df[df["month"] == selected_month]

       # Cek Apakah Data Tersedia
       if df_month.empty:
          st.warning("Tidak ada data untuk bulan yang dipilih.")
       else:
        # === Hitung Rata-Rata Kategori Jam Masuk per Pegawai ===
        avg_cat_in = df_month.groupby(['nama', 'unit'])['cat_in'].mean().reset_index()

        # === Konversi Rata-Rata ke Kategori Terdekat ===
        avg_cat_in['avg_cat_in'] = avg_cat_in['cat_in'].round().astype(int)

        # === Hitung Jumlah Pegawai per Kategori Rata-Rata Jam Masuk ===
        kategori_counts = avg_cat_in['avg_cat_in'].value_counts().sort_index()
        # === Buat Layout untuk Grafik Bersampingan ===
        fig, axs = plt.subplots(1, 2, figsize=(20, 8))

        # === Grafik Batang Jumlah Orang per Kategori Jam Masuk Berdasarkan Unit ===
        sns.countplot(x="avg_cat_in", hue="unit", data=avg_cat_in, palette="Set2", edgecolor='white', ax=axs[0])
        axs[0].set_title('Jumlah Orang per Kategori Jam Masuk Berdasarkan Unit')
        axs[0].set_xlabel('Kategori Jam Masuk')
        axs[0].set_ylabel('Jumlah Orang')
        axs[0].legend(title='Unit', bbox_to_anchor=(1.05, -0.1), ncol=2)
        axs[0].grid(axis='y', linestyle='--', alpha=0.7)

        # === Grafik Pie Chart Porsi Pegawai per Kategori Jam Masuk ===
        axs[1].pie(
            kategori_counts,
            labels=kategori_counts.index,
            autopct='%1.1f%%',
            startangle=120,
            colors=plt.cm.Set2(range(len(kategori_counts))),
            wedgeprops={'edgecolor': 'white'}
        )
        bulan_terpilih = bulan_dict[selected_month]
        axs[1].set_title(f'Porsi Pegawai per Kategori Jam Masuk\nBulan: {bulan_terpilih}')

        # === Tampilkan Grafik di Streamlit ===
        st.subheader(':blue[Kategori Jam Masuk]')
        st.pyplot(fig)

        # === Hitung Rata-Rata Kategori Jam Keluar per Pegawai ===
        avg_cat_ot = df_month.groupby(['nama', 'unit'])['cat_ot'].mean().reset_index()

         # === Konversi Rata-Rata ke Kategori Terdekat ===
        avg_cat_ot['avg_cat_ot'] = avg_cat_ot['cat_ot'].round().astype(int)

        # === Hitung Jumlah Pegawai per Kategori Rata-Rata Jam Keluar ===
        kategori_counts2 = avg_cat_ot['avg_cat_ot'].value_counts().sort_index()
        # === Buat Layout untuk Grafik Bersampingan ===
        fig2, axs = plt.subplots(1, 2, figsize=(20, 8))

        # === Grafik Batang Jumlah Orang per Kategori Jam Keluar Berdasarkan Unit ===
        sns.countplot(x="avg_cat_ot", hue="unit", data=avg_cat_ot, palette="Set2", edgecolor='white', ax=axs[0])
        axs[0].set_title('Jumlah Orang per Kategori Jam Keluar Berdasarkan Unit')
        axs[0].set_xlabel('Kategori Jam Keluar')
        axs[0].set_ylabel('Jumlah Orang')
        axs[0].legend(title='Unit', bbox_to_anchor=(1.05, -0.1), ncol=2)
        axs[0].grid(axis='y', linestyle='--', alpha=0.7)

        # === Grafik Pie Chart Porsi Pegawai per Kategori Jam Keluar ===
        axs[1].pie(
            kategori_counts2,
            labels=kategori_counts2.index,
            autopct='%1.1f%%',
            startangle=120,
            colors=plt.cm.Set2(range(len(kategori_counts2))),
            wedgeprops={'edgecolor': 'white'}
        )
        bulan_terpilih = bulan_dict[selected_month]
        axs[1].set_title(f'Porsi Pegawai per Kategori Jam Keluar\nBulan: {bulan_terpilih}')

        # === Tampilkan Grafik di Streamlit ===
        st.subheader(':blue[Kategori Jam Masuk Keluar]')
        st.pyplot(fig2)
       
    if menu == "Monitoring Unit Kerja":
       # === Input Pilihan Bulan dari Dataset ===
       bulan_dict = {
       1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
       5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
       9: "September", 10: "Oktober", 11: "November", 12: "Desember"
       }
       bulan_options = sorted(df["month"].unique().tolist())
       selected_month = st.selectbox("Pilih Bulan:", bulan_options, format_func=lambda x: bulan_dict[x])

       # === Input Pilihan Unit dari Dataset ===
       unit_options = df["unit"].unique().tolist()
       selected_unit = st.selectbox("Pilih Unit:", unit_options)

       # === Filter DataFrame Berdasarkan Pilihan Bulan dan Unit ===
       df_filtered = df[(df["month"] == selected_month) & (df["unit"] == selected_unit)]

       # Cek Apakah Data Tersedia
       if df_filtered.empty:
          st.warning("Tidak ada data untuk kombinasi Bulan dan Unit yang dipilih.")
       else:
          # === Hitung Rata-Rata Kategori Jam Masuk per Pegawai ===
          avg_cat_in2 = df_filtered.groupby('nama')['cat_in'].mean().reset_index()
    
          # === Konversi Rata-Rata ke Kategori Terdekat ===
          avg_cat_in2['avg_cat_in2'] = avg_cat_in2['cat_in'].round().astype(int)

          # === Hitung Jumlah Pegawai per Kategori Rata-Rata Jam Masuk ===
          kategori_counts3 = avg_cat_in2['avg_cat_in2'].value_counts().sort_index()

          # === Buat Layout untuk Grafik Bersampingan ===
          fig3, axs = plt.subplots(1, 2, figsize=(20, 8))

          # === Grafik Batang Jumlah Orang per Kategori Jam Masuk Berdasarkan Unit ===
          sns.countplot(x="avg_cat_in2", data=avg_cat_in2, palette="Set2", edgecolor='black', ax=axs[0])
          axs[0].set_title(f'Jumlah Orang per Kategori Jam Masuk\nUnit: {selected_unit}')
          axs[0].set_xlabel('Kategori Jam Masuk')
          axs[0].set_ylabel('Jumlah Orang')
          axs[0].grid(axis='y', linestyle='--', alpha=0.7)
    
          # === Grafik Pie Chart Porsi Pegawai per Kategori Jam Masuk ===
          wedges, texts, autotexts = axs[1].pie(
            kategori_counts3,
            labels=kategori_counts3.index,
            autopct='%1.1f%%',
            startangle=120,
            colors=plt.cm.Set2(range(len(kategori_counts3))),
            wedgeprops={'edgecolor': 'white'}
          )
          axs[1].set_title(f'Porsi Pegawai per Kategori Jam Masuk\nUnit: {selected_unit}')

          # === Atur Legend di Bawah Kedua Grafik ===
          axs[0].legend(title='Kategori Jam Masuk', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
          axs[1].legend(wedges, kategori_counts3.index, title='Kategori Jam Masuk', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

          # === Tampilkan Grafik di Streamlit ===
          st.subheader(f'Kategori Jam Masuk Masuk')
          st.pyplot(fig3)

          # === Hitung Rata-Rata Kategori Jam Keluar per Pegawai ===
          avg_cat_ot3 = df_filtered.groupby('nama')['cat_ot'].mean().reset_index()
    
          # === Konversi Rata-Rata ke Kategori Terdekat ===
          avg_cat_ot3['avg_cat_ot3'] = avg_cat_ot3['cat_ot'].round().astype(int)

          # === Hitung Jumlah Pegawai per Kategori Rata-Rata Jam Keluar ===
          kategori_counts4 = avg_cat_ot3['avg_cat_ot3'].value_counts().sort_index()

          # === Buat Layout untuk Grafik Bersampingan ===
          fig4, axs = plt.subplots(1, 2, figsize=(20, 8))

          # === Grafik Batang Jumlah Orang per Kategori Jam Keluar Berdasarkan Unit ===
          sns.countplot(x="avg_cat_ot3", data=avg_cat_ot3, palette="Set2", edgecolor='white', ax=axs[0])
          axs[0].set_title(f'Jumlah Orang per Kategori Jam Keluar\nUnit: {selected_unit}')
          axs[0].set_xlabel('Kategori Jam Keluar')
          axs[0].set_ylabel('Jumlah Orang')
          axs[0].grid(axis='y', linestyle='--', alpha=0.7)
    
          # === Grafik Pie Chart Porsi Pegawai per Kategori Jam Keluar ===
          wedges, texts, autotexts = axs[1].pie(
            kategori_counts4,
            labels=kategori_counts4.index,
            autopct='%1.1f%%',
            startangle=120,
            colors=plt.cm.Set2(range(len(kategori_counts4))),
            wedgeprops={'edgecolor': 'white'}
          )
          axs[1].set_title(f'Porsi Pegawai per Kategori Jam Keluar\nUnit: {selected_unit}')

          # === Atur Legend di Bawah Kedua Grafik ===
          axs[0].legend(title='Kategori Jam Keluar', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
          axs[1].legend(wedges, kategori_counts4.index, title='Kategori Jam Keluar', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

          # === Tampilkan Grafik di Streamlit ===
          st.subheader(f'Kategori Jam Masuk Keluar')
          st.pyplot(fig4)

    if menu == "Monitoring Data Individu":
       # === Pilihan Unit ===
       unit_list = df["unit"].unique().tolist()
       selected_unit = st.selectbox("Pilih Unit:", unit_list)

       # === Pilihan Nama Berdasarkan Unit ===
       nama_list = df[df["unit"] == selected_unit]["nama"].unique().tolist()
       selected_nama = st.selectbox("Pilih Nama:", nama_list)

       # === Pilihan Bulan dari Dataset ===
       month_list = sorted(df["month"].unique().tolist())
       selected_month = st.selectbox("Pilih Bulan:", month_list, format_func=lambda x: f"Bulan {x}")

       # === Filter DataFrame Berdasarkan Pilihan ===
       filtered_df = df[
           (df["unit"] == selected_unit) & 
           (df["nama"] == selected_nama) & 
           (df["month"] == selected_month)
        ]

        # === Konversi dan Format Kolom Timedelta ===
       for col in ["dev_in", "dev_ot"]:
            filtered_df[col] = filtered_df[col].apply(convert_to_timedelta)
            filtered_df[col] = filtered_df[col].apply(format_timedelta)

        # === Pilih Kolom yang Akan Ditampilkan ===
       filtered_df = filtered_df[["date", "dev_in", "cat_in", "dev_ot", "cat_ot"]].rename(columns={
          "date": "Tanggal",
          "dev_in": "Deviasi Masuk",
          "cat_in": "Kategori Jam Masuk",
          "dev_ot": "Deviasi Keluar",
          "cat_ot": "Kategori Jam Keluar"
       })

       # === Perhitungan Rata-rata Kategori ===
       if not filtered_df.empty:
          avg_cat_in = round(filtered_df["Kategori Jam Masuk"].mean())
          avg_cat_ot = round(filtered_df["Kategori Jam Keluar"].mean())
    
       # === Mapping Kategori ===
       kategori_mapping = {
        1: "Sangat Awal",
        2: "Tepat Waktu",
        3: "Flexy Time",
        4: "Terlambat"
       }
       kategori_ot_mapping = {
        0: "Pulang Cepat",
        1: "Tepat Waktu",
        2: "Lembur Sedikit",
        3: "Lembur Sedang",
        4: "Lembur Banyak"
       }
    
       kategori_masuk = kategori_mapping.get(avg_cat_in, "Tidak Diketahui")
       kategori_keluar = kategori_ot_mapping.get(avg_cat_ot, "Tidak Diketahui")
    
       # === Tampilkan Hasil Kategori ===
       st.subheader("Hasil Kategori Berdasarkan Rata-rata:")
       st.markdown(f"""
       - **Kategori Jam Masuk:** {kategori_masuk} (Rata-rata: Kategori {avg_cat_in})
       - **Kategori Jam Keluar:** {kategori_keluar} (Rata-rata: Kategori {avg_cat_ot})
    """)
    else:
       st.warning("Tidak ada data untuk kombinasi Unit, Nama, dan Bulan yang dipilih.")

    # === Hitung Frekuensi Kategori Jam Masuk dan Keluar ===
    cat_in_counts = filtered_df["Kategori Jam Masuk"].value_counts().sort_index()
    cat_ot_counts = filtered_df["Kategori Jam Keluar"].value_counts().sort_index()

    # === Buat Grafik Bersebelahan ===
    fig5, axs = plt.subplots(1, 2, figsize=(20, 8))

    # Grafik Kategori Jam Masuk
    axs[0].bar(cat_in_counts.index, cat_in_counts.values, color='orange', edgecolor='black')
    axs[0].set_title('Distribusi Kategori Jam Masuk')
    axs[0].set_xlabel('Kategori')
    axs[0].set_ylabel('Frekuensi')
    axs[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Grafik Kategori Jam Keluar
    axs[1].bar(cat_ot_counts.index, cat_ot_counts.values, color='skyblue', edgecolor='black')
    axs[1].set_title('Distribusi Kategori Jam Keluar')
    axs[1].set_xlabel('Kategori')
    axs[1].set_ylabel('Frekuensi')
    axs[1].grid(axis='y', linestyle='--', alpha=0.7)

    # Tampilkan Grafik di Streamlit
    st.pyplot(fig5)

    # === Tampilkan DataFrame yang Telah Difilter ===
    st.subheader("Detail Kehadiran Pegawai:")
    st.dataframe(filtered_df)
if __name__=="__main__":
    main()
