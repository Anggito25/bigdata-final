import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

##       Bagian 1: Analisis Spesifikasi HP       ##

st.title("Dashboard Analisis: Harga Ponsel & Review Produk")
st.header("1️⃣ Analisis Spesifikasi Ponsel (Data Terstruktur)")

#load dataset GSM Arena
gsm_url = "https://raw.githubusercontent.com/Anggito25/finalproject-bigdata/refs/heads/main/gsmarena_phone.csv"
df_spec = pd.read_csv(gsm_url)

#bersihkan kolom brand
df_spec['phone_brand'] = df_spec['phone_brand'].fillna('Unknown').str.strip().str.title()

#filter kolom penting
df_selected = df_spec[['phone_brand', 'phone_model', 'price_USD', 'storage', 'ram', 'Year']]

#sidebar filter
phone_brand = sorted(df_selected['phone_brand'].unique())
selected_brands = st.sidebar.multiselect("Pilih Brand Handphone:", options=phone_brand, default=phone_brand)
df_filtered = df_selected[df_selected['phone_brand'].isin(selected_brands)]

#statistik
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata Harga", f"${df_filtered['price_USD'].mean():,.2f}")
col2.metric("Median Harga", f"${df_filtered['price_USD'].median():,.2f}")
col3.metric("Rata-rata RAM", f"{df_filtered['ram'].mean():.2f} GB")
col4.metric("Rata-rata Storage", f"{df_filtered['storage'].mean():.2f} GB")

#grafik distribusi harga
st.subheader("Distribusi Harga Ponsel")
plt.figure(figsize=(10, 4))
sns.histplot(df_filtered['price_USD'], kde=True, bins=30, color='skyblue')
plt.xlabel("Harga (USD)")
plt.ylabel("Jumlah Ponsel")
st.pyplot(plt)
plt.clf()

#grafik harga rata-rata per brand
st.subheader("Rata-rata Harga per Brand")
top_brand_price = df_filtered.groupby('phone_brand')['price_USD'].mean().sort_values(ascending=False).head(15)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_brand_price.values, y=top_brand_price.index, palette='viridis')
plt.xlabel("Harga Rata-rata (USD)")
plt.ylabel("Brand")
st.pyplot(plt)
plt.clf()

#HP Termahal dan Termurah
st.subheader("Perbandingan Harga Tertinggi dan Terendah")
max_row = df_filtered.loc[df_filtered['price_USD'].idxmax()]
min_row = df_filtered.loc[df_filtered['price_USD'].idxmin()]
c1, c2 = st.columns(2)
with c1:
    st.markdown("### Harga Tertinggi")
    st.markdown(f"**{max_row['phone_brand']} {max_row['phone_model']}**")
    st.markdown(f"Harga: **${max_row['price_USD']:,.2f}**")
    st.markdown(f"RAM: {max_row['ram']} GB | Storage: {max_row['storage']} GB")
    st.markdown(f"Tahun Rilis: {int(max_row['Year'])}")

with c2:
    st.markdown("### Harga Terendah")
    st.markdown(f"**{min_row['phone_brand']} {min_row['phone_model']}**")
    st.markdown(f"Harga: **${min_row['price_USD']:,.2f}**")
    st.markdown(f"RAM: {min_row['ram']} GB | Storage: {min_row['storage']} GB")
    st.markdown(f"Tahun Rilis: {int(min_row['Year'])}")

#rata-rata harga iPhone dari tahun ke tahun
iphone_df = df_selected[df_selected['phone_brand'] == 'Apple']
iphone_trend = iphone_df.groupby('Year')['price_USD'].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=iphone_trend.index, y=iphone_trend.values, marker='o', color='red')
plt.title('Rata-rata Harga iPhone dari Tahun ke Tahun')
plt.xlabel('Tahun')
plt.ylabel('Rata-rata Harga (USD)')
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Divider
st.divider()

##       Bagian 2: Analisis Review Produk (Lazada)       ##

st.header("2️⃣ Analisis Review Produk di Lazada (Data Tidak Terstruktur)")

#load dataset Lazada
lazada_url = "https://raw.githubusercontent.com/Anggito25/finalproject-bigdata/refs/heads/main/Lazada.csv"
df_lazada = pd.read_csv(lazada_url)

#tampilkan contoh data review
st.subheader("Contoh Review")
st.dataframe(df_lazada[['content', 'score']].dropna().head(10))

#distribusi panjang review
df_lazada['review_length'] = df_lazada['content'].dropna().astype(str).apply(len)
st.subheader("Distribusi Panjang Review")
plt.figure(figsize=(10, 4))
sns.histplot(df_lazada['review_length'], bins=30, color='orange')
plt.xlabel("Jumlah Karakter")
plt.ylabel("Jumlah Review")
st.pyplot(plt)
plt.clf()

st.subheader("WordCloud Review Pelanggan")
#siapkan teks dan stopwords
text = " ".join(df_lazada['content'].dropna().astype(str).str.lower())
#stopwords, hapus kata yang terlalu umum
stopwords = set(STOPWORDS)
stopwords.update(['lazada', 'app', 'item'])
#buat WordCloud dengan stopwords
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    stopwords=stopwords
).generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)
plt.clf()

#filter review dengan skor rendah (1 dan 2)
negatif_reviews = df_lazada[df_lazada['score'].isin([1, 2])]
#tampilkan contoh review negatif
st.subheader("Contoh Review Negatif")
st.dataframe(negatif_reviews[['score', 'content']].dropna().head(10))
#wordCloud dari review negatif
st.subheader("WordCloud Review Negatif")
negatif_text = " ".join(negatif_reviews['content'].dropna().astype(str).str.lower())
#stopwords, hapus kata yang terlalu umum
stopwords = set(STOPWORDS)
stopwords.update(['lazada', 'app', 'item'])
#buat WordCloud
wordcloud_neg = WordCloud(
    width=800,
    height=400,
    background_color='black',
    stopwords=stopwords,
    colormap='Reds'
).generate(negatif_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_neg, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)
plt.clf()
