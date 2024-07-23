import random
from itertools import combinations
import streamlit as st

# Daftar nama default
default_names = [
    "Vita Fauziah N", "Kartika Ratna S", "Wenny Yuanita K", "Isnen Hadi A", "Adira Nurul I", "Rinastya Meillenia", "Novia Larasati", "Syifa Ibnu S", "Eka Nabila A", "Windy Septianti",
    "Arya Hendro Y", "Restinuri Eliza", "Feby Nabillamah", "Nifa Aulia", "Sari Subiandini", "Salsabil S", "Tarisa S", "Selvia S", "Diva F", "Akhrinda Fadya Maulani",  "M Yusran Samad",
    "Riki Abdurrochim", "Galih Fathurrochman, "Naufal Rafif Ramadhan", "Edsel Fikriwafii Hidayat", "Kharisma Nur Fitriana", "Reza Haidar Mursid", "Zaki Husna Roid", "Yusron Khoirul Muslim"
]

# Menampilkan judul aplikasi
st.title("Kombinasi Nama")

# Opsi input: checkbox untuk memilih nama dari daftar default
st.subheader("Pilih nama dari daftar yang ada:")
selected_names = []
for name in default_names:
    if st.checkbox(name):
        selected_names.append(name)

# Opsi input: textarea untuk memasukkan nama secara manual
st.subheader("Atau masukkan daftar nama secara manual, pisahkan dengan koma:")
manual_names_input = st.text_area("Masukkan daftar nama:")

if manual_names_input:
    manual_names = [name.strip() for name in manual_names_input.split(",")]
    selected_names.extend(manual_names)

# Opsi untuk memilih jumlah kombinasi yang ditampilkan
num_combinations = st.number_input("Jumlah kombinasi yang ingin ditampilkan:", min_value=1, max_value=100, value=10)

# Tombol untuk memproses kombinasi
if st.button("Proses"):
    if len(selected_names) < 10:
        st.error("Masukkan setidaknya 10 nama untuk membuat kombinasi.")
    else:
        # Menghitung semua kombinasi dari nama yang dipilih
        all_combinations = list(combinations(selected_names, 10))

        # Menghitung jumlah total kombinasi
        comb_count = len(all_combinations)

        # Menampilkan jumlah total kombinasi
        st.write("Jumlah total kombinasi yang mungkin:", comb_count)

        # Menampilkan beberapa kombinasi acak berdasarkan input pengguna
        if num_combinations > comb_count:
            st.warning(f"Hanya ada {comb_count} kombinasi yang tersedia.")
            num_combinations = comb_count

        random_combinations = random.sample(all_combinations, num_combinations)

        st.write(f"Menampilkan {num_combinations} kombinasi acak:")
        for i, combo in enumerate(random_combinations, 1):
            st.subheader(f"Kombinasi {i}:")
            for j, name in enumerate(combo, 1):
                st.write(f"{j}. {name}")
