<div align="center">

# 🕵️ Fake Job Detector

### A Chrome Extension + Machine Learning API that flags fraudulent job postings in real time

[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension%20MV3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/intro/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#-license)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

*A lightweight browser extension that scans job postings and warns you in one click if a listing looks like a scam — powered by a TF-IDF + Logistic Regression model with a rule-based scam-keyword safety net.*

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Demo](#-demo)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How Detection Works](#-how-detection-works)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔎 Overview

**Fake Job Detector** is a browser extension built to protect job seekers from fraudulent job postings — a growing problem across job boards and career sites. With a single click, the extension reads the job description on the page you're viewing, sends it to a local machine learning API, and tells you whether the posting looks **Real** or **Fake**, along with a confidence score.

The backend combines:
- A **rule-based keyword filter** that instantly flags common scam phrases (e.g. *"pay registration fee"*, *"no interview"*, *"urgent hiring"*)
- A **TF-IDF + Logistic Regression** classifier trained on a balanced, real-world dataset of genuine and fraudulent job postings

This hybrid approach keeps detection fast, explainable, and resistant to obvious scam patterns, while still leveraging ML for the more nuanced cases.

---

## 🎥 Demo

<div align="center">

*Add a screenshot or GIF of the extension popup in action here!*

```
📷 assets/demo.gif
📷 assets/popup-screenshot.png
```

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖱️ **One-Click Check** | Analyze the current job posting straight from the browser toolbar |
| 🤖 **ML-Powered Classification** | TF-IDF vectorization + Logistic Regression trained on labeled job data |
| 🚩 **Instant Scam Keyword Detection** | Rule-based filter catches obvious red flags before the model even runs |
| 📊 **Confidence Score** | Every prediction returns a confidence percentage, not just a label |
| ⚖️ **Balanced Training Data** | Dataset is downsampled to avoid bias toward the majority (real) class |
| 🔌 **Simple REST API** | Clean Flask `/predict` endpoint — easy to reuse outside the extension |
| 🪶 **Lightweight Popup UI** | Minimal, distraction-free interface — just a button and a result |

---

## 🏗 System Architecture

```
┌───────────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
│   Job Posting Page     │        │   Chrome Extension    │        │   Flask ML Backend    │
│  (LinkedIn / Indeed /  │───────▶│  content.js scrapes   │───────▶│   /predict endpoint    │
│   Naukri / any site)   │        │  job description text │        │   (localhost:5000)     │
└───────────────────────┘        └──────────┬────────────┘        └──────────┬────────────┘
                                             │                                │
                                    popup.js sends text             Rule-based keyword check
                                    via fetch() POST                          │
                                             │                       TF-IDF + Logistic
                                             ▼                        Regression model
                                   ┌──────────────────┐                      │
                                   │   popup.html UI   │◀─────────────────────┘
                                   │  shows Result +    │   JSON: { result, confidence }
                                   │  Confidence Score   │
                                   └──────────────────┘
```

**Request Flow:**
1. User opens a job posting and clicks the extension icon.
2. Clicking **"Check Job"** triggers `popup.js`, which asks the content script to extract the job description from the page.
3. The description is sent via `fetch()` as a `POST` request to the Flask backend's `/predict` route.
4. The backend first checks for obvious scam keywords; if found, it immediately returns `Fake` with high confidence.
5. Otherwise, the text is vectorized with TF-IDF and classified by the trained Logistic Regression model.
6. The result (`Real` / `Fake`) and confidence score are sent back and displayed in the popup.

---

## 🧰 Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Extension** | HTML, CSS, JavaScript (Manifest V3) |
| **Backend API** | Python, Flask, Flask-CORS |
| **ML / Data** | pandas, scikit-learn (TF-IDF Vectorizer, Logistic Regression) |
| **Dataset** | `fake_job_postings.csv` (job descriptions labeled real/fraudulent) |

</div>

---

## 📁 Project Structure

```
Fake_Job_detection_Extension/
├── app.py                    # Flask backend — trains the model & serves the /predict API
├── manifest.json             # Chrome extension configuration (Manifest V3)
├── popup.html                # Extension popup UI
├── popup.js                  # Popup logic — triggers check, calls the API, renders result
├── content.js                # Content script — extracts job description from the page
├── style.css                 # Popup styling
└── fake_job_postings.csv     # Training dataset (not committed — see Setup)
```

---

## 🧠 How Detection Works

### 1. Rule-Based Pre-Filter
Before any ML inference happens, the backend scans the job description for common scam phrases:

```
"earn money", "no experience", "work from home", "pay fee",
"registration fee", "quick money", "daily income",
"no interview", "urgent hiring"
```

If any of these appear, the posting is immediately flagged **Fake** with **95% confidence** — no need to run the model for obvious cases.

### 2. Machine Learning Classification
For everything else, the description is:
1. Transformed using a **TF-IDF Vectorizer** (`max_features=10000`, unigrams + bigrams, English stop words removed)
2. Classified by a **Logistic Regression** model (`class_weight="balanced"`, `max_iter=2000`)
3. Trained on a dataset that's been **downsampled** so real and fake postings are equally represented — preventing the model from just learning to always predict "Real"

The API returns a JSON response like:

```json
{
  "result": "Fake",
  "confidence": 87.42
}
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Chrome (or any Chromium-based browser)
- The training dataset `fake_job_postings.csv` placed in the project root

### 1. Clone the Repository
```bash
git clone https://github.com/ChathurthiBR/Fake_Job_detection_Extension.git
cd Fake_Job_detection_Extension
```

### 2. Set Up the Backend
```bash
# Install dependencies
pip install flask flask-cors pandas scikit-learn

# Run the Flask server (trains the model on startup)
python app.py
```
The server starts at `http://127.0.0.1:5000` — you should see `✅ Model trained successfully!` in the console.

### 3. Load the Extension in Chrome
1. Open `chrome://extensions/`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the `Fake_Job_detection_Extension` folder
5. The **Fake Job Detector** icon will appear in your toolbar

### 4. Use It
1. Navigate to any job posting page
2. Click the extension icon
3. Click **"Check Job"**
4. View the result — `Real` ✅ or `Fake` 🚩 — with a confidence score

> ⚠️ The backend must be running locally (`python app.py`) for the extension to work, since the extension calls `http://127.0.0.1:5000/predict`.

---

## 📡 API Reference

### `POST /predict`

Analyzes a job description and returns a classification.

**Request Body:**
```json
{
  "description": "Full text of the job posting..."
}
```

**Response:**
```json
{
  "result": "Real",
  "confidence": 92.15
}
```

**Error Response:**
```json
{
  "error": "No description provided"
}
```

### `GET /`
Health check — returns `"Backend is running!"`

---

## 🖼 Screenshots

```
📷 assets/popup-real-result.png    — Example of a "Real" classification
📷 assets/popup-fake-result.png    — Example of a "Fake" classification
```

---

## 🔮 Roadmap

- [ ] Auto-extract job descriptions from popular job boards (LinkedIn, Indeed, Naukri) without manual copy-paste
- [ ] Deploy the Flask backend to the cloud so the extension works without running a local server
- [ ] Expand the scam-keyword list and support multiple languages
- [ ] Add a browsing history of previously checked postings
- [ ] Improve the model with more recent, larger labeled datasets
- [ ] Add explainability — highlight which words/phrases influenced the prediction
- [ ] Package and publish to the Chrome Web Store

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the detection model, add job-board integrations, or polish the UI:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

This project is open-sourced for educational purposes. Feel free to fork, modify, and build upon it.

```
MIT License — free to use, modify, and distribute with attribution.
```

<div align="center">

### ⭐ If this project helped you spot a scam, consider giving it a star!

Made with 🛡️ and 💙 by **Chathurthi B R**

</div>
