import random
from itertools import combinations
import streamlit as st

# Menampilkan judul aplikasi
st.title("Kombinasi Nama")

# Input dari pengguna
names_input = st.text_area("Masukkan daftar nama, pisahkan dengan koma:", "")

# Jika input tidak kosong, proses daftar nama
if names_input:
    # Membagi input menjadi daftar nama
    names = [name.strip() for name in names_input.split(",")]

    if len(names) < 10:
        st.error("Masukkan setidaknya 10 nama untuk membuat kombinasi.")
    else:
        # Menghitung semua kombinasi 19 orang yang dipilih 10
        all_combinations = list(combinations(names, 10))

        # Menghitung jumlah total kombinasi
        comb_count = len(all_combinations)

        # Menampilkan jumlah total kombinasi
        st.write("Jumlah total kombinasi yang mungkin:", comb_count)

        # Menampilkan beberapa kombinasi acak (contohnya 10 kombinasi acak)
        random_combinations = random.sample(all_combinations, 10)

        st.write("Beberapa kombinasi acak (10 contoh):")
        for i, combo in enumerate(random_combinations, 1):
            st.write(f"Kombinasi {i}: {combo}")
