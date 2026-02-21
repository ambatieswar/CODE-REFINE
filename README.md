# ⚡ AI Code Review & Rewrite Agent

> Powered by **Groq Llama 3.3 70B** & **Mistral AI** · Built with **Flask** + **MongoDB**

---

**The brilliant minds---- behind CodeReview AI**
<img width="1911" height="880" alt="image" src="https://github.com/user-attachments/assets/16064198-b46f-4bb4-bc43-b32186a07f3f" />


## 🖼️ Output Screenshots
<img width="1919" height="880" alt="image" src="https://github.com/user-attachments/assets/5678fd59-f99e-45c9-aa5a-ae5c268a81e4" />


**Dashboard — Code Analysis Output**

![Dashboard Output]
<img width="1915" height="870" alt="image" src="https://github.com/user-attachments/assets/3fffcd5f-4019-4bb7-9730-ff85f958a561" />

**History Page — Review Records**

![History Output]
<img width="1916" height="885" alt="image" src="https://github.com/user-attachments/assets/71cf7563-5b64-473f-9bc3-3db4a452c415" />

**Email-Report -- Review Records**

![Email Output]
<img width="1917" height="868" alt="image" src="https://github.com/user-attachments/assets/2c784307-500e-4240-8d16-ef626661f5d3" />



**Analysus Report -- Analytics**

![Results Output]
<img width="1917" height="862" alt="image" src="https://github.com/user-attachments/assets/1bdb4a7b-4d73-42dc-9b60-9a698a90a755" />


---

## 📌 About

AI Code Review & Rewrite Agent is a full-stack web application that uses state-of-the-art Large Language Models to analyze your code in real time. It detects bugs, security vulnerabilities, performance bottlenecks, and best-practice violations — then rewrites your code into clean, production-ready output.

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 🔍 | **AI Code Analysis** | Detects bugs, security risks, performance issues, and best-practice violations with severity classification (Critical / High / Medium / Low) |
| ✨ | **Smart Rewrite** | One-click AI-powered full code rewrite — clean, documented, and production-ready |
| ⚡ | **Dual AI Providers** | Choose between Groq Llama 3.3 70B (4 models) and Mistral AI (3 models) from the dashboard |
| 👁️ | **Live Preview** | HTML code renders live in a new browser tab; other languages show syntax-highlighted output |
| 📜 | **Review History** | All reviews saved to MongoDB with full detail view, email export, and delete options |
| 📧 | **Email Reports** | Send full review reports (code + issues + fixes + rewrite) to any email via SMTP |
| 🤖 | **CodeBot Assistant** | Built-in AI chat assistant for code questions, debugging help, and explanations |
| 🔐 | **Auth System** | Sign Up, Sign In, and Forgot Password with OTP email verification |
| 🗑️ | **Delete History** | Delete individual records or clear all history with confirmation popup |

---

## 🏗️ Project Architecture

```
ai_code_review/
├── app.py               ← Flask routes, AI calls, email, all API endpoints
├── config.py            ← API keys (Groq, Mistral), MongoDB URI, SMTP config
├── database.py          ← MongoDB helpers (users, history CRUD + delete)
├── requirements.txt     ← Python dependencies
├── templates/
│   ├── landing.html     ← Landing page (hero, features, team cards, chatbot)
│   ├── auth.html        ← Sign In / Sign Up / Forgot Password (OTP flow)
│   ├── dashboard.html   ← Main code review page (model selector, analyze, rewrite)
│   └── history.html     ← Review history (view, email, delete per record)
└── static/
    └── style.css        ← Full dark theme design system (all components)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python + Flask | Web framework & routing |
| AI (Primary) | Groq SDK + Llama 3.3 70B | Ultra-fast LLM inference |
| AI (Secondary) | Mistral AI API | Alternative LLM provider |
| Database | MongoDB (PyMongo) | User accounts & history storage |
| Auth | bcrypt + Flask sessions | Secure login & password hashing |
| Email | smtplib (Gmail SMTP) | OTP delivery & report export |
| Frontend | HTML5 + CSS3 + Vanilla JS | No frameworks, pure web |
| Fonts | Sora + Space Mono | Google Fonts (via CDN) |
| Icons | Font Awesome 6.5 | UI icons (via CDN) |

---

## 🚀 Setup & Installation

### Step 1 — Clone / Download

```bash
git clone https://github.com/yourname/ai-code-review.git
cd ai-code-review
```

### Step 2 — Install Dependencies

```bash
pip install flask pymongo bcrypt groq requests
```

### Step 3 — Configure API Keys

Open `config.py` and fill in your keys:

```python
GROQ_API_KEY    = "your_groq_api_key_here"     # console.groq.com (free)
MISTRAL_API_KEY = "your_mistral_api_key_here"  # console.mistral.ai

SMTP_USER = "your_email@gmail.com"
SMTP_PASS = "your_gmail_app_password"

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME   = "ai_code_review"
```

### Step 4 — Start MongoDB

```bash
mongod
```

### Step 5 — Run the App

```bash
python app.py
```

Open your browser at → **http://localhost:5000**

---

## 📖 How to Use

### 1. Register & Login
- Go to `http://localhost:5000` and click **Get Started**
- **Sign Up** with name, email, and password
- **Sign In** to reach the Dashboard

