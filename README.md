# analisis-data-penjualan-game

# Dashboard Penjualan Video Game 🎮

Proyek ini merupakan dashboard interaktif berbasis Streamlit untuk menganalisis dan memvisualisasikan data penjualan video game secara global.

## 🎯 Pertanyaan Bisnis
Dashboard ini bertujuan untuk menjawab pertanyaan-pertanyaan berikut:
- Platform mana yang memiliki total penjualan global tertinggi sepanjang waktu?
- Genre game apa yang paling populer berdasarkan total penjualan global?
- Bagaimana tren penjualan video game secara global dari tahun ke tahun?
- Platform mana yang menjadi pemimpin penjualan setiap tahunnya sejak tahun 1980?

## 📊 Fitur Dashboard
- Filter berdasarkan tahun dan wilayah (NA, EU, JP, Other).
- Analisis penjualan berdasarkan genre, platform, dan publisher.
- Visualisasi tren penjualan global tahunan.
- Grafik distribusi penjualan berdasarkan genre dan wilayah.
- Tampilan interaktif dengan pengaturan jumlah item teratas (Top-N).

## 🛠️ Teknologi
- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn

## 📁 Dataset
Dataset yang digunakan adalah [Video Game Sales](https://www.kaggle.com/datasets/anandshaw2001/video-game-sales) dari Kaggle, berisi informasi tentang penjualan video game berdasarkan region dan platform sejak tahun 1980-an.

## 🚀 Cara Menjalankan
1. Pastikan Python dan Streamlit sudah terinstal.
2. Jalankan perintah berikut:
   ```
   streamlit run dashboard.py
📌 Catatan
Pastikan file vgsales.csv tersedia di direktori yang sama dengan file notebook.

Beberapa data mungkin mengandung nilai kosong yang telah ditangani dengan median atau modus sesuai konteks.

✨ Kontributor
andry septian syahputra tumaruk
