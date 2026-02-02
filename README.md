# PhishTrace AI: Hybrid Client-Side Phishing Detection

![Project Status](https://img.shields.io/badge/Status-Capstone_Project-blue)
![Python](https://img.shields.io/badge/Backend-Python_Flask-green)
![Platform](https://img.shields.io/badge/Platform-Chrome_Extension_V3-yellow)

**PhishTrace AI** is a specialized security framework designed to address the "Human Layer" vulnerability in cybersecurity. Unlike traditional server-side filters, this project utilizes a hybrid, client-side approach to detect phishing attacks in real-time directly within the browser.

The system combines **Machine Learning (Behavioral Analysis)** and **Digital Forensics (OSINT)** to bridge the "latency gap" inherent in reputation-based blacklists.

---

## 🚀 Key Features

* **Dual-Engine Detection:** Integrates a Random Forest Classifier for semantic analysis and a Digital Forensic Module for technical verification.
* **Real-Time Zero-Day Defense:** Automatically flags domains registered less than **30 days ago** as high-risk, catching threats before they appear on global blocklists.
* **Behavioral Analysis:** Detects psychological triggers such as urgency ("Act Now"), coercion, and fear in email text using NLP.
* **Client-Side Privacy:** Operates via a Chrome Extension and a local Flask server (`127.0.0.1`), ensuring analysis happens locally to prevent sensitive data leakage.
* **Traffic Light Interface:** Provides immediate, explainable feedback (Red/Yellow/Green) to the user, effectively combating "alert fatigue".

---

## 🛠️ Tech Stack

### Frontend (Client)
* **Browser Technology:** Google Chrome Manifest V3 (Secure & Ephemeral Service Workers) .
* **Languages:** HTML5, CSS3, JavaScript (ES6) for DOM manipulation.
* **Communication:** Asynchronous HTTP `fetch` API.

### Backend (Server)
* **Language:** Python 3.11+.
* **Framework:** Flask (REST API Gateway).
* **Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas (Data Processing), Joblib (Model Serialization) .
* **Forensics:** `python-whois` (Domain Age Lookup), `dnspython`.

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.11 or higher installed.
* Google Chrome (or any Chromium-based browser).

### 1. Clone the Repository
```bash
git clone [https://github.com/K921-cyber/Phishing_project.git](https://github.com/K921-cyber/Phishing_project.git)
cd Phishing_project
```
### 2. Backend Setup
Navigate to the backend directory and install the required dependencies.
```
cd backend
pip install flask flask-cors scikit-learn pandas joblib python-whois dnspython
```
### 3. Train the Model
Before running the server, you must generate the ML model artifacts. The train_model.py utility handles tokenization and serialization.
```

python train_model.py

Output: "Success! Model saved as 'phishing_model.pkl'".
```
### 4. Start the Analysis Engine
Run the Flask application. It provides a live logging console for debugging.

```

python app.py
The server will start on http://127.0.0.1:5000.
```
### 5. Frontend Setup (Chrome Extension)
Open Chrome and navigate to chrome://extensions/.

Enable Developer Mode (toggle in the top right corner).

Click Load unpacked.

Select the extension folder from this repository.

The PhishTrace icon should appear in your browser toolbar.

## 📊 Performance Results

Accuracy: The Random Forest model achieved 94% accuracy on the test dataset.


Speed: Domain Age lookups averaged 1.2 seconds, detecting 100% of simulated zero-day domains.


Latency: The system is optimized to perform inference in sub-millisecond time by loading models into RAM.

📂 Project Structure
```Plaintext

PhishTrace-AI/
├── backend/
│   ├── app.py              # Flask REST API & Verdict Logic
│   ├── train_model.py      # ML Training Utility & Serialization
│   ├── phishing_model.pkl  # Serialized Model (Generated)
│   ├── vectorizer.pkl      # NLP Vectorizer (Generated)
│   └── datasets/           # Enron (Legit) & Nazario (Phishing) Data
├── extension/
│   ├── manifest.json       # V3 Configuration
│   ├── popup.html          # Traffic Light UI
│   ├── popup.js            # Dynamic Logic & Animation
│   └── content.js          # DOM Telemetry Extraction
└── README.md










