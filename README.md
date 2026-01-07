# PhishTrace AI: Hybrid Client-Side Phishing Detection

![Project Status](https://img.shields.io/badge/Status-Capstone_Project-blue)
![Python](https://img.shields.io/badge/Backend-Python_Flask-green)
![Platform](https://img.shields.io/badge/Platform-Chrome_Extension_V3-yellow)

[cite_start]**PhishTrace AI** is a specialized security framework designed to address the "Human Layer" vulnerability in cybersecurity[cite: 64]. [cite_start]Unlike traditional server-side filters, this project utilizes a hybrid, client-side approach to detect phishing attacks in real-time directly within the browser[cite: 65].

[cite_start]The system combines **Machine Learning (Behavioral Analysis)** and **Digital Forensics (OSINT)** to bridge the "latency gap" inherent in reputation-based blacklists [cite: 73-75].

---

## 🚀 Key Features

* [cite_start]**Dual-Engine Detection:** Integrates a Random Forest Classifier for semantic analysis and a Digital Forensic Module for technical verification [cite: 50-52].
* [cite_start]**Real-Time Zero-Day Defense:** Automatically flags domains registered less than **30 days ago** as high-risk, catching threats before they appear on global blocklists[cite: 53].
* [cite_start]**Behavioral Analysis:** Detects psychological triggers such as urgency ("Act Now"), coercion, and fear in email text using NLP[cite: 51, 99].
* [cite_start]**Client-Side Privacy:** Operates via a Chrome Extension and a local Flask server (`127.0.0.1`), ensuring analysis happens locally to prevent sensitive data leakage[cite: 150].
* [cite_start]**Traffic Light Interface:** Provides immediate, explainable feedback (Red/Yellow/Green) to the user, effectively combating "alert fatigue"[cite: 54, 85].

---

## 🛠️ Tech Stack

### Frontend (Client)
* [cite_start]**Browser Technology:** Google Chrome Manifest V3 (Secure & Ephemeral Service Workers) [cite: 230-231].
* [cite_start]**Languages:** HTML5, CSS3, JavaScript (ES6) for DOM manipulation[cite: 221].
* [cite_start]**Communication:** Asynchronous HTTP `fetch` API[cite: 204].

### Backend (Server)
* [cite_start]**Language:** Python 3.11+[cite: 220].
* [cite_start]**Framework:** Flask (REST API Gateway)[cite: 222].
* [cite_start]**Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas (Data Processing), Joblib (Model Serialization) [cite: 227-229].
* [cite_start]**Forensics:** `python-whois` (Domain Age Lookup), `dnspython`[cite: 232].

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
2. Backend Setup
Navigate to the backend directory and install the required dependencies.

Bash

cd backend
pip install flask flask-cors scikit-learn pandas joblib python-whois dnspython
3. Train the Model
Before running the server, you must generate the ML model artifacts. The train_model.py utility handles tokenization and serialization.

Bash

python train_model.py

Output: "Success! Model saved as 'phishing_model.pkl'".

4. Start the Analysis Engine
Run the Flask application. It provides a live logging console for debugging.

Bash

python app.py
The server will start on http://127.0.0.1:5000.

5. Frontend Setup (Chrome Extension)
Open Chrome and navigate to chrome://extensions/.

Enable Developer Mode (toggle in the top right corner).

Click Load unpacked.

Select the extension folder from this repository.

The PhishTrace icon should appear in your browser toolbar.

📊 Performance Results

Accuracy: The Random Forest model achieved 94% accuracy on the test dataset.


Speed: Domain Age lookups averaged 1.2 seconds, detecting 100% of simulated zero-day domains.


Latency: The system is optimized to perform inference in sub-millisecond time by loading models into RAM.

📂 Project Structure
Plaintext

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
