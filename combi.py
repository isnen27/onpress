import random
from itertools import combinations

# Daftar nama
names = [
    "Vita Fauziah N", "Kartika Ratna S", "Wenny Yuanita K", "Isnen Hadi A", "Adira Nurul I", "Rinastya Meillenia", "Novia Larasati", "Syifa Ibnu S", "Eka Nabila A", "Windy Septianti",
    "Arya Hendro Y", "Restinuri Eliza", "Feby Nabillamah", "Nifa Aulia", "Sari Subiandini", "Salsabil S", "Tarisa S", "Selvia S", "Diva F",
]

# Menghitung semua kombinasi 19 orang yang dipilih 10
all_combinations = list(combinations(names, 10))

# Menghitung jumlah total kombinasi
comb_count = len(all_combinations)

# Menampilkan beberapa kombinasi acak (contohnya 10 kombinasi acak)
random_combinations = random.sample(all_combinations, 10)

# Menampilkan hasil
print("Jumlah total kombinasi yang mungkin:", comb_count)
print("Beberapa kombinasi acak (10 contoh):")
for i, combo in enumerate(random_combinations, 1):
    print(f"Kombinasi {i}: {combo}")
