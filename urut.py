import pandas as pd

# Baca file CSV
df = pd.read_csv("tiktokscraped.csv")

# Urutkan berdasarkan kolom label (misalnya nama kolomnya "label")
df_sorted = df.sort_values(by="label")

# Simpan kembali ke CSV jika perlu
df_sorted.to_csv("Data_Scraping.csv", index=False)
