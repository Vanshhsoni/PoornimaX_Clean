from pathlib import Path
import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
USE_CLOUDINARY=True

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://neondb_owner:npg_bGguxX0VRQ7w@ep-shiny-salad-admgmfak-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=dhol8imhb
CLOUDINARY_API_KEY=616112266455922
CLOUDINARY_API_SECRET=LVW7RCMdSQzSFQHrP5di_K58p4w

# Email Configuration
EMAIL_HOST_USER=sonivanshmaster@gmail.com
EMAIL_HOST_PASSWORD=geid mgxd obrn mubh
DEFAULT_FROM_EMAIL=sonivanshmaster@gmail.com

# Redis (for production channel layers - optional)
# REDIS_URL=redis://localhost:6379
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-ll(dkrpdb5wrj+#(zvmhz=a9c*a84%$#!34ib$9ymj6o2i8tzh')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']

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
    'cloudinary_storage',  # Add this for Cloudinary
    'cloudinary',          # Add this for Cloudinary
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'poornimax.wsgi.application'

# Database Configuration
# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Production database (PostgreSQL via Neon)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Cloudinary Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', 'dhol8imhb'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', '616112266455922'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', 'LVW7RCMdSQzSFQHrP5di_K58p4w'),
}

# Configure cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# Media files configuration
# Use Cloudinary for media files in production
if os.getenv('USE_CLOUDINARY', 'False').lower() == 'true':
    # Production: Use Cloudinary for media files
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
else:
    # Development: Use local storage
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(Path.home(), 'PoornimaX')  # Save to ~/PoornimaX folder

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'sonivanshmaster@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'geid mgxd obrn mubh')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'sonivanshmaster@gmail.com')

# Django Channels Configuration
ASGI_APPLICATION = 'poornimax.asgi.application'

# Channel layers configuration
# Use Redis in production, InMemory in development
REDIS_URL = os.getenv('REDIS_URL')

if REDIS_URL:
    # Production: Use Redis for channel layers
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
else:
    # Development: Use InMemory channel layer
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

# File locking workaround for SQLite
from django.core.files import locks

def dummy_lock(f, flags):
    pass

def dummy_unlock(f):
    pass

locks.lock = dummy_lock
locks.unlock = dummy_unlock

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
