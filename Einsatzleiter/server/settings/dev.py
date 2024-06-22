from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-pnxcsdqt#*edu21fs^c4d840sj*9r_#ym9mu@#0m%$ffiasg32"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# This logs any emails sent to the console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"