from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.utils import resample

app = Flask(__name__)
CORS(app)

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("fake_job_postings.csv")
df = df.dropna(subset=["description", "fraudulent"])

# =========================
# BALANCE DATASET
# =========================
df_real = df[df.fraudulent == 0]
df_fake = df[df.fraudulent == 1]

df_real_downsampled = resample(
    df_real,
    replace=False,
    n_samples=len(df_fake),
    random_state=42
)

df_balanced = pd.concat([df_real_downsampled, df_fake])

X = df_balanced["description"]
y = df_balanced["fraudulent"]

# =========================
# VECTORIZER
# =========================
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000,
    ngram_range=(1, 2)
)

X_vec = vectorizer.fit_transform(X)

# =========================
# MODEL
# =========================
model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

model.fit(X_vec, y)

print("✅ Model trained successfully!")

# =========================
# HOME ROUTE
# =========================
@app.route("/")
def home():
    return "Backend is running!"

# =========================
# PREDICTION API (FINAL FIX)
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        text = data.get("description", "")

        if text.strip() == "":
            return jsonify({"error": "No description provided"})

        # =========================
        # RULE-BASED DETECTION (IMPORTANT)
        # =========================
        scam_keywords = [
            "earn money", "no experience", "work from home",
            "pay fee", "registration fee", "quick money",
            "daily income", "no interview", "urgent hiring"
        ]

        text_lower = text.lower()

        if any(keyword in text_lower for keyword in scam_keywords):
            return jsonify({
                "result": "Fake",
                "confidence": 95.0
            })

        # =========================
        # ML PREDICTION
        # =========================
        text_vec = vectorizer.transform([text])

        prediction = model.predict(text_vec)[0]
        confidence = model.predict_proba(text_vec)[0].max() * 100

        result = "Fake" if prediction == 1 else "Real"

        return jsonify({
            "result": result,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)