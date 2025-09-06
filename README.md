

# 🛡️ KomDetek – TikTok Comment Bullying Detection

![KomDetek Logo](img/KomDetek.png)

**KomDetek** is a Streamlit application for detecting bullying comments on TikTok, both individually and in bulk via CSV upload.

---

## 🔥 Main Features

- Detect TikTok comments instantly (manual input)
- Bulk detection via CSV upload
- Visualize prediction results with a pie chart
- Interactive classification table

---

## 🚀 Installation & Usage

1. **Clone this repository**
2. **(Optional but recommended) Create a virtual environment:**

    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3. **Install all dependencies:**

    ```powershell
    pip install -r requirements.txt
    ```

4. **Run the app:**

    ```powershell
    streamlit run web.py
    ```

---

## 📤 CSV Upload Format

Your CSV file must have at least a `Text` column. Example:

```csv
Text,Description
First comment,This is from user A
Second comment,From user B
Third comment,Random comment
```

You may add extra columns (e.g. `Description`), but only the `Text` column will be processed for bullying detection.

---

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- Scikit-learn (SVM, Logistic Regression, Naive Bayes)
- Keras (LSTM)
- IndoNLP & Sastrawi (Indonesian text preprocessing)

---

## 🧠 Models Used

All models are trained on real TikTok comment data:

- `svm_model.pkl`
- `logistic_regression_model.pkl`
- `naive_bayes_model.pkl`
- `lstm_model.h5`
- `vectorizer.pkl` (TF-IDF)

---

## 📓 Training & Preprocessing Notebook

See the full training and preprocessing workflow in Google Colab:
[Open Training Notebook](https://colab.research.google.com/drive/1QQB4o4Eqn4RObcmGNNvLlhokYGYVf7TS?usp=sharing)

---

## 🖼️ App Screenshots

### Upload CSV

![Submit CSV](img/Submit_Csv.png)

### Manual Input

![Submit Manual](img/Submit_Words.png)

---

## 📁 Project Structure

```bash
.
├── README.md
├── requirements.txt
├── tiktokscraped.csv
├── web.py                  # Main Streamlit app
│
├── img/
│   ├── KomDetek.png
│   ├── Submit_Csv.png
│   └── Submit_Words.png
│
└── models/
     ├── svm_model.pkl
     ├── logistic_regression_model.pkl
     ├── naive_bayes_model.pkl
     ├── lstm_model.h5
     └── vectorizer.pkl
```

---

## 👤 Contact & Contributor

- Made by [Naufal Fahri](https://nfahrisalim.com)

---
