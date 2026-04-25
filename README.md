# 🛡️ AI Email Security Analyzer

An intelligent email classification system that detects and categorizes emails into **Safe**, **Spam**, and **Phishing** using a hybrid approach combining Machine Learning and rule-based risk analysis.

---

## 🚀 Features

- 🔍 3-Class Classification: Safe / Spam / Phishing  
- 🧠 Hybrid AI System (ML + Rule-based Detection)  
- 🔗 URL Extraction & Domain Trust Analysis  
- ⚠️ Suspicious Keyword Detection  
- 📊 Risk Scoring System  
- 🧾 Explainable AI (Reason-based output)  
- 🎨 Interactive Streamlit UI  
- 📜 Scan History Tracking  

---

## 🧠 How It Works

1. **Text Processing** using TF-IDF Vectorization  
2. **Machine Learning Model** (Naive Bayes) predicts base classification  
3. **Risk Scoring System** analyzes:
   - URLs  
   - Keywords  
   - Sensitive requests  
4. **Domain Trust Logic** reduces false positives  
5. Final classification into:
   - 🟢 Safe  
   - 🟡 Spam  
   - 🔴 Phishing  

---

## 🛠️ Tech Stack

- Python  
- Scikit-learn  
- Streamlit  
- NLP (TF-IDF)  
- Naive Bayes  

---

## 📁 Project Structure


ai-email-security-analyzer/
│
├── app.py
├── spam_classifier.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
└── README.md


---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
