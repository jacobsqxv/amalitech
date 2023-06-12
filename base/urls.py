from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    # password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    # password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # user registration
    path('register/', views.register, name="register"),

    # access keys generation
    path('generate-access-key/', GenerateAccessKeyView.as_view(), name='access_key_form'),
    # path('generate-access-key/', views.generate_access_key, name='access_key_form'),
    path('access-keys/', AccessKeyView.as_view(), name='access_keys'),

    # admin
    path('admin_login/', auth_views.LoginView.as_view(template_name = 'registration/admin_login.html'), name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('revoke_access_key/<str:pk>/', views.revoke_access_key, name='revoke_access_key'),

    # endpoint
    path('api/check-school-email/', check_school_email, name='check_school_email'),
    path('endpoint/', endpoint_view, name='endpoint'),

]