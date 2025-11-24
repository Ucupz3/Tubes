# Penjelasan Kode Program Analisis Sentimen Tokopedia

Dokumen ini berisi penjelasan detail mengenai setiap file dan fungsi yang ada dalam proyek ini.

## 1. Pipeline Utama ([main.py](file:///home/rodwell/Documents/E/main.py))
File ini adalah pengatur utama (orchestrator) yang menjalankan seluruh proses analisis data dari awal hingga akhir.

- **[main()](file:///home/rodwell/Documents/E/main.py#11-41)**: Fungsi utama yang memanggil langkah-langkah berikut secara berurutan:
    1.  `collect_data()`: Mengambil data ulasan.
    2.  [label_data()](file:///home/rodwell/Documents/E/src/data_labeler.py#4-28): Memberi label sentimen pada data.
    3.  [process_data()](file:///home/rodwell/Documents/E/src/preprocessor.py#23-67): Membersihkan dan memproses teks ulasan.
    4.  [extract_features()](file:///home/rodwell/Documents/E/src/feature_extractor.py#6-34): Mengubah teks menjadi angka (vektor).
    5.  [train_model()](file:///home/rodwell/Documents/E/src/naive_bayes_classifier.py#8-37): Melatih model Naive Bayes.
    6.  [evaluate_model()](file:///home/rodwell/Documents/E/src/evaluator.py#8-52): Menguji akurasi model.
    7.  [visualize_data()](file:///home/rodwell/Documents/E/src/visualizer.py#7-41): Membuat grafik visualisasi.

## 2. Pengumpulan Data ([src/data_collector.py](file:///home/rodwell/Documents/E/src/data_collector.py))
Bertugas mengambil (scraping) ulasan dari Google Play Store.

- **`collect_data()`**:
    - Menggunakan library `google_play_scraper`.
    - Mengambil 5000 ulasan terbaru dari aplikasi Tokopedia (`com.tokopedia.tkpd`).
    - Menyimpan data mentah ke [data/tokopedia_reviews_raw.csv](file:///home/rodwell/Documents/E/data/tokopedia_reviews_raw.csv).
    - Jika file sudah ada, proses ini dilewati untuk menghemat waktu.

## 3. Pelabelan Data ([src/data_labeler.py](file:///home/rodwell/Documents/E/src/data_labeler.py))
Memberikan label sentimen (positif/negatif) berdasarkan skor bintang yang diberikan pengguna.

- **[get_sentiment(score)](file:///home/rodwell/Documents/E/src/data_labeler.py#14-19)**:
    - Skor 1-3 dianggap **negative**.
    - Skor 4-5 dianggap **positive**.
- **[label_data()](file:///home/rodwell/Documents/E/src/data_labeler.py#4-28)**:
    - Membaca data mentah.
    - Menerapkan fungsi [get_sentiment](file:///home/rodwell/Documents/E/src/data_labeler.py#14-19) ke setiap ulasan.
    - Menyimpan hasilnya ke [data/tokopedia_reviews_labeled.csv](file:///home/rodwell/Documents/E/data/tokopedia_reviews_labeled.csv).

## 4. Preprocessing ([src/preprocessor.py](file:///home/rodwell/Documents/E/src/preprocessor.py))
Membersihkan teks agar siap diolah oleh mesin.

- **[preprocess_text(text)](file:///home/rodwell/Documents/E/src/preprocessor.py#7-22)**:
    - **Case Folding**: Mengubah semua huruf menjadi kecil (lowercase).
    - **Cleaning**: Menghapus karakter non-alfabet (angka, tanda baca) dan spasi berlebih.
- **[full_pipeline(text)](file:///home/rodwell/Documents/E/src/preprocessor.py#38-51)**:
    - Memanggil [preprocess_text](file:///home/rodwell/Documents/E/src/preprocessor.py#7-22).
    - **Stopword Removal**: Menghapus kata-kata umum yang tidak bermakna (seperti "dan", "yang", "di") menggunakan library `Sastrawi`.
    - **Stemming**: Mengubah kata berimbuhan menjadi kata dasar (contoh: "membeli" -> "beli") menggunakan `Sastrawi`.
- **[process_data()](file:///home/rodwell/Documents/E/src/preprocessor.py#23-67)**:
    - Menerapkan pipeline di atas ke seluruh data ulasan.
    - Menggunakan `tqdm` untuk menampilkan progress bar karena proses stemming memakan waktu lama.
    - Menyimpan hasil bersih ke [data/tokopedia_reviews_processed.csv](file:///home/rodwell/Documents/E/data/tokopedia_reviews_processed.csv).

## 5. Ekstraksi Fitur ([src/feature_extractor.py](file:///home/rodwell/Documents/E/src/feature_extractor.py))
Mengubah teks yang sudah bersih menjadi representasi angka (matriks) agar bisa dipahami model matematika.

- **[extract_features()](file:///home/rodwell/Documents/E/src/feature_extractor.py#6-34)**:
    - Menggunakan **TF-IDF (Term Frequency-Inverse Document Frequency)**.
    - `max_features=5000`: Membatasi hanya 5000 kata terpenting yang diambil.
    - Menyimpan matriks fitur ke [data/features.pkl](file:///home/rodwell/Documents/E/data/features.pkl) dan model vectorizer ke [models/vectorizer.pkl](file:///home/rodwell/Documents/E/models/vectorizer.pkl).

## 6. Pelatihan Model ([src/naive_bayes_classifier.py](file:///home/rodwell/Documents/E/src/naive_bayes_classifier.py))
Melatih model Machine Learning untuk mengenali pola sentimen.

- **[train_model()](file:///home/rodwell/Documents/E/src/naive_bayes_classifier.py#8-37)**:
    - Membagi data menjadi **Training Set (80%)** dan **Test Set (20%)**.
    - Menggunakan algoritma **Multinomial Naive Bayes**, yang sangat cocok untuk klasifikasi teks.
    - Melatih model menggunakan data training.
    - Menyimpan model yang sudah dilatih ke [models/sentiment_model.pkl](file:///home/rodwell/Documents/E/models/sentiment_model.pkl).

## 7. Evaluasi Model ([src/evaluator.py](file:///home/rodwell/Documents/E/src/evaluator.py))
Mengukur seberapa pintar model yang telah dilatih.

- **[evaluate_model()](file:///home/rodwell/Documents/E/src/evaluator.py#8-52)**:
    - Menggunakan data test (yang tidak dilihat model saat latihan) untuk memprediksi sentimen.
    - Menghitung metrik:
        - **Accuracy**: Persentase prediksi yang benar.
        - **Precision**: Ketepatan prediksi positif.
        - **Recall**: Kemampuan menemukan data positif.
        - **F1-Score**: Rata-rata harmonis dari Precision dan Recall.
    - Membuat **Confusion Matrix** (tabel perbandingan prediksi vs kenyataan) dan menyimpannya sebagai gambar.

## 8. Visualisasi ([src/visualizer.py](file:///home/rodwell/Documents/E/src/visualizer.py))
Membuat grafik untuk memudahkan pemahaman data.

- **[visualize_data()](file:///home/rodwell/Documents/E/src/visualizer.py#7-41)**:
    - **Pie Chart**: Menampilkan persentase ulasan positif vs negatif.
    - **Word Cloud**: Menampilkan kata-kata yang paling sering muncul dalam ulasan positif dan negatif.

## 9. Web Interface ([app.py](file:///home/rodwell/Documents/E/app.py), `templates/`, `static/`)
Aplikasi web untuk mencoba model secara langsung.

- **[app.py](file:///home/rodwell/Documents/E/app.py) (Backend)**:
    - Menggunakan **Flask**.
    - Memuat model dan vectorizer yang sudah dilatih.
    - **Route `/`**: Menampilkan halaman utama.
    - **Route `/predict`**: Menerima teks dari user, memprosesnya, dan mengembalikan hasil prediksi (sentimen, confidence score, probabilitas) dalam format JSON.
- **[templates/index.html](file:///home/rodwell/Documents/E/templates/index.html) (Frontend HTML)**:
    - Struktur halaman web.
    - Memiliki input text area dan tempat untuk menampilkan hasil.
- **[static/style.css](file:///home/rodwell/Documents/E/static/style.css) (Frontend CSS)**:
    - Mengatur tampilan agar modern dan responsif (warna gelap, animasi, layout).
- **[static/script.js](file:///home/rodwell/Documents/E/static/script.js) (Frontend JS)**:
    - Menangani interaksi user (klik tombol).
    - Mengirim data ke backend tanpa reload halaman (AJAX/Fetch).
    - Menampilkan hasil prediksi dan animasi loading.
