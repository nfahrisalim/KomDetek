import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import joblib
import pandas as pd
import re
import matplotlib.pyplot as plt
from keras.models import load_model
from indoNLP.preprocessing import replace_slang, emoji_to_words
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from scipy.special import expit

st.set_page_config(page_title="Bullying Comment Detector", layout="wide")

# Load models and vectorizer
svm = joblib.load('models/svm_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

# Global styling
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; }
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
    text = emoji_to_words(text, lang='id', use_alias=False, delimiter=(' ', ' '))
    text = clean_text(text)
    text = text.lower()
    text = replace_slang(text)
    text = stopword(text)
    text = tokenize_text(text)
    text = stemming(text)

    word_count = len(text.split())
    if word_count == 0 or word_count > 25:
        return None

    text_transformed = vectorizer.transform([text])
    prediction = model.predict(text_transformed)
    return 'Bullying' if prediction == 1 else 'Non-Bullying'

def main():
    menu_selection = option_menu(
        menu_title=None,
        options=["Home", "Bullying Detection"],
        icons=["house-fill", "exclamation-triangle"],
        default_index=0,
        orientation="horizontal",
    )

    if menu_selection == "Home":
        st.markdown("<h1 style='text-align:center; color:#E4A800;'>Machine Learning - Kelompok 6B</h1>", unsafe_allow_html=True)
        st.markdown("""
        <table>
            <tr><th>Nama Anggota</th><th>NIM</th></tr>
            <tr><td>Muh. Naufal Fahri Salim</td><td>H071231031</td></tr>
            <tr><td>Muh. Aipun Pratama</td><td>H071231045</td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div style="text-align: center"><h2>🎯 Deteksi Komentar Bullying di Media Sosial</h2></div>', unsafe_allow_html=True)

        st.write("""
        Aplikasi ini bertujuan untuk mendeteksi komentar TikTok apakah mengandung unsur **bullying** atau tidak. Model dilatih menggunakan data komentar dari scraping video TikTok yang telah dilabeli secara manual.
        """)

        st.markdown("#### 📊 Dataset Overview")
        df = pd.read_csv(r'D:\Data Science\tiktok scrape\tiktokscraped.csv')
        search = st.text_input("🔍 Cari komentar")
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
                        st.markdown('<div style="padding:15px;background-color:#FFD2D2;border-radius:10px;text-align:center;font-weight:bold;">🚨 Komentar terdeteksi sebagai <u>Bullying</u></div>', unsafe_allow_html=True)
                    elif result == "Non-Bullying":
                        st.markdown('<div style="padding:15px;background-color:#D4EDDA;border-radius:10px;text-align:center;font-weight:bold;">✅ Komentar ini termasuk <u>Non-Bullying</u></div>', unsafe_allow_html=True)
                    else:
                        st.warning("Komentar tidak valid atau terlalu panjang (> 25 kata).")

        with tab2:
            st.markdown('<div class="header-box">Unggah file CSV dengan komentar</div><br>', unsafe_allow_html=True)
            with st.form(key='upload_csv_form'):
                uploaded_file = st.file_uploader("Unggah file CSV", type="csv")
                upload_button = st.form_submit_button("Proses")
                if upload_button and uploaded_file:
                    try:
                        df_upload = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                        if 'Text' in df_upload.columns:
                            df_upload['Prediction'] = df_upload['Text'].apply(lambda x: predict_hate_speech(x, svm))
                            df_upload = df_upload.dropna()

                            col1, col2 = st.columns([0.55, 0.45])
                            with col1:
                                st.dataframe(df_upload, use_container_width=True, height=600)
                                csv = df_upload.to_csv(index=False).encode('utf-8')
                                st.download_button("💾 Download Hasil", csv, "hasil_prediksi.csv", mime='text/csv')

                            with col2:
                                counts = df_upload['Prediction'].value_counts()
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
                            st.error("File CSV harus memiliki kolom 'Text'.")
                    except Exception as e:
                        st.error(f"Gagal memproses file: {str(e)}")

if __name__ == "__main__":
    main()