### 2. Analyze Code
- Select **Provider**: Groq or Mistral using the toggle
- Select **Model** from the dropdown (e.g. Llama 3.3 70B Versatile)
- Select **Language** (Python, JavaScript, Java, C++, HTML, etc.)
- Paste your code in the editor
- Click **🔍 Analyze Code** — results appear instantly:
  - Score out of 100, summary, and classified issue list
  - Each issue shows type, severity, line number, description, and fix
  - If no errors: a green **"No errors found"** message is shown

### 3. Rewrite Code
- Click **✨ Rewrite Code** to get a clean, optimized version
- Use **Copy** to copy it or **Preview** to open in browser

### 4. Preview Code
- **HTML**: renders live in a new browser tab
- **Other languages**: displays syntax-highlighted code

### 5. History
- All reviews are saved automatically to MongoDB
- Click **👁 View** to see full detail (issues, code, rewrite)
- Click **📧 Email** to send the full report to any email address
- Click **🗑 Delete** to remove a single record (with confirmation)
- Click **🗑 Delete All** in the header to wipe all history

### 6. CodeBot Assistant
- Click the 🤖 button (bottom-right corner) to open CodeBot
- Ask anything about your code, bugs, or programming
- Uses your currently selected provider and model

### 7. Forgot Password
- Click **Forgot** on the auth page
- Enter your email → receive OTP → verify → set new password

---

## 🔑 Getting API Keys

### Groq API Key (Free)
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys → Create API Key**
4. Paste into `config.py` as `GROQ_API_KEY`

### Mistral API Key
1. Visit [https://console.mistral.ai](https://console.mistral.ai)
2. Create an account and go to **API Keys**
3. Generate a key and paste into `config.py` as `MISTRAL_API_KEY`

### Gmail SMTP (for Email Features)
1. Enable **2-Step Verification** on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Generate an app password for **Mail**
4. Use that 16-character password as `SMTP_PASS` in `config.py`

---

## 🤖 Available AI Models

### Groq Models
| Model ID | Name | Best For |
|----------|------|----------|
| `llama-3.3-70b-versatile` | Llama 3.3 70B (Versatile) | Best quality |
| `llama-3.1-8b-instant` | Llama 3.1 8B (Fast) | Fastest responses |
| `mixtral-8x7b-32768` | Mixtral 8x7B | Long context |
| `gemma2-9b-it` | Gemma2 9B | Lightweight |

### Mistral Models
| Model ID | Name | Best For |
|----------|------|----------|
| `mistral-large-latest` | Mistral Large | Highest quality |
| `mistral-small-latest` | Mistral Small | Balanced |
| `open-mixtral-8x7b` | Open Mixtral 8x7B | Open source |

---

## 🗄️ Database Schema (MongoDB)

### `users` collection
```json
{
  "name":       "string",
  "email":      "string (unique)",
  "password":   "binary (bcrypt hashed)",
  "otp":        "string (for password reset)",
  "otp_time":   "date",
  "created_at": "date"
}
```

### `history` collection
```json
{
  "user_email":    "string",
  "language":      "string",
  "original_code": "string",
  "review_data": {
    "has_errors": "boolean",
    "score":      "integer (0–100)",
    "summary":    "string",
    "errors": [
      {
        "type":        "string",
        "severity":    "string",
        "line":        "string",
        "description": "string",
        "fix":         "string"
      }
    ]
  },
  "rewritten_code": "string",
  "created_at":     "date"
}
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Landing page |
| GET | `/auth` | Sign In / Sign Up / Forgot Password |
| POST | `/signup` | Register new user |
| POST | `/signin` | Login user |
| POST | `/forgot-password` | Send OTP to email |
| POST | `/verify-otp` | Verify OTP code |
| POST | `/reset-password` | Reset password |
| GET | `/dashboard` | Main code review page |
| GET | `/history` | Review history page |
| POST | `/api/analyze` | Analyze code with AI |
| POST | `/api/rewrite` | Rewrite code with AI |
| POST | `/api/chat` | CodeBot chat message |
| POST | `/api/send-history-email` | Email a review report |
| POST | `/api/delete-history` | Delete one history record |
| POST | `/api/delete-all-history` | Delete all history records |
| GET | `/preview` | Preview code in browser |
| GET | `/logout` | Sign out |

---

## 👥 Team

| Avatar | Name | Role |
|--------|------|------|
| **AER** | AMBATI ESWAR REDDY | AI/ML Engineer |
| **BRH** |  BODAPATI RAJESH | Backend Developer |
| **MST** | MADATHALA SHIVA TEJA | Frontend Engineer |

---

## 📁 requirements.txt

```
flask
pymongo
bcrypt
groq
requests
```

---

*⚡ AI Code Review & Rewrite Agent — Built with Groq Llama 3.3 70B & Mistral AI · Flask · MongoDB · © 2025*
