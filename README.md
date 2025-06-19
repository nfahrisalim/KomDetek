# KomDetek – Deteksi Komentar Bullying dari TikTok

**KomDetek** adalah aplikasi berbasis Streamlit untuk mendeteksi komentar bullying yang diambil **khusus dari platform TikTok**. Aplikasi ini dirancang untuk mempermudah analisis komentar secara individual maupun dalam jumlah besar melalui file CSV.

![KomDetek Logo](img/KomDetek.png)

---

## 🎯 Fitur Utama

- **Input Manual** untuk mendeteksi satu komentar TikTok.
- **Upload CSV** berisi komentar TikTok untuk deteksi batch.
- **Visualisasi Pie Chart** yang menunjukkan proporsi komentar bullying dan non-bullying.
- **Tabel Hasil Klasifikasi** yang interaktif dan mudah dibaca.

---

## 📦 Teknologi

- Python 3.10
- Streamlit
- Scikit-learn (SVM)
- IndoNLP & Sastrawi untuk preprocessing Bahasa Indonesia

---

## 🧠 Model Deteksi

Model klasifikasi teks menggunakan algoritma **Support Vector Machine (SVM)**, dilatih hanya dengan data **komentar TikTok** yang sudah melalui proses labeling dan pembersihan teks.

---

## 🖼 Tampilan Aplikasi

### 📤 Deteksi dari File CSV

![Submit CSV](img/Submit_CSV.png)

### ✍️ Deteksi Komentar Manual

![Submit Manual](img/Submit_Words.png)

---

## 📁 Struktur Folder

```bash
tiktokcyberbullying/
│
├── img/
│   ├── KomDetek.png
│   ├── Submit_CSV.png
│   └── Submit_Words.png
│
├── web.py
├── model/
│   └── svm_model.pkl
├── requirements.txt
└── .streamlit/
    └── config.toml
