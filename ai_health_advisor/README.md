# 🏥 AI Health Advisor

---

## 📋 Project Overview

AI Health Advisor is an intelligent healthcare web application built using **Django** that analyzes user-provided symptoms and suggests possible medical conditions along with severity levels and general health advice.

The system leverages **Natural Language Processing (NLP)** to process free-text input and uses a **machine learning-inspired scoring approach (Precision, Recall, F1 Score)** to match symptoms with potential diseases. It also provides **data visualizations** using Seaborn and Matplotlib to enhance interpretability.

---

## 🛠️ Tech Stack & Modules

| Module           | Purpose                                          |
| ---------------- | ------------------------------------------------ |
| **Django**       | Backend framework, ORM, authentication, routing  |
| **Seaborn**      | Statistical data visualization (charts & graphs) |
| **Matplotlib**   | Chart rendering for web display                  |
| **scikit-learn** | F1-score based condition matching logic          |
| **NLTK**         | NLP preprocessing (tokenization, normalization)  |
| **SQLite**       | Lightweight database via Django ORM              |

---

## 🚀 Quick Start

### Prerequisites

* Python 3.9+
* pip

### Installation & Run

```bash
# Navigate to project directory
cd ai_health_advisor

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Alternative (Setup Script)

```bash
bash setup_and_run.sh
```

---

## 🌐 Access the Application

* **User Interface:** http://127.0.0.1:8000
* **Admin Panel:** http://127.0.0.1:8000/admin-login/

---

## 📁 Project Structure

```
ai_health_advisor/
├── manage.py
├── requirements.txt
├── setup_and_run.sh
├── ai_health_advisor/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── healthapp/
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── ai_engine.py
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

### 👤 User Features

* User registration and login system
* AI-powered symptom analysis using NLP
* Recognition of 30+ symptoms
* Prediction of 10+ medical conditions
* Confidence scoring using F1-like metric
* Visual charts for condition confidence
* Severity classification (Mild / Moderate / Severe)
* Emergency symptom detection
* Personalized health advice
* Suggested medications (informational only)
* User history tracking
* Quick symptom selection interface

---

### 🛠️ Admin Features

* Secure admin login
* Dashboard with user and activity insights
* Visualization of severity distribution
* User management system
* View all symptom check records

---

## 🧠 AI Engine Details (`ai_engine.py`)

### 🔍 NLP Processing Pipeline

1. Text preprocessing (lowercasing, punctuation removal, normalization)
2. Keyword-based symptom extraction
3. Mapping symptoms to predefined categories
4. Condition scoring using F1-like metric

### 📊 Scoring Logic

* **Precision** = Matched Symptoms / Total Detected Symptoms
* **Recall** = Matched Symptoms / Total Condition Symptoms
* **F1 Score** = 2 × (Precision × Recall) / (Precision + Recall)

### ⚠️ Additional Intelligence

* Severity classification based on condition score
* Emergency detection for critical symptoms
* Ranked list of possible conditions

---

## 🧬 Supported Conditions

* Common Cold
* Influenza
* Gastroenteritis
* Migraine
* Allergic Reaction
* Hypertension
* Anxiety Disorder
* Urinary Tract Infection (UTI)
* Back Pain
* Depression

---

## ⚠️ Disclaimer

This application is intended for **educational and informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

## 📌 Future Enhancements

* Integration with real medical datasets
* Machine learning model for improved accuracy
* Chatbot-based interaction
* Mobile application version
* Doctor consultation integration

---
