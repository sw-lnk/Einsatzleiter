import os

from .base import BASE_DIR, STATIC_URL, MEDIA_URL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
ALLOWED_HOSTS.append(os.environ.get("DEVICE_IP"))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# STATICFILES_DIRS = [ os.path.join('usr', 'src', 'app', STATIC_URL) ]
STATIC_ROOT = os.path.join('usr', 'src', 'app', 'staticfiles')
MEDIA_ROOT = os.path.join('usr', 'src', 'app', 'mediafiles')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DB_NAME = os.environ.get("DB_NAME")
DB_USER_NM = os.environ.get("DB_USER_NM")
DB_USER_PW = os.environ.get("DB_USER_PW")
DB_IP = os.environ.get("DB_IP")
DB_PORT = os.environ.get("DB_PORT")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER_NM,
        "PASSWORD": DB_USER_PW,
        "HOST": DB_IP,
        "PORT": DB_PORT,
    }
}

CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']
CSRF_TRUSTED_ORIGINS.append(f'http://{os.environ.get("DEVICE_IP")}:1337')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = os.environ.get("SMTP_SERVER")
EMAIL_PORT = os.environ.get("SMTP_PORT")
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_ADRESSE")
EMAIL_HOST_USER = os.environ.get("EMAIL_ADRESSE")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
