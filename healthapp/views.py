from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import json

from .forms import UserRegistrationForm, SymptomInputForm
from .models import UserRegistrationModel, SymptomCheckHistory, AdminRegistrationModel
from .ai_engine import analyze_symptoms, get_symptom_display_name, generate_chart_data


# ─── Utility ──────────────────────────────────────────────────────────────────

def generate_bar_chart(conditions):
    """Use seaborn + matplotlib to generate a match confidence bar chart."""
    if not conditions:
        return None
    try:
        names = [c['name'] for c in conditions]
        scores = [c['score'] for c in conditions]
        colors_map = {'mild': '#27ae60', 'moderate': '#f39c12', 'severe': '#e74c3c'}
        bar_colors = [colors_map.get(c['severity'], '#3498db') for c in conditions]

        fig, ax = plt.subplots(figsize=(7, 3.5))
        sns.set_style('whitegrid')
        bars = ax.barh(names, scores, color=bar_colors, edgecolor='white', linewidth=0.5)

        for bar, score in zip(bars, scores):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f'{score}%', va='center', fontsize=10, fontweight='bold', color='#2c3e50')

        ax.set_xlabel('Match Confidence (%)', fontsize=10, color='#555')
        ax.set_title('Possible Conditions – Confidence Score', fontsize=12,
                     fontweight='bold', color='#2c3e50', pad=10)
        ax.set_xlim(0, 115)
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=130, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception:
        return None


# ─── Public Views ─────────────────────────────────────────────────────────────

def index(request):
    return render(request, 'index.html')


def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered! Please log in.')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.error(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get("loginid")
        password = request.POST.get("pswd")
        print(loginid)
        print(password)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=password)
            status = check.status
            if status == "activated":
                request.session['id'] = check.id
                request.session['loginid'] = check.loginid
                request.session['password'] = check.password
                request.session['email'] = check.email
                request.session['name'] = check.name
                return render(request, 'users/UserHome.html', {'user': check})
            else:
                messages.error(request, "Your account is not activated.")
            return render(request, "UserLogin.html")
        except Exception as e:
            print('=======> ', e)
            messages.error(request, 'Invalid login details. Please try again.')
            return render(request, 'UserLogin.html', {})
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    if 'loginid' not in request.session:
        return redirect('user_login')
    user = get_object_or_404(UserRegistrationModel, loginid=request.session['loginid'])
    recent_checks = SymptomCheckHistory.objects.filter(user=user)[:5]
    return render(request, 'users/UserHome.html', {'user': user, 'recent_checks': recent_checks})


def SymptomCheck(request):
    if 'loginid' not in request.session:
        return redirect('user_login')

    user = get_object_or_404(UserRegistrationModel, loginid=request.session['loginid'])
    result = None
    chart_img = None

    if request.method == 'POST':
        form = SymptomInputForm(request.POST)
        if form.is_valid():
            symptoms_text = form.cleaned_data['symptoms']
            result = analyze_symptoms(symptoms_text)

            # Generate seaborn chart
            if result['conditions']:
                chart_img = generate_bar_chart(result['conditions'])

            # Format symptoms for display
            result['symptoms_display'] = [
                get_symptom_display_name(s) for s in result['detected_symptoms']
            ]

            # Save to history
            conditions_str = ', '.join([c['name'] for c in result['conditions']])
            advice_str = ' | '.join(result['general_advice'])
            detected_str = ', '.join(result['symptoms_display'])

            SymptomCheckHistory.objects.create(
                user=user,
                symptoms_input=symptoms_text,
                detected_symptoms=detected_str,
                possible_conditions=conditions_str or 'No specific conditions detected',
                advice=advice_str,
                severity=result['overall_severity'],
            )
    else:
        form = SymptomInputForm()

    return render(request, 'users/SymptomCheck.html', {
        'form': form,
        'result': result,
        'chart_img': chart_img,
        'user': user,
    })


def UserHistory(request):
    if 'loginid' not in request.session:
        return redirect('user_login')
    user = get_object_or_404(UserRegistrationModel, loginid=request.session['loginid'])
    history = SymptomCheckHistory.objects.filter(user=user)
    return render(request, 'users/UserHistory.html', {'user': user, 'history': history})


def UserProfile(request):
    if 'loginid' not in request.session:
        return redirect('user_login')
    user = get_object_or_404(UserRegistrationModel, loginid=request.session['loginid'])
    profile_fields = [
        ('Full Name', user.name),
        ('Username', user.loginid),
        ('Email Address', user.email),
        ('Mobile Number', user.mobile),
        ('Age', user.age),
        ('Gender', user.gender),
        ('Account Status', user.status.title()),
        ('Member Since', user.created_at.strftime('%B %d, %Y') if user.created_at else 'N/A'),
    ]
    return render(request, 'users/UserProfile.html', {'user': user, 'profile_fields': profile_fields})


def UserLogout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('user_login')


# ─── Admin Views ──────────────────────────────────────────────────────────────

def AdminLogin(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        if loginid == 'admin' and password == 'admin123':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'admin_panel/AdminLogin.html')


def AdminDashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    total_users = UserRegistrationModel.objects.count()
    total_checks = SymptomCheckHistory.objects.count()
    users = UserRegistrationModel.objects.all()

    # Seaborn chart: checks per severity
    try:
        from django.db.models import Count
        severity_data = SymptomCheckHistory.objects.values('severity').annotate(count=Count('id'))
        severities = [d['severity'] for d in severity_data]
        counts = [d['count'] for d in severity_data]
        color_map = {'mild': '#27ae60', 'moderate': '#f39c12', 'severe': '#e74c3c'}
        bar_colors = [color_map.get(s, '#3498db') for s in severities]

        fig, ax = plt.subplots(figsize=(6, 3))
        sns.set_style('whitegrid')
        ax.bar(severities, counts, color=bar_colors, edgecolor='white')
        ax.set_title('Checks by Severity Level', fontsize=11, fontweight='bold')
        ax.set_xlabel('Severity')
        ax.set_ylabel('Number of Checks')
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=120)
        plt.close()
        buf.seek(0)
        severity_chart = base64.b64encode(buf.read()).decode('utf-8')
    except Exception:
        severity_chart = None

    return render(request, 'admin_panel/AdminDashboard.html', {
        'total_users': total_users,
        'total_checks': total_checks,
        'users': users,
        'severity_chart': severity_chart,
    })


def AdminViewChecks(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    checks = SymptomCheckHistory.objects.select_related('user').all()
    return render(request, 'admin_panel/AdminViewChecks.html', {'checks': checks})


def AdminLogout(request):
    request.session.pop('admin_logged_in', None)
    return redirect('admin_login')
