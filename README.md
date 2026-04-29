<div align="center">

<img src="https://img.shields.io/badge/PhishTrace_AI-v1.0-critical?style=for-the-badge&logo=shield&logoColor=white" />

# 🛡️ PhishTrace AI
### Hybrid Client-Side Phishing Detection Framework

*Bridging the gap between human vulnerability and real-time cyber threat intelligence.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-REST_API-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Chrome](https://img.shields.io/badge/Chrome-Manifest_V3-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Status](https://img.shields.io/badge/Status-Capstone_Project-blueviolet?style=flat-square)](https://github.com/K921-cyber/Phishing_project)
[![Accuracy](https://img.shields.io/badge/Model_Accuracy-94%25-success?style=flat-square)](#-performance-results)

<br/>

[**Features**](#-key-features) · [**Architecture**](#-system-architecture) · [**Installation**](#%EF%B8%8F-installation--setup) · [**Performance**](#-performance-results) · [**Structure**](#-project-structure)

---

</div>

## 🎯 What is PhishTrace AI?

**PhishTrace AI** is a specialized cybersecurity framework engineered to address the most exploited attack surface in modern security — the **Human Layer**. Phishing attacks succeed not because firewalls fail, but because humans are tricked. PhishTrace AI places the defense at the point of deception: directly inside the browser.

Unlike traditional server-side reputation filters that suffer from **blacklist latency**, PhishTrace AI uses a **hybrid dual-engine approach** — combining Machine Learning with Digital Forensics — to detect threats *in real-time*, before they can cause damage.

```
 [Suspicious Email] ──► [Chrome Extension] ──► [Local Flask Server]
                                                       │
                                          ┌────────────┴────────────┐
                                          │                         │
                                   [ML Engine]              [Forensic Engine]
                              Random Forest Classifier     WHOIS · DNS · OSINT
                              Behavioral NLP Analysis      Zero-Day Domain Check
                                          │                         │
                                          └────────────┬────────────┘
                                                       │
                                             [🚦 Traffic Light Verdict]
                                             🔴 Phishing  🟡 Suspicious  🟢 Safe
```

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🤖 Dual-Engine Detection
Combines a **Random Forest Classifier** for semantic/behavioral analysis with a **Digital Forensic Module** for deep technical verification. Two independent signals, one unified verdict.

</td>
<td width="50%">

### ⚡ Real-Time Zero-Day Defense
Automatically flags domains registered **< 30 days ago** as high-risk — catching brand-new phishing infrastructure *before* it appears on any global blocklist.

</td>
</tr>
<tr>
<td width="50%">

### 🧠 Behavioral NLP Analysis
Detects psychological manipulation tactics embedded in email text — **urgency** ("Act Now!"), **fear** ("Your account will be suspended"), and **coercion** — using trained NLP models.

</td>
<td width="50%">

### 🔒 Privacy-First, Client-Side
Operates via a local Flask server on `127.0.0.1`. Your emails and URLs **never leave your machine**. Zero telemetry. Zero data leakage.

</td>
</tr>
<tr>
<td width="50%">

### 🚦 Traffic Light Interface
Instant, explainable feedback designed to combat **alert fatigue**. Users get a clear Red / Yellow / Green verdict with reasoning — not cryptic scores.

</td>
<td width="50%">

### 🔬 OSINT & DNS Forensics
Leverages `python-whois` for domain age lookup and `dnspython` for DNS record analysis, providing a full forensic fingerprint of any suspicious domain.

</td>
</tr>
</table>

---

## 🏗️ System Architecture

### How the Dual-Engine Works

```
INPUT: Email Text + Sender Domain URL
         │
         ├──────────────────────────────────────────────┐
         │                                              │
         ▼                                              ▼
 ┌────────────────────┐                    ┌─────────────────────────┐
 │   🤖 ML ENGINE     │                    │   🔬 FORENSIC ENGINE    │
 │                    │                    │                         │
 │  • TF-IDF          │                    │  • WHOIS Lookup         │
 │    Vectorization   │                    │  • Domain Age Check     │
 │  • Random Forest   │                    │    (Flag if < 30 days)  │
 │    Classifier      │                    │  • DNS Record Analysis  │
 │  • Urgency NLP     │                    │  • OSINT Correlation    │
 │    Detection       │                    │                         │
 └────────┬───────────┘                    └────────────┬────────────┘
          │                                             │
          │   ML Probability Score                      │   Forensic Risk Flag
          └─────────────────────┬───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   ⚖️  VERDICT ENGINE   │
                    │   Weighted Fusion     │
                    │   Logic (app.py)      │
                    └───────────┬───────────┘
                                │
                   ┌────────────▼─────────────┐
                   │  🚦 Final Verdict + JSON  │
                   │  { risk, score, reason }  │
                   └──────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Chrome Extension (MV3) | UI, DOM telemetry, user interaction |
| **Communication** | JavaScript Fetch API (async) | Client ↔ Backend messaging |
| **Backend** | Python 3.11 + Flask | REST API gateway & verdict logic |
| **ML Model** | Scikit-Learn (Random Forest) | Phishing classification |
| **NLP** | TF-IDF Vectorizer (Joblib) | Text feature extraction |
| **Data Processing** | Pandas | Dataset handling & preprocessing |
| **Domain Forensics** | `python-whois` | Domain age & registrar lookup |
| **DNS Analysis** | `dnspython` | DNS record inspection |
| **Datasets** | Enron (legit) + Nazario (phishing) | Model training corpus |

---

## ⚙️ Installation & Setup

### Prerequisites

- ✅ **Python 3.11+** installed and on your `PATH`
- ✅ **Google Chrome** or any Chromium-based browser
- ✅ **Git** for cloning the repository

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/K921-cyber/Phishing_project.git
cd Phishing_project
```

### Step 2 — Install Backend Dependencies

```bash
cd backend
pip install flask flask-cors scikit-learn pandas joblib python-whois dnspython
```

### Step 3 — Train the ML Model

Generate the serialized model artifacts. This only needs to be done once.

```bash
python train_model.py
```

> ✅ **Expected output:** `Success! Model saved as 'phishing_model.pkl'`
>
> This creates two files: `phishing_model.pkl` (classifier) and `vectorizer.pkl` (TF-IDF tokenizer).

### Step 4 — Start the Analysis Engine

```bash
python app.py
```

> 🟢 **Server running at:** `http://127.0.0.1:5000`
>
> The terminal will display a live logging console for real-time debugging.

### Step 5 — Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Toggle **Developer Mode** ON (top-right corner)
3. Click **"Load unpacked"**
4. Select the `/extension` folder from this repository
5. 🛡️ The **PhishTrace AI** icon will appear in your browser toolbar

---

## 📊 Performance Results

<div align="center">

| Metric | Result | Notes |
|:---:|:---:|:---|
| 🎯 **Model Accuracy** | **94%** | Evaluated on held-out test split |
| ⏱️ **Domain Age Lookup** | **~1.2 sec** | Avg. WHOIS query latency |
| 🚀 **ML Inference** | **< 1ms** | Model pre-loaded into RAM |
| 🛡️ **Zero-Day Detection** | **100%** | All simulated new domains flagged |

</div>

> **Why sub-millisecond inference?** The serialized model is loaded into RAM on server startup via `joblib`. Every subsequent request hits an in-memory object — no disk I/O on the critical path.

---

## 📂 Project Structure

```
PhishTrace-AI/
│
├── 📁 backend/
│   ├── app.py                  # Flask REST API & weighted verdict logic
│   ├── train_model.py          # ML training pipeline & serialization utility
│   ├── phishing_model.pkl      # ⚙️  Serialized Random Forest (generated)
│   ├── vectorizer.pkl          # ⚙️  TF-IDF Vectorizer (generated)
│   └── datasets/
│       ├── enron/              # Legitimate email corpus
│       └── nazario/            # Phishing email corpus
│
├── 📁 extension/
│   ├── manifest.json           # Chrome MV3 configuration & permissions
│   ├── popup.html              # Traffic Light UI layout
│   ├── popup.js                # Dynamic verdict rendering & animation
│   └── content.js              # DOM telemetry extraction (active tab)
│
└── 📄 README.md
```

---

## 🔬 The Core Problem Solved

| Traditional Approach | PhishTrace AI Approach |
|---|---|
| Server-side blacklist lookup | **Client-side, local analysis** |
| Hours/days to list new threats | **Instant zero-day flagging** |
| Binary block/allow decisions | **Probabilistic risk scoring** |
| Sends URL to external servers | **100% local — no data leaves device** |
| Alert fatigue from vague warnings | **Explainable Red/Yellow/Green verdicts** |

---

<div align="center">

**Built with 🛡️ to keep humans one step ahead of attackers.**

*PhishTrace AI — Because the best firewall is an informed user.*

</div>
