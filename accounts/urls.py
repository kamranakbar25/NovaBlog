from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

app_name = 'accounts'

urlpatterns = [
    # Login View (Django ka bana-banaya view use karenge)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=UserLoginForm), name='login'),
    
    # Logout View
    path('logout/', views.logout_view, name='logout'),
    
    # Register View (Custom view jo humne views.py mein banaya hai)
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    
    # Profile View
    path('profile/', views.profile, name='profile'),
    path('u/<str:username>/', views.public_profile, name='public_profile'),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]