from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def env_int(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r)3oy#n_xqo8=kx%^=#@-(4h#wach_j)&hi6supwvf53!w*%5o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'juliaportfolio-production.up.railway.app',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp',
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

ROOT_URLCONF = 'myProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# settings.py
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def env_bool(key: str, default=False):
    return str(os.getenv(key, str(default))).lower() in ("1", "true", "yes", "y", "on")

DB_LIVE = env_bool("DB_LIVE")  # set to 1/true on Railway if you want Postgres

if DB_LIVE:
    # Prefer DATABASE_URL (Railway Postgres). If missing, try manual PG vars. Otherwise, fall back to SQLite.
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        import dj_database_url
        DATABASES = {
            "default": dj_database_url.parse(
                DATABASE_URL, conn_max_age=600, ssl_require=True
            )
        }
    else:
        host = os.getenv("DB_HOST")
        if host:
            DATABASES = {
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": os.getenv("DB_NAME"),
                    "USER": os.getenv("DB_USER"),
                    "PASSWORD": os.getenv("DB_PASSWORD"),
                    "HOST": host,
                    "PORT": os.getenv("DB_PORT", "5432"),
                    "CONN_MAX_AGE": 600,
                    "OPTIONS": {"sslmode": "require"},
                }
            }
        else:
            # Safety net: no PG config found, use SQLite so the app still runs.
            DATABASES = {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                }
            }
else:
    # Local/dev: SQLite—boring and reliable.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Or your preferred path
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")

# Default: TLS on 587 (works for Gmail). Flip to SSL/465 by setting EMAIL_USE_SSL=True.
if env_bool("EMAIL_USE_SSL", False):
    EMAIL_PORT = env_int("EMAIL_PORT", 465)
    EMAIL_USE_SSL = True
    EMAIL_USE_TLS = False
else:
    EMAIL_PORT = env_int("EMAIL_PORT", 587)
    EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
    EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "juliavictorio16@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")  # Gmail App Password
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", f"Julia Victorio <{EMAIL_HOST_USER}>")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", DEFAULT_FROM_EMAIL)  # used by Django for error mails
CONTACT_TO = os.environ.get("CONTACT_TO", "juliavictorio16@gmail.com")
EMAIL_TIMEOUT = env_int("EMAIL_TIMEOUT", 20)

# Where contact messages go:
CONTACT_TO = "juliavictorio16@gmail.com"