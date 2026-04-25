import streamlit as st
import time
from spam_classifier import predict_email

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Intelligent Email Security Analyzer",
    page_icon="🛡️",
    layout="centered"
)

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #4CAF50;
}
.result-box {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    animation: fadeIn 1s ease-in-out;
}
.safe {
    background-color: #d4edda;
    color: #155724;
}
.spam {
    background-color: #fff3cd;
    color: #856404;
}
.phishing {
    background-color: #f8d7da;
    color: #721c24;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Sidebar
# ==============================
st.sidebar.title("📊 Model Info")
st.sidebar.write("Model: Naive Bayes (Hybrid AI)")
st.sidebar.write("Classes: Safe / Spam / Phishing")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.subheader("📜 Scan History")

# ==============================
# Title
# ==============================
st.markdown('<div class="title">🛡️ Intelligent Email Security Analyzer</div>', unsafe_allow_html=True)
st.write("")

# ==============================
# Input
# ==============================
email_text = st.text_area("📩 Paste your email content here:", height=200)

# ==============================
# Highlight function
# ==============================
def highlight_text(text, keywords):
    for word in keywords:
        text = text.replace(word, f"**:red[{word}]**")
    return text

# ==============================
# Button Action
# ==============================
if st.button("🔍 Analyze Email"):

    if email_text.strip() == "":
        st.warning("Please enter email content!")
    
    else:
        with st.spinner("Analyzing email..."):
            time.sleep(1.5)

        # Get result
        result = predict_email(email_text)

        label = result["label"]               # 0 / 1 / 2
        label_name = result["label_name"]     # Safe / Spam / Phishing
        prob = result["probability"]
        urls = result["urls"]
        keywords = result["keywords"]
        reasons = result["reasons"]
        risk_score = result["risk_score"]

        # Save history
        st.session_state.history.append({
            "text": email_text[:40] + "...",
            "result": label_name,
            "confidence": f"{prob*100:.2f}%"
        })

        # ==============================
        # Result Display
        # ==============================
        if label == 2:
            st.markdown(
                f'<div class="result-box phishing">⚠️ Phishing Detected ({prob*100:.2f}%)</div>',
                unsafe_allow_html=True
            )
        elif label == 1:
            st.markdown(
                f'<div class="result-box spam">📬 Spam Detected ({prob*100:.2f}%)</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-box safe">✅ Safe Email ({prob*100:.2f}%)</div>',
                unsafe_allow_html=True
            )

        # Confidence bar
        st.progress(float(prob))
        st.caption(f"Confidence Score: {prob*100:.2f}%")

        # Show classification clearly
        st.write(f"**Classification:** {label_name}")
        st.write(f"**Risk Score:** {risk_score}")

        st.write("")

        # ==============================
        # Explanation
        # ==============================
        if reasons:
            st.subheader("🧠 Why this result?")
            for r in reasons:
                st.write(f"• {r}")

        # ==============================
        # URL Section
        # ==============================
        if urls:
            st.subheader("🔗 Detected URLs")
            for u in urls:
                st.error(f"⚠️ {u}")

        # ==============================
        # Keywords
        # ==============================
        if keywords:
            st.subheader("⚠️ Suspicious Keywords")
            st.write(", ".join(keywords))

        # ==============================
        # Highlighted Content
        # ==============================
        if keywords:
            st.subheader("📌 Highlighted Email Content")
            highlighted = highlight_text(email_text.lower(), keywords)
            st.markdown(highlighted)

# ==============================
# Show History
# ==============================
for item in reversed(st.session_state.history[-5:]):
    st.sidebar.write(f"{item['result']} ({item['confidence']})")