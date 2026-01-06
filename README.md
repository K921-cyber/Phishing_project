# PhishTrace AI: Hybrid Client-Side Phishing Detection

[cite_start]**PhishTrace AI** is a specialized security framework designed to address the "Human Layer" vulnerability in cybersecurity[cite: 64, 65]. [cite_start]Unlike traditional server-side filters, this project utilizes a hybrid, client-side approach to detect phishing attacks in real-time directly within the browser[cite: 66, 67].

[cite_start]The system combines **Machine Learning (Behavioral Analysis)** and **Digital Forensics (OSINT)** to bridge the latency gap inherent in reputation-based blacklists[cite: 68, 73].

---

## 🚀 Key Features

* [cite_start]**Dual-Engine Detection:** Integrates a Random Forest Classifier for semantic analysis and a Forensic Engine for technical verification[cite: 68].
* [cite_start]**Real-Time Zero-Day Defense:** Automatically flags domains registered less than **30 days ago** as high-risk, catching threats before they appear on blacklists[cite: 53, 179].
* [cite_start]**Behavioral Analysis:** Detects psychological triggers such as urgency, coercion, and fear in email text[cite: 99, 136].
* [cite_start]**Client-Side Privacy:** Operates via a Chrome Extension and a local Flask server (`127.0.0.1`), ensuring analysis happens locally without data leakage[cite: 150].
* [cite_start]**Traffic Light Interface:** Provides immediate, explainable feedback (Red/Yellow/Green) to combat user alert fatigue[cite: 54, 85].

---

## 🛠️ Tech Stack

### Frontend (Client)
* [cite_start]**Google Chrome Extension:** Manifest V3 Architecture (Secure & Ephemeral)[cite: 49, 230].
* [cite_start]**Languages:** HTML5, CSS3, JavaScript (ES6)[cite: 154, 221].
* [cite_start]**Communication:** Asynchronous HTTP `fetch` API[cite: 204].

### Backend (Server)
* [cite_start]**Language:** Python 3.11+[cite: 220].
* [cite_start]**Framework:** Flask (REST API Gateway)[cite: 156, 222].
* [cite_start]**Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas, Joblib (Serialization)[cite: 227, 228, 229].
* [cite_start]**Forensics:** `python-whois` (Domain Age Lookup), `dnspython`[cite: 232].

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.11 or higher.
* Google Chrome (or Chromium-based browser).

### 1. Clone the Repository
```bash
git clone [https://github.com/K921-cyber/Phishing_project.git](https://github.com/K921-cyber/Phishing_project.git)
cd Phishing_project
