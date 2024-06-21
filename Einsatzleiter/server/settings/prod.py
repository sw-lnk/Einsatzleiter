import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

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