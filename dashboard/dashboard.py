import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Analisis E-Commerce",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Analisis Data E-Commerce")

st.write("""
Dashboard ini menampilkan hasil analisis data e-commerce terkait tren pendapatan,
kategori produk dengan kontribusi pendapatan tertinggi, serta segmentasi pelanggan
berdasarkan RFM.
""")

# Load dataset
orders = pd.read_csv("data/orders_dataset.csv")
payments = pd.read_csv("data/order_payments_dataset.csv")
customers = pd.read_csv("data/customers_dataset.csv")
order_items = pd.read_csv("data/order_items_dataset.csv")
products = pd.read_csv("data/products_dataset.csv")

# Cleaning data orders
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

orders = orders.drop_duplicates()
orders = orders.dropna(subset=["order_purchase_timestamp"])

# Menggabungkan data untuk analisis revenue
df_eda = orders.merge(order_items, on="order_id")
df_eda = df_eda.merge(products, on="product_id")
df_eda = df_eda.merge(payments, on="order_id")

df_eda["order_month"] = df_eda["order_purchase_timestamp"].dt.to_period("M").astype(str)
df_eda["order_year"] = df_eda["order_purchase_timestamp"].dt.year

# Sidebar filter
st.sidebar.header("Filter Data")

year_options = sorted(df_eda["order_year"].dropna().unique())

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=year_options,
    default=year_options
)

filtered_df = df_eda[df_eda["order_year"].isin(selected_year)]

# Ringkasan metrik
st.subheader("Ringkasan Data")

total_revenue = filtered_df["payment_value"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_id"].nunique()
total_products = filtered_df["product_id"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Total Products", f"{total_products:,}")

st.divider()

# Pertanyaan 1
st.subheader("Pertanyaan 1")
st.write("""
Bagaimana tren total nilai pembayaran per bulan selama periode 2016–2018,
serta kategori produk apa yang memberikan kontribusi pendapatan tertinggi?
""")

monthly_revenue = (
    filtered_df.groupby("order_month")["payment_value"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=monthly_revenue,
    x="order_month",
    y="payment_value",
    marker="o",
    ax=ax
)

ax.set_title("Tren Pendapatan Bulanan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)

st.pyplot(fig, clear_figure=True)

st.write("""
Berdasarkan grafik tren pendapatan bulanan, total nilai pembayaran mengalami perubahan
dari waktu ke waktu. Pola ini dapat digunakan untuk melihat periode dengan peningkatan
maupun penurunan pendapatan.
""")

category_revenue = (
    filtered_df.groupby("product_category_name")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.subheader("Top 10 Kategori Produk Berdasarkan Revenue")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=category_revenue.head(10),
    x="payment_value",
    y="product_category_name",
    ax=ax
)

ax.set_title("Top 10 Kategori Produk Berdasarkan Pendapatan")
ax.set_xlabel("Total Revenue")
ax.set_ylabel("Kategori Produk")

st.pyplot(fig, clear_figure=True)

st.write("""
Kategori produk dengan pendapatan tertinggi merupakan kategori yang memberikan kontribusi
besar terhadap revenue. Kategori ini dapat menjadi fokus dalam strategi pemasaran,
pengelolaan stok, dan pengembangan bisnis.
""")

st.divider()

# Pertanyaan 2
st.subheader("Pertanyaan 2")
st.write("""
Bagaimana segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary (RFM),
serta bagaimana kontribusi masing-masing segmen terhadap total pendapatan?
""")

rfm_df = orders.merge(payments, on="order_id")
rfm_df = rfm_df.merge(customers, on="customer_id")

snapshot_date = rfm_df["order_purchase_timestamp"].max()

rfm = rfm_df.groupby("customer_id").agg({
    "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
    "order_id": "count",
    "payment_value": "sum"
}).reset_index()

rfm.columns = ["customer_id", "recency", "frequency", "monetary"]
rfm = rfm.dropna()

q25 = rfm["monetary"].quantile(0.25)
q75 = rfm["monetary"].quantile(0.75)

def segment_customer(m):
    if m >= q75:
        return "High Value"
    elif m >= q25:
        return "Medium Value"
    else:
        return "Low Value"

rfm["segment"] = rfm["monetary"].apply(segment_customer)

segment_revenue = (
    rfm.groupby("segment")["monetary"]
    .sum()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Segmentasi Pelanggan")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(
        data=rfm,
        x="segment",
        order=["High Value", "Medium Value", "Low Value"],
        ax=ax
    )

    ax.set_title("Distribusi Segment Pelanggan")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Jumlah Pelanggan")

    st.pyplot(fig, clear_figure=True)

with col2:
    st.subheader("Kontribusi Revenue per Segment")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=segment_revenue,
        x="segment",
        y="monetary",
        order=["High Value", "Medium Value", "Low Value"],
        ax=ax
    )

    ax.set_title("Kontribusi Revenue per Segment")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Total Revenue")

    st.pyplot(fig, clear_figure=True)

st.write("""
Hasil analisis RFM menunjukkan bahwa pelanggan dapat dikelompokkan menjadi tiga segmen,
yaitu High Value, Medium Value, dan Low Value. Segmen High Value merupakan pelanggan
dengan kontribusi pendapatan terbesar sehingga penting untuk dipertahankan.
""")

with st.expander("Lihat Data RFM"):
    st.dataframe(rfm)

st.divider()

# Kesimpulan
st.subheader("Kesimpulan dan Rekomendasi")

st.write("""
**Kesimpulan Pertanyaan 1:**  
Total nilai pembayaran per bulan menunjukkan pola yang fluktuatif selama periode analisis.
Beberapa kategori produk memiliki kontribusi pendapatan yang lebih besar dibandingkan
kategori lainnya.

**Kesimpulan Pertanyaan 2:**  
Segmentasi pelanggan berdasarkan RFM menghasilkan tiga kelompok pelanggan, yaitu
High Value, Medium Value, dan Low Value. Segmen High Value memberikan kontribusi
pendapatan terbesar sehingga perlu menjadi fokus utama dalam strategi retensi pelanggan.

**Rekomendasi Action Item:**  

1. Mempertahankan pelanggan High Value melalui program loyalitas, diskon eksklusif,
   atau membership.
2. Mengoptimalkan kategori produk dengan revenue tertinggi melalui promosi dan
   strategi pemasaran.
3. Melakukan re-engagement kepada pelanggan Low Value melalui voucher, email marketing,
   atau promo khusus.
""")