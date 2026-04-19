# 🏥 AI Health Advisor

**St. Martin's Engineering College – Department of AI & ML**  
**Batch 02** | A. Sravani (23K81A7302), A. Sai Prasad (23K81A7305), MD. Salman (23K81A7336)  
**Guide:** Mr. M. Rajaram, Assistant Professor

---

## 📋 Project Overview

An intelligent healthcare web application built with **Django** that provides health advice based on symptoms described by the user. The system uses **Natural Language Processing (NLP)** to analyze symptom input, **machine learning-inspired scoring** (Precision, Recall, F1) to match conditions, and **Seaborn/Matplotlib** for data visualization.

---

## 🛠️ Tech Stack & Modules

| Module | Purpose |
|--------|---------|
| **Django** | Web framework, ORM, session management, forms |
| **Seaborn** | Statistical data visualization (confidence charts, severity graphs) |
| **Matplotlib** | Backend for generating PNG charts embedded in pages |
| **scikit-learn** | F1-score based symptom-condition matching |
| **NLTK** | NLP preprocessing (tokenization, text normalization) |
| **SQLite** | Database via Django ORM |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation & Run

```bash
# 1. Navigate to project directory
cd ai_health_advisor

# 2. Install dependencies
pip install Django seaborn matplotlib scikit-learn nltk Pillow

# 3. Run migrations
python manage.py makemigrations healthapp
python manage.py migrate

# 4. Start the server
python manage.py runserver
```

OR just run the setup script:
```bash
bash setup_and_run.sh
```

### Access the App
- **User App:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin-login/
  - Username: `admin` | Password: `admin123`

---

## 📁 Project Structure

```
ai_health_advisor/
├── manage.py
├── requirements.txt
├── setup_and_run.sh
├── ai_health_advisor/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── healthapp/                  # Main application
    ├── models.py               # UserRegistrationModel, SymptomCheckHistory
    ├── forms.py                # UserRegistrationForm, SymptomInputForm
    ├── views.py                # All view functions
    ├── urls.py                 # URL routing
    ├── ai_engine.py            # NLP + AI analysis engine
    ├── templatetags/
    │   └── custom_filters.py
    └── templates/
        ├── base.html
        ├── index.html
        ├── UserRegistrations.html
        ├── UserLogin.html
        ├── users/
        │   ├── UserHome.html
        │   ├── SymptomCheck.html
        │   ├── UserHistory.html
        │   └── UserProfile.html
        └── admin_panel/
            ├── AdminLogin.html
            ├── AdminDashboard.html
            └── AdminViewChecks.html
```

---

## ✨ Features

### User Features
- ✅ User Registration & Login with session management
- ✅ AI-powered symptom checker (NLP-based)
- ✅ 30+ symptom keywords recognized
- ✅ 10+ disease/condition profiles
- ✅ Confidence scoring using F1-like metric (Precision × Recall)
- ✅ Seaborn bar charts showing condition match confidence
- ✅ Severity assessment (Mild 🟢 / Moderate 🟡 / Severe 🔴)
- ✅ Emergency symptom detection
- ✅ Detailed health advice per condition
- ✅ Suggested medications (informational only)
- ✅ Health check history tracking
- ✅ Quick-select symptom chips on the checker page

### Admin Features
- ✅ Admin login portal
- ✅ Dashboard with total user/check counts
- ✅ Seaborn chart: checks grouped by severity
- ✅ Full user management table
- ✅ View all symptom check records

---

## 🧠 AI Engine Details (`ai_engine.py`)

### NLP Processing
1. **Text Preprocessing** — lowercase, remove punctuation, normalize whitespace
2. **Keyword Extraction** — matches 30+ symptom keywords to 30 symptom categories
3. **Condition Scoring** — computes F1-like score:
   - **Precision** = matched symptoms / total detected symptoms
   - **Recall** = matched symptoms / total disease symptoms
   - **F1 Score** = 2 × (P × R) / (P + R)
4. **Severity Assignment** — based on top matched condition
5. **Emergency Detection** — flags chest pain, shortness of breath, bleeding, etc.

### Conditions Database
- Common Cold, Influenza, Gastroenteritis
- Migraine, Allergic Reaction
- Hypertension, Anxiety Disorder
- UTI, Back Pain, Depression

---

## ⚠️ Medical Disclaimer

This application is for **educational and informational purposes only**. It does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

*Developed as part of the AI & ML curriculum at St. Martin's Engineering College, Secunderabad.*
