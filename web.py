import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import joblib
import pandas as pd
import re
import matplotlib.pyplot as plt
from indoNLP.preprocessing import replace_slang, emoji_to_words
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from pathlib import Path

st.set_page_config(page_title="Bullying Comment Detector", layout="wide")

# Load models and vectorizer
svm = joblib.load('models/svm_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

# Global styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; }
    .header-box {
        background-color: #FFF3CD;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #856404;
    }
    table {
        margin: auto;
        width: 70%;
        text-align: center;
        border-collapse: collapse;
    }
    th, td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    th {
        background-color: #E4A800;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Preprocessing functions
def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(.)\1+', r'\1', text)
    return text

def stopword(str_text):
    stop_words = StopWordRemoverFactory().get_stop_words()
    new_array = ArrayDictionary(stop_words)
    stop_words_remover_new = StopWordRemover(new_array)
    return stop_words_remover_new.remove(str_text)

def tokenize_text(text):
    return text.split()

def stemming(text_cleaning):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return ' '.join([stemmer.stem(word) for word in text_cleaning])

def predict_hate_speech(text, model):
    try:
        if pd.isna(text) or not isinstance(text, str) or text.strip() == '':
            return "Tidak Valid (Kosong)"

        text = emoji_to_words(text, lang='id', use_alias=False, delimiter=(' ', ' '))
        text = clean_text(text)
        text = text.lower()
        text = replace_slang(text)
        text = stopword(text)
        text = tokenize_text(text)
        text = stemming(text)

        word_count = len(text.split())
        if word_count == 0:
            return "Tidak Valid (Kosong)"
        elif word_count > 25:
            return "Tidak Valid (>25 kata)"

        text_transformed = vectorizer.transform([text])
        prediction = model.predict(text_transformed)
        return 'Bullying' if prediction == 1 else 'Non-Bullying'
    except Exception as e:
        return f"Error"
def main():
    menu_selection = option_menu(
        menu_title=None,
        options=["Home", "Bullying Detection"],
        icons=["house-fill", "exclamation-triangle"],
        default_index=0,
        orientation="horizontal",
    )

    if menu_selection == "Home":
        logo = Image.open(Path("img") / "KomDetek.png")
        st.image(logo, use_container_width=True)

        st.markdown("<h1 style='text-align:center; color:#E4A800;'>Machine Learning - Kelompok 6B</h1>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Nama Anggota</th><th>NIM</th></tr>
            <tr><td>Muh. Naufal Fahri Salim</td><td>H071231031</td></tr>
            <tr><td>Muh. Aipun Pratama</td><td>H071231045</td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: center"><h2>\U0001F3AF Deteksi Komentar Bullying di Media Sosial</h2></div>', unsafe_allow_html=True)
        st.write("Aplikasi ini digunakan untuk mendeteksi komentar TikTok apakah mengandung unsur bullying atau tidak.")

        st.markdown("#### \U0001F4D6 Tutorial Penggunaan Aplikasi")
        st.markdown("""
        1. **Input Komentar**: Masukkan satu komentar pada tab *Input Komentar* untuk deteksi cepat.
        2. **Upload CSV**: Unggah file `.csv` yang berisi kolom `Text` pada tab *Upload CSV* untuk prediksi massal.
        3. **Hasil**: Komentar yang valid akan diklasifikasikan sebagai *Bullying* atau *Non-Bullying*.
        4. **Unduh Hasil**: Klik tombol **\U0001F4BE Download Hasil** untuk menyimpan file prediksi.
        """)

        st.markdown("#### \U0001F4CA Dataset Overview")
        df = pd.read_csv(r'tiktokscraped.csv')
        search = st.text_input("\U0001F50D Cari komentar")
        if search:
            st.dataframe(df[df['Text'].str.contains(search, case=False)], use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

    elif menu_selection == "Bullying Detection":
        tab1, tab2 = st.tabs(["Input Komentar 📝", "Upload CSV 📂"])

        with tab1:
            st.markdown('<div class="header-box">Masukkan komentar untuk dideteksi</div><br>', unsafe_allow_html=True)
            with st.form(key='form_komentar'):
                user_input = st.text_area("Komentar", height=150)
                submit = st.form_submit_button("Deteksi")
                if submit:
                    result = predict_hate_speech(user_input, svm)
                    if result == "Bullying":
                        st.markdown("""
                            <div style="
                                padding:15px;
                                background-color:#FFD2D2;
                                border-radius:10px;
                                text-align:center;
                                font-weight:bold;
                                color:#721c24;">
                                🚨 Komentar terdeteksi sebagai <u>Bullying</u>
                            </div>
                        """, unsafe_allow_html=True)
                    elif result == "Non-Bullying":
                        st.markdown("""
                            <div style="
                                padding:15px;
                                background-color:#D4EDDA;
                                border-radius:10px;
                                text-align:center;
                                font-weight:bold;
                                color:#155724;">
                                ✅ Komentar ini termasuk <u>Non-Bullying</u>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("Komentar tidak valid atau terlalu panjang (> 25 kata).")

        with tab2:
            st.markdown('<div class="header-box">Unggah file CSV dengan komentar</div><br>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Unggah file CSV", type="csv")

            if uploaded_file:
                try:
                    df_upload = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                    if 'Text' in df_upload.columns:
                        df_upload = df_upload[df_upload['Text'].notna()]
                        df_upload['Text'] = df_upload['Text'].astype(str)
                        df_upload['Prediction'] = df_upload['Text'].apply(lambda x: predict_hate_speech(x, svm))

                        valid_df = df_upload[df_upload['Prediction'].isin(['Bullying', 'Non-Bullying'])]

                        col1, col2 = st.columns([0.55, 0.45])
                        with col1:
                            st.dataframe(df_upload, use_container_width=True, height=600)
                            csv = df_upload.to_csv(index=False).encode('utf-8')
                            st.download_button("💾 Download Hasil", csv, "hasil_prediksi.csv", mime='text/csv')

                        with col2:
                            if not valid_df.empty:
                                counts = valid_df['Prediction'].value_counts()
                                labels = [f"{label} ({count})" for label, count in counts.items()]
                                colors = ['#379C5E', '#E4A800']
                                explode = [0.03] * len(counts)

                                plt.figure(figsize=(5,5))
                                plt.pie(counts, labels=labels, colors=colors[:len(counts)],
                                        autopct='%1.1f%%', startangle=140, explode=explode,
                                        wedgeprops={'edgecolor': 'black'})
                                plt.title("Distribusi Prediksi", fontsize=11)
                                st.pyplot(plt)
                            else:
                                st.info("Tidak ada prediksi valid untuk ditampilkan di grafik.")
                    else:
                        st.error("File CSV harus memiliki kolom 'Text'.")
                except Exception as e:
                    st.error(f"Gagal memproses file: {str(e)}")

if __name__ == "__main__":
    main()
