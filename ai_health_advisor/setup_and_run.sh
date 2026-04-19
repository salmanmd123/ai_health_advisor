#!/bin/bash
# ============================================================
#  AI Health Advisor – Setup & Run Script
#  St. Martin's Engineering College – Batch 02
# ============================================================

echo "======================================"
echo "  AI Health Advisor – Setup Script"
echo "======================================"

# 1. Install dependencies
echo ""
echo "[1/3] Installing Python dependencies..."
pip install Django seaborn matplotlib scikit-learn nltk Pillow

# 2. Run migrations
echo ""
echo "[2/3] Setting up database..."
python manage.py makemigrations healthapp
python manage.py migrate

# 3. Start server
echo ""
echo "[3/3] Starting development server..."
echo ""
echo "======================================"
echo "  App running at: http://127.0.0.1:8000"
echo "  Admin Panel:    http://127.0.0.1:8000/admin-login/"
echo "  Admin login:    admin / admin123"
echo "======================================"
echo ""
python manage.py runserver
