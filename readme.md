# PhishSentinel

> **Multi-engine, client-side phishing detection for email.**  
> Six detection engines fire in parallel. No cloud. No data leakage.

![Version](https://img.shields.io/badge/Version-2.0.0-0d1520?style=for-the-badge&logo=shield&logoColor=00ccff)
![Python](https://img.shields.io/badge/Python-3.11+-00ff88?style=for-the-badge&logo=python&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-00ccff?style=for-the-badge&logo=fastapi&logoColor=black)
![Extension](https://img.shields.io/badge/Chrome-Manifest_V3-ffcc00?style=for-the-badge&logo=googlechrome&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

---

## Table of Contents

1. [The Problem PhishSentinel Solves](#1-the-problem-phishsentinel-solves)  
2. [What Is New vs PhishTrace v1](#2-what-is-new-vs-phishtrace-v1)  
3. [System Architecture](#3-system-architecture)  
4. [Detection Engines](#4-detection-engines)  
5. [Tech Stack](#5-tech-stack)  
6. [Project Structure](#6-project-structure)  
7. [Installation & Setup](#7-installation--setup)  
8. [API Reference](#8-api-reference)  
9. [How Scoring Works](#9-how-scoring-works)  
10. [Threat Model](#10-threat-model)  
11. [Performance](#11-performance)  
12. [Limitations & Roadmap](#12-limitations--roadmap)  
13. [Contributing](#13-contributing)  

---

## 1. The Problem PhishSentinel Solves

Traditional anti-phishing tools rely on **reputation blocklists** — databases of known bad domains that are maintained by vendors like Google Safe Browsing or Microsoft SmartScreen. These work well for *old* threats but fail completely for **zero-day phishing**:

```
Hour 0:  Attacker registers secure-paypa1-login.xyz  ($1 on Namecheap)
Hour 0:  Attacker provisions a Let's Encrypt TLS cert  (free, takes 30 seconds)
Hour 1:  Mass phishing emails sent to 500,000 targets
Hour 8:  Google Safe Browsing finally flags the domain
          ↑
          8 hours of unprotected exposure
```

PhishSentinel attacks this gap with signals that are visible **from the moment of registration**, not from accumulated reputation.

---

## 2. What Is New vs PhishTrace v1

| Feature | PhishTrace v1 | PhishSentinel v2 |
|---|---|---|
| Backend framework | Flask (sync) | **FastAPI (async)** |
| Engine execution | Sequential | **All engines run in parallel** |
| IP Rollback prevention | ✅ | ✅ Enhanced |
| Domain age check | ✅ Single sender domain | ✅ **All links checked** |
| ML engine | ✅ RF | ✅ RF + feature explainability |
| **Homograph / IDN detection** | ❌ | ✅ Unicode lookalike detection |
| **Typosquatting detection** | ❌ | ✅ Levenshtein vs 50 brands |
| **URL shortener expansion** | ❌ | ✅ Full redirect chain |
| **SSL certificate age** | ❌ | ✅ New cert = suspicious |
| **Email header auth** | ❌ | ✅ SPF / DKIM / DMARC parsing |
| **Suspicious TLD scoring** | ❌ | ✅ .tk / .xyz / .top etc. |
| **Subdomain depth analysis** | ❌ | ✅ Nested subdomain detection |
| **Keyword injection** | ❌ | ✅ Brand in subdomain check |
| **Weighted threat score** | ❌ | ✅ 0-100 per-engine weighted score |
| **Worst-case escalation** | ❌ | ✅ Any 90+ score → forces HIGH |
| API endpoint | GET (leaks in logs) | **POST only (body only)** |
| Rate limiting | Basic | Enhanced (40 req/min) |
| Popup UI | Traffic light + table | **Animated threat gauge + engine bars + findings feed** |
| Redirect unwrapping | Gmail only | **Gmail + Outlook + all shorteners** |
| Auto-docs | ❌ | ✅ Swagger at `/docs` |

---

## 3. System Architecture

```
╔═══════════════════════════════════════════════════════════════════╗
║                        CHROME BROWSER                             ║
║                                                                   ║
║  ┌─────────────────────────┐     ┌──────────────────────────┐   ║
║  │   Gmail / Outlook Web   │     │   PhishSentinel Popup     │   ║
║  │                         │     │                           │   ║
║  │  content.js             │◄────│  • Animated threat gauge  │   ║
║  │  ├─ Extract body text   │     │  • Engine breakdown bars  │   ║
║  │  ├─ Collect all hrefs   │     │  • Findings feed          │   ║
║  │  ├─ Unwrap redirects    │     │  • Per-link forensic table│   ║
║  │  └─ Read auth signals   │     │  • Escalation notice      │   ║
║  └────────────┬────────────┘     └──────────────────────────┘   ║
╚══════════════|════════════════════════════════════════════════════╝
               │  POST /api/scan
               │  { text, links[], raw_headers }
               │  (JSON body — never in URL)
               ▼
╔═══════════════════════════════════════════════════════════════════╗
║         FastAPI Backend  ·  127.0.0.1:5000  (loopback only)       ║
║                                                                   ║
║   asyncio.gather() — all engines fire simultaneously              ║
║   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────────┐  ║
║   │ ML Engine  │ │  Domain    │ │ Heuristic  │ │   Header    │  ║
║   │            │ │  Engine    │ │  Engine    │ │   Engine    │  ║
║   │ TF-IDF +   │ │            │ │            │ │             │  ║
║   │ Random     │ │ • Raw-IP   │ │ • Homograph│ │ • SPF check │  ║
║   │ Forest     │ │ • WHOIS age│ │ • Typosquat│ │ • DKIM check│  ║
║   │            │ │ • DNS check│ │ • Shortener│ │ • DMARC     │  ║
║   │ Score: 0-  │ │ • SSL cert │ │   expand   │ │ • Reply-To  │  ║
║   │ 100        │ │ • Subd.dep │ │ • Keyword  │ │   mismatch  │  ║
║   │ Weight:0.70│ │ • Susp. TLD│ │   injection│ │ • Display   │  ║
║   └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ │   name spoof│  ║
║         │              │              │         └──────┬──────┘  ║
║         └──────────────┴──────────────┴────────────────┘         ║
║                                  │                               ║
║                        scorer.aggregate()                         ║
║                    Weighted average + escalation                  ║
║                                  │                               ║
║             { overall_score, overall_risk, colour,               ║
║               engine_scores, all_findings, detail }              ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 4. Detection Engines

### Engine 1 — ML Behavioural Analysis

Analyses the email body text using a **TF-IDF vectorizer** (unigrams + bigrams, 15 000 features) feeding into a **Random Forest classifier** (300 trees) trained on the Enron (legitimate) and Nazario (phishing) email corpora.

Key patterns the model learns:
- Urgency language: *"act now"*, *"expires in 24 hours"*, *"account suspended"*
- Fear and coercion: *"legal action"*, *"final notice"*, *"suspicious activity detected"*  
- Credential harvesting: *"enter your password"*, *"confirm your billing information"*
- Impersonation tells: generic salutations, brand names used inconsistently with URLs

Returns: phishing probability (0–100), predicted label, top 5 trigger words.

---

### Engine 2 — Domain OSINT Forensics

For **every link** extracted from the email (not just the sender's domain):

| Check | Method | High Risk Signal |
|---|---|---|
| Raw IP detection | `ipaddress.ip_address()` | Any IPv4/IPv6 used directly |
| Domain age | WHOIS lookup | < 30 days old |
| DNS existence | A-record query | Domain doesn't resolve |
| SSL cert age | TLS handshake | Certificate < 30 days old |
| Suspicious TLD | Static lookup table | `.tk`, `.xyz`, `.ml`, etc. |
| Subdomain depth | Label counting | ≥ 4 subdomain levels |

All network checks run concurrently via `asyncio.gather()` with a thread pool executor.

---

### Engine 3 — Heuristic Analysis

**Homograph / IDN Spoofing Detection:**  
Decodes punycode (`xn--`), applies NFKD normalisation, then maps 15+ confusable Unicode characters (Cyrillic `а` → Latin `a`, Greek `ο` → Latin `o`, etc.) to their ASCII equivalents. The normalised domain is compared against known brands.

```
Domain received: pаypal.com   (Cyrillic 'а', not Latin 'a')
Encoded form:    xn--pypal-6ve.com
After normalise: paypal.com  ← matches brand → HIGH RISK
```

**Typosquatting Detection:**  
Levenshtein edit distance between the registered domain (TLD+1) and 50+ known brands. Distance ≤ 2 with a non-identical result = typosquat.

```
paypa1.com  →  edit distance from "paypal" = 1  →  TYPOSQUAT
```

**Keyword Injection Detection:**  
Brand name present in subdomain but not in the registered domain:

```
paypal.secure-login.evil.xyz
  ↑                    ↑
brand in subdomain   registered domain = evil.xyz
→ KEYWORD INJECTION
```

**URL Shortener Expansion:**  
Follows the complete redirect chain for 16 known shortener services (bit.ly, tinyurl, t.co, etc.) and runs all other engines on the **real destination**, not the shortened URL.

---

### Engine 4 — Email Header Authentication

Parses the raw email header block (if accessible) to check:

| Header | What it means | Fail = ? |
|---|---|---|
| `SPF` | Was the sending IP authorised by the domain? | Server not authorised — spoofed sender |
| `DKIM` | Is the email's cryptographic signature valid? | Message tampered or forged |
| `DMARC` | Do SPF/DKIM results align with the From domain? | Policy violation — likely spoofed |
| `Reply-To` | Does Reply-To domain match From domain? | Replies go to attacker's mailbox |
| Display name | Does the visible name match the actual email address? | Classic impersonation |
| X-Mailer | Does the mailer header reveal a bulk-sending tool? | Phishing infrastructure fingerprint |

---

## 5. Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **FastAPI** | Async REST API with auto-generated Swagger docs |
| **uvicorn** | ASGI server for FastAPI |
| **scikit-learn** | Random Forest classifier |
| **pandas** | Dataset loading and preprocessing |
| **joblib** | Model serialization (compressed `.pkl`) |
| **python-whois** | WHOIS domain registration date lookup |
| **dnspython** | DNS A-record existence checks |
| **httpx** | Async HTTP client for redirect chain following |
| **pydantic** | Request validation and schema definition |

### Frontend (Chrome Extension)

| Technology | Purpose |
|---|---|
| **Manifest V3** | Modern Chrome extension format |
| **Content Scripts** | DOM access for email body + link extraction |
| **Fetch API (POST)** | Secure transport to local backend |
| **Vanilla JS + CSS** | Zero-dependency popup UI |
| **CSS animations** | Threat gauge, engine bars, findings feed |

---

## 6. Project Structure

```
PhishSentinel/
│
├── backend/
│   ├── main.py                  # FastAPI app, routes, middleware, rate limiting
│   ├── config.py                # All thresholds, weights, brand lists, TLD sets
│   ├── scorer.py                # Weighted aggregation + worst-case escalation
│   ├── train_model.py           # ML training utility with eval + cross-validation
│   │
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── ml_engine.py         # TF-IDF + Random Forest + feature explainability
│   │   ├── domain_engine.py     # WHOIS, DNS, SSL cert, raw-IP, TLD, subdomain depth
│   │   ├── heuristic_engine.py  # Homograph IDN, typosquat, shortener expansion, keyword inject
│   │   └── header_engine.py     # SPF, DKIM, DMARC, Reply-To, display-name spoof
│   │
│   └── datasets/
│       ├── enron/               # Legitimate email corpus (.txt files)
│       └── nazario/             # Phishing email corpus (.txt files)
│
├── extension/
│   ├── manifest.json            # MV3 config, permissions, host access, CSP
│   ├── popup.html               # Cyberpunk terminal UI shell
│   ├── popup.js                 # Verdict rendering: gauge, engine bars, findings, table
│   ├── content.js               # Email extraction: text, links, redirect unwrapping, headers
│   └── icons/
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
│
└── README.md
```

---

## 7. Installation & Setup

### Prerequisites

- Python **3.11** or newer
- `pip` package manager
- Google Chrome (or any Chromium-based browser)
- Git

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/K921-cyber/PhishSentinel.git
cd PhishSentinel
```

---

### Step 2 — Install Python Dependencies

```bash
cd backend
pip install fastapi uvicorn[standard] scikit-learn pandas joblib python-whois dnspython httpx pydantic
```

Or install from the requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt contents:**

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
scikit-learn>=1.4.0
pandas>=2.2.0
joblib>=1.4.0
python-whois>=0.9.4
dnspython>=2.6.1
httpx>=0.27.0
pydantic>=2.7.0
```

---

### Step 3 — Get Email Datasets (for ML training)

**Option A — Real corpora (recommended):**

| Dataset | Type | Source |
|---|---|---|
| Enron Email Corpus | Legitimate | [cs.cmu.edu/~enron](https://www.cs.cmu.edu/~enron/) |
| Nazario Phishing Corpus | Phishing | (yet to decide) |

Extract email files (one email per `.txt` file) into:
```
backend/datasets/enron/        ← legitimate emails
backend/datasets/nazario/      ← phishing emails
```

**Option B — CSV dataset:**

Use any CSV with `text` (email body) and `label` (0 = legitimate, 1 = phishing) columns:

```bash
python train_model.py --csv /path/to/dataset.csv
```

**Option C — Synthetic fallback (no data needed):**

If no datasets are found, `train_model.py` automatically generates a synthetic training set. Suitable for testing the pipeline; **not for production**.

---

### Step 4 — Train the ML Model

```bash
cd backend
python train_model.py
```

Expected output:
```
[INFO] Dataset: 6240 samples | Legitimate: 3180 | Phishing: 3060
[INFO] Fitting TF-IDF vectorizer…
[INFO] Training Random Forest (this may take a moment)…
==================================================
Test Accuracy : 94.1%

Classification Report:
              precision    recall  f1-score
  Legitimate     0.95       0.93      0.94
    Phishing     0.93       0.95      0.94

5-Fold CV F1  : 0.942 ± 0.011
==================================================
✅  Saved: phishing_model.pkl  (14 MB)
✅  Saved: vectorizer.pkl  (2 MB)
Ready. Start the server with:  python main.py
```

---

### Step 5 — Start the Analysis Server

```bash
python main.py
```

Expected output:
```
INFO:     ✅  ML model loaded from disk.
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000
```

> **Note:** The server binds **only to `127.0.0.1` (loopback)**. It is not accessible from the network — your email data never leaves your machine.

To verify the server is running:
```bash
curl http://127.0.0.1:5000/api/health
```

**Interactive API docs** (Swagger UI) are available at:  
```
http://127.0.0.1:5000/docs
```

---

### Step 6 — Load the Chrome Extension

1. Open Chrome → navigate to `chrome://extensions/`
2. Toggle **Developer mode** (top-right corner)
3. Click **Load unpacked**
4. Select the `extension/` folder
5. The PhishSentinel shield icon 🛡 appears in your toolbar

> **Tip:** Pin the extension to your toolbar for quick access.

---

### Step 7 — Scan Your First Email

1. Open **Gmail**, **Outlook Web**, or **Yahoo Mail**
2. Click on any email you want to analyse
3. Click the 🛡 PhishSentinel icon in your toolbar
4. Click **INITIATE SCAN**
5. The popup shows:
   - **Threat gauge** (0–100 animated score)
   - **Engine breakdown** (4 horizontal signal bars)
   - **Findings feed** (specific reasons for the verdict)
   - **Link forensics table** (per-URL breakdown)

---

## 8. API Reference

All endpoints are on `http://127.0.0.1:5000`.  
Interactive docs: `http://127.0.0.1:5000/docs`

---

### `POST /api/scan`

Run a full multi-engine phishing analysis.

**Request Body (JSON):**

```json
{
  "text"        : "Dear customer, your account has been suspended...",
  "links"       : [
    "https://paypa1.com/login",
    "http://185.220.101.5/verify",
    "https://secure-login.xyz/account"
  ],
  "raw_headers" : "Authentication-Results: spf=fail dkim=none dmarc=fail"
}
```

| Field | Type | Required | Limit | Description |
|---|---|---|---|---|
| `text` | string | No* | 25 000 chars | Full email body text |
| `links` | array | No* | 30 entries | All href URLs from the email |
| `raw_headers` | string | No | 10 000 chars | Raw email header block |

*At least one field must be non-empty.

**Response (JSON):**

```json
{
  "overall_score"  : 87.4,
  "overall_risk"   : "HIGH",
  "colour"         : "RED",
  "escalated"      : true,
  "scan_time_ms"   : 1842,
  "engine_scores"  : {
    "ml"       : 78.0,
    "domain"   : 95.0,
    "heuristic": 80.0,
    "header"   : 60.0
  },
  "all_findings"   : [
    "Raw IP address (185.220.101.5) used directly — bypasses all domain-reputation checks.",
    "Domain 'secure-login.xyz' is only 3 day(s) old.",
    "TLD '.xyz' is commonly abused for phishing.",
    "Typosquatting detected: 'paypa1' is 1 edit away from 'paypal'.",
    "SPF = 'fail': The sender's identity could not be verified.",
    "ML confidence: 78.0% phishing probability.",
    "Top triggers detected: verify, account, suspended, immediately."
  ],
  "detail": {
    "ml"       : { "engine": "ml", "score": 78.0, "label": "PHISHING", ... },
    "domain"   : { "engine": "domain", "score": 95.0, "urls": [...], ... },
    "heuristic": { "engine": "heuristic", "score": 80.0, "typosquat_hits": [...], ... },
    "header"   : { "engine": "header", "score": 60.0, "spf": "fail", "dkim": "none", ... }
  }
}
```

---

### `GET /api/health`

```json
{
  "status"  : "ok",
  "version" : "2.0.0",
  "engines" : {
    "ml"       : "ready",
    "domain"   : "ready",
    "heuristic": "ready",
    "header"   : "ready"
  }
}
```

---

## 9. How Scoring Works

Each engine produces a score from 0 to 100, representing the likelihood of a phishing signal in that engine's domain. These are combined into a single **weighted threat score**:

```
final_score = Σ (engine_score × engine_weight) / Σ weights
```

### Engine Weights

| Engine | Weight | Why |
|---|---|---|
| Raw IP (domain engine) | 1.00 | Near-certain phishing signal |
| Homograph (heuristic) | 0.95 | Very strong brand spoofing signal |
| Typosquat (heuristic) | 0.80 | Strong brand confusion signal |
| ML classifier | 0.70 | Reliable but can be evaded by clean language |
| Domain age (domain) | 0.65 | Strong zero-day signal |
| Header auth fail | 0.60 | Definitive spoofing evidence when present |
| SSL cert age | 0.45 | Corroborating signal, not standalone proof |
| Suspicious TLD | 0.40 | Supporting signal |
| Subdomain depth | 0.30 | Weak standalone, strong corroborator |

### Worst-Case Escalation

If **any single engine** scores ≥ 90, the overall verdict is forced to **HIGH** regardless of other engine scores. This prevents a highly suspicious signal from being diluted by other engines that happen to score low.

Example: A raw-IP link (score=100) in an otherwise clean email with low ML score still produces a HIGH verdict.

### Verdict Mapping

| Score | Risk | Colour | Meaning |
|---|---|---|---|
| ≥ 60 | HIGH | 🔴 RED | Almost certainly phishing |
| 35–59 | MEDIUM | 🟡 YELLOW | Suspicious — review carefully |
| < 35 | LOW | 🟢 GREEN | No significant signals detected |

---

## 10. Threat Model

### What PhishSentinel Detects

| Attack Type | Engine | Detection Method |
|---|---|---|
| Brand-new phishing domain | Domain | WHOIS age < 30 days |
| Raw-IP phishing (no domain) | Domain | `ipaddress.ip_address()` check |
| Homograph / IDN spoofing | Heuristic | Unicode normalisation + brand matching |
| Typosquatting | Heuristic | Levenshtein distance ≤ 2 from brand list |
| Brand keyword injection | Heuristic | Brand in subdomain, different registered domain |
| Short URL concealment | Heuristic | Shortener expansion, redirect chain analysis |
| Freshly provisioned TLS cert | Domain | SSL certificate age < 30 days |
| Abused TLD | Domain | Suspicious TLD static scoring |
| SPF / DKIM / DMARC failure | Header | Authentication result parsing |
| Reply-To mismatch | Header | Domain comparison |
| Display-name spoofing | Header | Brand in display name vs actual sender |
| Deep fake subdomain nesting | Domain | Subdomain depth ≥ 4 |
| Urgency / coercion language | ML | TF-IDF + Random Forest |
| Gmail/Outlook redirect hiding | Content | Redirect URL unwrapping |

### What PhishSentinel Does NOT Protect Against

| Attack | Reason |
|---|---|
| Aged phishing domains (>90 days) | WHOIS alone cannot flag old-but-malicious domains |
| Legitimate domains serving malware | No URL content scanning or sandboxing |
| Spear phishing (no urgency language) | ML model relies on common phishing language patterns |
| Voice / SMS phishing (vishing/smishing) | Browser extension scope only |
| 0-day CVE exploits in email clients | Out of scope |

---

## 11. Performance

| Metric | Value | Notes |
|---|---|---|
| ML inference time | < 1 ms | Model pre-loaded in RAM at startup |
| Homograph check | < 1 ms | Pure string operations |
| Typosquatting check | ~2 ms | O(n × m) Levenshtein per brand |
| DNS check | 50–200 ms | Network-dependent |
| WHOIS lookup | 500–2000 ms | Slowest step; bottleneck for many unique domains |
| SSL cert check | 100–500 ms | TLS handshake per domain |
| Full scan (5 links) | ~1.5-3 s | Parallel execution; bounded by WHOIS |
| Full scan (1 link) | ~0.8-1.5 s | Single WHOIS lookup |
| Raw-IP detection | < 0.1 ms | No network needed |
| ML test accuracy | ~94% | Enron + Nazario combined corpus |

---

## 12. Limitations & Roadmap

### Current Limitations

- **WHOIS latency** is the primary bottleneck. Emails with 10+ unique new domains may take 5–8 seconds to scan.
- The **ML model** is trained on English-language email datasets. Phishing emails in Hindi, regional languages, or multilingual content may score lower than expected.
- **Header extraction** from webmail clients is limited by what the DOM exposes. Full raw headers require the user to open "Show original" in Gmail first.
- The backend must be **started manually** — no auto-start mechanism included yet.

### Roadmap

- [ ] **Async WHOIS** via `aiodns` + custom WHOIS parser to replace blocking calls
- [ ] **Visual similarity hashing** — screenshot page, compare pHash against known login page fingerprints
- [ ] **PhishTank / OpenPhish** free feed integration — real-time blacklist check
- [ ] **Multilingual ML model** — train on phishing corpora in Hindi and other Indian languages
- [ ] **Auto-start service** — Windows Task Scheduler / Linux systemd unit file
- [ ] **Firefox extension** port (WebExtension API compatible)
- [ ] **DMARC DNS lookup** — actively query `_dmarc.sender-domain.com` instead of relying on headers
- [ ] **Dashboard page** — full-page analysis report with historical scan log

---

## 13. Contributing

Contributions welcome! Open an issue before starting large changes to discuss the approach.

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/PhishSentinel.git

# 3. Create a feature branch
git checkout -b feature/add-async-whois

# 4. Make your changes, add tests
# 5. Commit with a descriptive message
git commit -m "feat(domain): replace blocking WHOIS with async aiodns lookup"

# 6. Push and open a Pull Request
git push origin feature/add-async-whois
```

### Commit Message Convention

| Prefix | When to use |
|---|---|
| `feat(scope):` | New feature |
| `fix(scope):` | Bug fix |
| `perf(scope):` | Performance improvement |
| `docs:` | Documentation only |
| `test:` | Adding or fixing tests |
| `refactor:` | Code restructure, no behaviour change |

### Coding Standards

- Backend: PEP 8, type hints on all public functions, docstrings on all classes and public methods
- Frontend: ES6+, JSDoc on exported functions, no runtime dependencies
- Every new engine must implement `async def run(...) -> dict` with a `score` and `findings` key

---

*Built by KAPS — Cybersecurity Researcher*  
*IndiaSkills Nationals 2025-2026 · Medallion of Excellence · Skill 54: Cyber Security*  
*Mentored by Nitish Agrawal & Smridh Gupta — Thinknyx Technologies · Shivalik College Dehradun*

---

> "The best firewall is the one that catches what others miss — before the user ever clicks."
