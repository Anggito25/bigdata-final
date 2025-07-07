import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from wordcloud import WordCloud, STOPWORDS

#load dataset (github)
url = "https://raw.githubusercontent.com/Anggito25/bigdata-final/refs/heads/main/Shoes_Data.csv"
df = pd.read_csv(url)

st.title("Dashboard Analisis Sepatu: Harga & Ulasan Produk")
st.header("1️⃣ Perbandingan Data Mentah vs Data Sudah Dibersihkan")
#pembersihan kolom: hapus simbol dan konversi ke numerik
df['price'] = df['price'].replace('[₹,]', '', regex=True).astype(float)
df['rating'] = df['rating'].str.extract(r'([\d.]+)').astype(float)
df['total_reviews'] = df['total_reviews'].str.replace('[^0-9]', '', regex=True).astype(int)

# Simpan salinan data mentah (sebelum cleaning)
raw_sample = pd.read_csv(url).head()
# Tampilkan data mentah
st.subheader("**Data Mentah:**")
st.dataframe(raw_sample[['title', 'price', 'rating', 'total_reviews']])
# Tampilkan data hasil pembersihan (sudah dilakukan sebelumnya)
clean_sample = df[['title', 'price', 'rating', 'total_reviews']].head()
st.subheader("**Data Setelah Dibersihkan:**")
st.dataframe(clean_sample)

##       Bagian 1: Analisis Sepatu (Data Terstruktur)       ##
st.header("2️⃣ Analisis Data Sepatu (Data Terstruktur)")

#sidebar: filter berdasarkan shoe_types
shoe_types = sorted(df['Shoe Type'].dropna().unique())
selected_types = st.sidebar.multiselect("Pilih Tipe Sepatu:", options=shoe_types, default=shoe_types)
df_filtered = df[df['Shoe Type'].isin(selected_types)]

# Statistik ringkas
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Harga", f"₹{df_filtered['price'].mean():,.2f}")
col2.metric("Rata-rata Rating", f"{df_filtered['rating'].mean():.2f} / 5")
col3.metric("Jumlah Review Total", f"{df_filtered['total_reviews'].sum():,}")

# Distribusi harga
st.subheader("Distribusi Harga Sepatu")
plt.figure(figsize=(10, 4))
sns.histplot(df_filtered['price'], bins=30, kde=True, color='skyblue')
plt.xlabel("Harga (₹)")
plt.ylabel("Jumlah Produk")
st.pyplot(plt)
plt.clf()

#perbandingan harga sepatu men dan women
st.subheader("Rata-rata Harga Sepatu Men vs Women")
avg_price = df[df['Shoe Type'].isin(['Men', 'Women'])].groupby('Shoe Type')['price'].mean()
plt.figure(figsize=(6, 4))
sns.barplot(x=avg_price.index, y=avg_price.values, palette="pastel")
plt.ylabel("Harga Rata-rata (₹)")
plt.xlabel("Tipe Sepatu")
for i, val in enumerate(avg_price.values):
    plt.text(i, val + 10, f"₹{val:,.0f}", ha='center')
st.pyplot(plt)
plt.clf()

# Rata-rata rating per Shoe Type
st.subheader("Rata-rata Rating per Tipe Sepatu")
type_rating = df_filtered.groupby('Shoe Type')['rating'].mean().sort_values(ascending=False)
plt.figure(figsize=(8, 4))
sns.barplot(x=type_rating.index, y=type_rating.values, palette="viridis")
plt.xlabel("Tipe Sepatu")
plt.ylabel("Rata-rata Rating")
st.pyplot(plt)
plt.clf()

# Produk Termahal dan Termurah
st.subheader("Harga Tertinggi & Terendah: Sepatu Men")
men_df = df[df['Shoe Type'] == 'Men']
max_men = men_df.loc[men_df['price'].idxmax()]
min_men = men_df.loc[men_df['price'].idxmin()]
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Harga Tertinggi (Men)**")
    st.markdown(f"**{max_men['title']}**")
    st.markdown(f"Harga: ₹{max_men['price']:,.2f}")
    st.markdown(f"Rating: {max_men['rating']} | Reviews: {max_men['total_reviews']}")
with c2:
    st.markdown("**Harga Terendah (Men)**")
    st.markdown(f"**{min_men['title']}**")
    st.markdown(f"Harga: ₹{min_men['price']:,.2f}")
    st.markdown(f"Rating: {min_men['rating']} | Reviews: {min_men['total_reviews']}")

st.subheader("Harga Tertinggi & Terendah: Sepatu Women")
women_df = df[df['Shoe Type'] == 'Women']
if not women_df.empty:
    max_women = women_df.loc[women_df['price'].idxmax()]
    min_women = women_df.loc[women_df['price'].idxmin()]
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Harga Tertinggi (Women)**")
        st.markdown(f"**{max_women['title']}**")
        st.markdown(f"Harga: ₹{max_women['price']:,.2f}")
        st.markdown(f"Rating: {max_women['rating']} | Reviews: {max_women['total_reviews']}")
    with c4:
        st.markdown("**Harga Terendah (Women)**")
        st.markdown(f"**{min_women['title']}**")
        st.markdown(f"Harga: ₹{min_women['price']:,.2f}")
        st.markdown(f"Rating: {min_women['rating']} | Reviews: {min_women['total_reviews']}")

# Divider
st.divider()

##       Bagian 2: Analisis Review Sepatu (Data Tidak Terstruktur)       ##

st.header("3️⃣ Analisis Review Pelanggan (Data Tidak Terstruktur)")

# Tampilkan contoh review
st.subheader("Contoh Review")
st.dataframe(df[['reviews', 'rating']].dropna().head(10))

# Panjang teks review
df['review_length'] = df['reviews'].dropna().astype(str).apply(len)
st.subheader("Distribusi Panjang Review")
plt.figure(figsize=(10, 4))
sns.histplot(df['review_length'], bins=30, color='orange')
plt.xlabel("Jumlah Karakter")
plt.ylabel("Jumlah Review")
st.pyplot(plt)
plt.clf()

# WordCloud semua review
st.subheader("WordCloud Seluruh Review")
all_text = " ".join(df['reviews'].dropna().astype(str).str.lower())
stopwords = set(STOPWORDS)
stopwords.update(['shoe', 'shoes', 'amazon', 'product'])  # tambahan stopwords
wordcloud = WordCloud(width=800, height=400, background_color='white',
                      stopwords=stopwords).generate(all_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)
plt.clf()

# WordCloud review negatif (rating 1-2)
def extract_review_scores(rating_str):
    if pd.isna(rating_str):
        return []
    scores = re.findall(r'(\d\.\d)', rating_str)
    return [float(s) for s in scores]

df['parsed_scores'] = df['reviews_rating'].apply(extract_review_scores)
negatif_reviews = df[df['parsed_scores'].apply(lambda scores: any(score <= 2 for score in scores))]
negatif_text = " ".join(negatif_reviews['reviews'].dropna().astype(str).str.lower())

st.subheader("WordCloud Review Negatif")
stopwords = set(STOPWORDS)
stopwords.update(['shoe', 'shoes', 'amazon', 'product', 'nice', 'good', 'comfortable'])
wordcloud_neg = WordCloud(width=800, height=400, background_color='black',
                          stopwords=stopwords, colormap='Reds').generate(negatif_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_neg, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)
plt.clf()
