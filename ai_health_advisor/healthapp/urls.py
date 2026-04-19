from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.index, name='index'),
    path('register/', views.UserRegisterActions, name='user_register'),
    path('login/', views.UserLoginCheck, name='user_login'),
    path('logout/', views.UserLogout, name='user_logout'),

    # User area
    path('home/', views.UserHome, name='user_home'),
    path('symptom-check/', views.SymptomCheck, name='symptom_check'),
    path('history/', views.UserHistory, name='user_history'),
    path('profile/', views.UserProfile, name='user_profile'),

    # Admin area
    path('admin-login/', views.AdminLogin, name='admin_login'),
    path('admin-dashboard/', views.AdminDashboard, name='admin_dashboard'),
    path('admin-checks/', views.AdminViewChecks, name='admin_checks'),
    path('admin-logout/', views.AdminLogout, name='admin_logout'),
]
