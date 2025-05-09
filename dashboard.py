# Import library utama
import streamlit as st 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman Streamlit
st.set_page_config(layout="wide")
st.title("📊 Dashboard Penjualan Video Game 🎮")

# Fungsi untuk load dataset dengan cache
@st.cache_data
def load_data():
    df = pd.read_csv("data/vgsales.csv", encoding='latin-1')
    df['Year'].fillna(df['Year'].median(), inplace=True)
    df['Publisher'].fillna(df['Publisher'].mode()[0], inplace=True)
    return df

df = load_data()

# ========== SIDEBAR ========== #
with st.sidebar:
    st.header("Filter Tahun")
    year_range = st.slider("Pilih Rentang Tahun", int(df['Year'].min()), int(df['Year'].max()), (1980, 2020))

    st.header("Filter berdasarkan Region")
    show_na = st.checkbox("Tampilkan NA_Sales", value=True)
    show_eu = st.checkbox("Tampilkan EU_Sales", value=True)
    show_jp = st.checkbox("Tampilkan JP_Sales", value=True)
    show_other = st.checkbox("Tampilkan Other_Sales", value=True)

    selected_columns = []
    if show_na: selected_columns.append('NA_Sales')
    if show_eu: selected_columns.append('EU_Sales')
    if show_jp: selected_columns.append('JP_Sales')
    if show_other: selected_columns.append('Other_Sales')

    st.header("Pengaturan Grafik")
    max_top = min(20, len(df))
    top_n = st.slider("Jumlah Game Teratas", 1, max_top, 10)    

    

    st.header("Pilih Genre")
    genres_sidebar = sorted(df['Genre'].unique())
    selected_genre_radio = st.radio("Pilih satu genre", genres_sidebar)

# ========== FILTER DATA ========== #
df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# ===== Panel Atas: Ringkasan Genre =====
st.subheader("Penjualan Video Game Berdasarkan Genre")
selected_genre = st.selectbox("Pilih Genre untuk Analisis Spesifik", genres_sidebar)
genre_data = df[df['Genre'] == selected_genre]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Jumlah Data", f"{len(genre_data)} data")
col2.metric("NA_Sales", f"{genre_data['NA_Sales'].sum():.2f} Juta unit")
col3.metric("EU_Sales", f"{genre_data['EU_Sales'].sum():.2f} Juta unit")
col4.metric("JP_Sales", f"{genre_data['JP_Sales'].sum():.2f} Juta unit")

# ===== Panel Tengah: Grafik =====
col7, col8, col9 = st.columns(3)

with col7:
    st.subheader("Top 10 Platform Penjualan Global")
    platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=platform_sales.values, y=platform_sales.index, palette='viridis')
    plt.title("Top 10 Platform dengan Penjualan Global Tertinggi")
    st.pyplot(plt)

with col8:
    st.subheader("Tren Penjualan Global per Tahun")
    global_trend = df_filtered.groupby('Year')['Global_Sales'].sum()
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=global_trend.index, y=global_trend.values, marker='o')
    plt.title("Tren Penjualan Global per Tahun")
    plt.grid(True)
    st.pyplot(plt)

with col9:
    st.subheader(f"Top {top_n} Game Penjualan Tertinggi")
    top_games = df.sort_values(by='Global_Sales', ascending=False).head(top_n)
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Global_Sales', y='Name', data=top_games, palette='mako')
    plt.title(f"Top {top_n} Game")
    st.pyplot(plt)

# ===== Platform Terbaik per Tahun =====
st.subheader("Platform Terbaik per Tahun")
years = sorted(df['Year'].dropna().unique())
year_ranges = [f"{y}-{y+4}" for y in range(int(min(years)), int(max(years)) + 1, 5)]
selected_ranges = st.multiselect("Pilih Rentang Tahun (5 Tahunan)", options=year_ranges, default=year_ranges)

selected_years = []
for range_str in selected_ranges:
    start, end = map(int, range_str.split('-'))
    selected_years.extend(list(range(start, end + 1)))

top_platform_per_year = df[df['Year'].isin(selected_years)].groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()
top_per_year = top_platform_per_year.sort_values('Global_Sales', ascending=False).drop_duplicates('Year')

if not top_per_year.empty:
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Year', y='Global_Sales', hue='Platform', data=top_per_year)
    plt.title("Platform Terbaik per Tahun")
    plt.xticks(rotation=45)
    st.pyplot(plt)

# ===== Distribusi Penjualan dan Genre Region =====
col10, col11 = st.columns(2)

with col10:
    st.subheader("Distribusi Penjualan berdasarkan Region")
    if selected_columns:
        region_sum = df_filtered[selected_columns].sum()
        plt.figure(figsize=(6, 3))
        plt.pie(region_sum, labels=selected_columns, autopct='%1.1f%%', startangle=140)
        st.pyplot(plt)

with col11:
    st.subheader(f"Penjualan Genre {selected_genre_radio} per Wilayah")
    region_genres = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    selected_data = region_genres.loc[[selected_genre_radio]].T.reset_index()
    selected_data.columns = ['Wilayah', 'Penjualan']
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Wilayah', y='Penjualan', data=selected_data, palette='pastel')
    st.pyplot(plt)

# ===== Publisher dan Genre Trend =====
col12, col13 = st.columns(2)

with col12:
    st.subheader("Top Publisher berdasarkan Penjualan Global")
    top_n_publishers = st.slider("Jumlah Publisher Teratas", 1, max_top, 5)
    top_publishers = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(top_n_publishers)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_publishers.values, y=top_publishers.index, palette='plasma')
    st.pyplot(plt)

with col13:
    st.subheader("Tren Genre Game Berdasarkan Penjualan Global")
    genre_trend = df.groupby(['Year', 'Genre'])['Global_Sales'].sum().reset_index()
    selected_genre_trend = st.selectbox("Pilih Genre", sorted(genre_trend['Genre'].unique()))
    genre_filtered = genre_trend[genre_trend['Genre'] == selected_genre_trend]
    plt.figure(figsize=(12, 5))
    sns.lineplot(x='Year', y='Global_Sales', data=genre_filtered)
    st.pyplot(plt)

# ===== Distribusi Penjualan Global berdasarkan Genre =====
st.subheader("Distribusi Penjualan Global berdasarkan Genre")

# Inputan interaktif: Pilih satu atau beberapa genre yang ingin ditampilkan
available_genres = sorted(df_filtered['Genre'].unique())
selected_genres = st.multiselect("Pilih Genre", options=available_genres, default=available_genres[:12])

# Filter data berdasarkan genre yang dipilih
if selected_genres:
    genre_sales = df_filtered[df_filtered['Genre'].isin(selected_genres)].groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 5))
    sns.barplot(x=genre_sales.index, y=genre_sales.values, palette='cubehelix')
    plt.xticks(rotation=45)
    plt.ylabel("Global Sales (Juta Unit)")
    plt.title("Distribusi Penjualan Global berdasarkan Genre yang Dipilih")
    st.pyplot(plt)
else:
    st.warning("Silakan pilih minimal satu genre untuk ditampilkan.")
