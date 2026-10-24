# Proyek Analisis Data E-Commerce

## Deskripsi Proyek

Proyek ini merupakan submission analisis data menggunakan dataset e-commerce (Olist). Analisis dilakukan untuk memahami tren pendapatan, kategori produk dengan kontribusi pendapatan tertinggi, serta segmentasi pelanggan berdasarkan RFM.

Dashboard interaktif dibuat menggunakan Streamlit untuk membantu menampilkan hasil analisis secara lebih mudah dan informatif.

## Pertanyaan Bisnis

1. Bagaimana tren total nilai pembayaran per bulan selama periode 2016–2018, serta kategori produk apa yang memberikan kontribusi pendapatan tertinggi?
2. Bagaimana segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary (RFM) selama periode 2016–2018, serta bagaimana kontribusi masing-masing segmen terhadap total pendapatan?

## Struktur Folder

submission
├── dashboard
│   ├── main_data.csv
│   └── dashboard.py
├── data
│   ├── orders_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   └── products_dataset.csv
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Cara Menjalankan Dashboard

### Setup Environment - Anaconda

1. Buka terminal.

2. Masuk ke folder utama submission.

```bash
cd submission
```

3. Buat environment Anaconda dengan Python 3.9.

```bash
conda create —name main-ds python=3.9
```

4. Aktifkan environment tersebut.

```bash
conda activate main-ds
```

5. Instal semua dependensi (library) yang dibutuhkan dari file `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal (Tanpa Anaconda)

Jika kamu tidak ingin menggunakan Anaconda, kamu dapat menggunakan virtual environment bawaan terminal:

1. Buka terminal.

2. Masuk ke folder utama submission.

```bash
cd submission
```

3. Buat dan aktifkan virtual environment.

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
```

4. Instal semua dependensi (library) yang dibutuhkan dari file `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Run Streamlit App

Setelah environment siap dan semua library terinstal, jalankan dashboard dengan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Atau menggunakan Python module:

```bash
python3 -m streamlit run dashboard/dashboard.py
```

Tunggu hingga dashboard muncul di browser (biasanya di `http://localhost:8501`).

## Catatan Tambahan

### requirements.txt

Pada file `requirements.txt`, setiap library ditentukan dengan versi spesifik untuk menghindari konflik versi (*dependency conflict*):

```txt
streamlit==1.57.0
pandas==3.0.2
matplotlib==3.10.9
seaborn==0.13.2
```

### url.txt

File `url.txt` berisi link Streamlit Cloud (jika sudah di-deploy). Untuk meng-deploy dashboard ke Streamlit Cloud:

1. Push project kamu termasuk dashboard, dataset, serta `requirements.txt` ke repository GitHub.
2. Masuk ke [share.streamlit.io](https://share.streamlit.io/), kemudian hubungkan dengan repository tersebut.
3. Lalu deploy dengan memilih file utama python dashboard (contohnya: `dashboard.py`).
4. Tunggu hingga aplikasi Successfully dibangun dan dapat dibuka tanpa autentikasi tambahan.
5. Setelah successfully, salin URL publik yang diberikan Streamlit Cloud (link berformat `https://<nama-app>.streamlit.app`) dan cantumkan kedalam file `url.txt`.
6. Pastikan dashboard yang telah di-deploy Successfully menampilkan hasil yang konsisten, dimana visualisasi yang ditampilkan yang sama dengan yang berjalan di lokal.

## Deskripsi Analisis

Analisis dilakukan pada dataset e-commerce (Olist) melalui notebook `Proyek_Analisis_Data.ipynb`. Dataset terdiri dari 5 file utama:

- `orders_dataset.csv` — Informasi pesanan (status, timestamp pengiriman, dll.)
- `order_items_dataset.csv` — Detail item pesanan per produk
- `order_payments_dataset.csv` — Nilai pembayaran per pesanan
- `customers_dataset.csv` — Data pelanggan
- `products_dataset.csv` — Kategori dan deskripsi produk

Metode analisis mencakup:
- **Data Wrangling**: Membersihkan data (konversi datetime, hapus duplikat & missing value)
- **EDA (Exploratory Data Analysis)**: Menjelajahi tren pendapatan bulanan, kontribusi kategori produk, dan segmentasi pelanggan berdasarkan RFM
- **Visualisasi**: Menggunakan matplotlib & seaborn untuk memvisualisasikan insight

## Hasil Analisis

1. **Tren Pendapatan Bulanan (2016–2018)**: Total nilai pembayaran menunjukkan pola fluktuatif dari waktu ke waktu, dengan periode tertentu mengalami peningkatan signifikan.
2. **Kategori Produk dengan Pendapatan Tertinggi**: Beberapa kategori produk memberikan kontribusi revenue yang lebih besar dibandingkan kategori lainnya, menjadi fokus strategi pemasaran dan pengelolaan stok.
3. **Segmentasi Pelanggan RFM**: Pelanggan dapat dikelompokkan menjadi tiga segmen — High Value, Medium Value, dan Low Value. Segmen High Value memberikan kontribusi pendapatan terbesar sehingga perlu dipertahankan melalui program loyalitas.

## Kesimpulan dan Rekomendasi

1. Mempertahankan pelanggan High Value melalui program loyalitas, diskon eksklusif, atau membership.
2. Mengoptimalkan kategori produk dengan revenue tertinggi melalui promosi dan strategi pemasaran.
3. Melakukan re-engagement kepada pelanggan Low Value melalui voucher, email marketing, atau promo khusus.# submission
