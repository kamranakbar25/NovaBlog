import os
from pathlib import Path

# File: novablog/settings.py

import os
from pathlib import Path
import dj_database_url # <--- ADD THIS
from dotenv import load_dotenv # <--- ADD THIS

load_dotenv() # .env file load karega

BASE_DIR = Path(__file__).resolve().parent.parent

# Yahan hum SECRET_KEY ko Environment Variable se uthayenge
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_insecure_key') # default key sirf local ke liye

# DEBUG aur ALLOWED_HOSTS ko production ke liye set karein
DEBUG = os.environ.get('DEBUG', 'True') == 'True' # Live par False hoga
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-app-name.onrender.com', '.render.com'] # <--- ADD/UPDATE THIS



BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-change-this-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom Apps
    'core',
    'blog',
    'accounts',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'novablog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Global templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'novablog.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'
LOGIN_URL = 'accounts:login'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'novablog.contact@gmail.com'
EMAIL_HOST_PASSWORD = 'uoce mpwc ysbe ovyx'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (User uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# File: novablog/settings.py

import os
from pathlib import Path
import dj_database_url # <--- ADD THIS
from dotenv import load_dotenv # <--- ADD THIS

load_dotenv() # .env file load karega

BASE_DIR = Path(__file__).resolve().parent.parent

# Yahan hum SECRET_KEY ko Environment Variable se uthayenge
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_insecure_key') # default key sirf local ke liye

# DEBUG aur ALLOWED_HOSTS ko production ke liye set karein
DEBUG = os.environ.get('DEBUG', 'True') == 'True' # Live par False hoga
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.onrender.com'] # <--- ADD/UPDATE THIS


# File: novablog/settings.py

# ... baaki settings ...

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Live par files yahan collect honge
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files ke liye
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Whitenoise compression
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}