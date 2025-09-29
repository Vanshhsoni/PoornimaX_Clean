from pathlib import Path
import os
import dj_database_url
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-ll(dkrpdb5wrj+#(zvmhz=a9c*a84%$#!34ib$9ymj6o2i8tzh'
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "https://poornimax.onrender.com",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    'poornima_site',
    'accounts',
    'feed',
    'chat',
    'django.contrib.humanize',
    'channels',
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.sitemaps'
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

ROOT_URLCONF = 'poornimax.urls'
WSGI_APPLICATION = 'poornimax.wsgi.application'
ASGI_APPLICATION = 'poornimax.asgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ------------------------
# DATABASE (PostgreSQL Neon)
# ------------------------
DATABASES = {
    "default": dj_database_url.parse(
        os.getenv('DATABASE_URL', 
            "postgresql://neondb_owner:npg_bGguxX0VRQ7w@ep-shiny-salad-admgmfak-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        ),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Add to your settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'chat.consumers': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ------------------------
# CLOUDINARY CONFIGURATION
# ------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dhol8imhb',
    'API_KEY': '616112266455922',
    'API_SECRET': 'LVW7RCMdSQzSFQHrP5di_K58p4w',
}

# Configure cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# ------------------------
# MEDIA FILES (Cloudinary)
# ------------------------
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # For local development fallback

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sonivanshmaster@gmail.com'
EMAIL_HOST_PASSWORD = 'mwtz lmiw rwuk ubkg'
DEFAULT_FROM_EMAIL = 'sonivanshmaster@gmail.com'

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
