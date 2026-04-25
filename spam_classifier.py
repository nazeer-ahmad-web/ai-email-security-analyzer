import pickle
import re
from urllib.parse import urlparse

# ==============================
# Load Model & Vectorizer
# ==============================
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ==============================
# Extract URLs
# ==============================
def extract_urls(text):
    url_pattern = r'(https?://\S+|www\.\S+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    return re.findall(url_pattern, text)

# ==============================
# Get domain
# ==============================
def get_domain(url):
    if not url.startswith("http"):
        url = "http://" + url
    return urlparse(url).netloc.lower()

# ==============================
# Trusted Domain Check
# ==============================
def is_trusted_domain(url):
    domain = get_domain(url)

    trusted_domains = [
        "nptel.ac.in", "iitm.ac.in",
        "google.com", "docs.google.com",
        "amazon.in", "microsoft.com"
    ]

    trusted_suffix = [".ac.in", ".edu", ".gov"]

    return any(domain.endswith(td) for td in trusted_domains) or \
           any(domain.endswith(s) for s in trusted_suffix)

def all_urls_trusted(urls):
    return urls and all(is_trusted_domain(u) for u in urls)

# ==============================
# Keywords
# ==============================
def get_keywords(text):
    words = [
        "urgent","verify","login","password","bank","account",
        "click","offer","free","winner","otp","limited",
        "job","salary","hiring","interview"
    ]
    text = text.lower()
    return [w for w in words if w in text]

# ==============================
# Newsletter detection
# ==============================
def is_newsletter(text):
    newsletter_words = [
        "newsletter", "release", "update", "community",
        "event", "changelog", "blog"
    ]
    text = text.lower()
    return any(w in text for w in newsletter_words)

# ==============================
# MAIN FUNCTION
# ==============================
def predict_email(text):
    text_lower = text.lower()

    # ML prediction
    vector = vectorizer.transform([text])
    ml_pred = model.predict(vector)[0]   # 0 or 1
    prob = model.predict_proba(vector)[0][ml_pred]

    urls = extract_urls(text)
    keywords = get_keywords(text)

    reasons = []
    risk_score = 0

    # ==============================
    # Risk scoring
    # ==============================
    if urls:
        risk_score += 2
        reasons.append("Contains URL")

    if keywords:
        risk_score += len(keywords)
        reasons.append(f"Keywords: {', '.join(keywords)}")

    if "otp" in text_lower and urls:
        risk_score += 4
        reasons.append("OTP with link")

    if any(w in text_lower for w in ["account","bank","login","password"]) and urls:
        risk_score += 3
        reasons.append("Sensitive request with link")

    if any(w in text_lower for w in ["job","salary"]) and urls:
        risk_score += 2
        reasons.append("Job scam pattern")

    # ==============================
    # Trust logic
    # ==============================
    trusted = all_urls_trusted(urls)
    if trusted:
        risk_score -= 5
        reasons.append("Trusted domain")

    # ==============================
    # FINAL CLASSIFICATION
    # ==============================

    # 🎣 PHISHING
    if risk_score >= 6:
        label = 2
        label_name = "Phishing"

    # 📬 SPAM (newsletter / promo)
    elif ml_pred == 1 or is_newsletter(text):
        label = 1
        label_name = "Spam"

    # ✅ SAFE
    else:
        label = 0
        label_name = "Safe"

    return {
        "label": label,
        "label_name": label_name,
        "probability": prob,
        "risk_score": risk_score,
        "urls": urls,
        "keywords": keywords,
        "reasons": reasons
    }