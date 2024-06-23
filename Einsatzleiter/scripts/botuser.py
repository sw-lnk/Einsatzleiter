from users.models import CustomUser

import secrets
import string
import os
from dotenv import load_dotenv
load_dotenv()

alphabet = string.ascii_letters + string.digits

# INSTALLED_APPS = [
#     ...,
#     'django_extensions',
# ]

# pip install django-extensions

# python manage.py runscript -v3 script_name

def bot_user() -> CustomUser:
    try:
        user = CustomUser.objects.get(username="bot")
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create(
            username="bot",
            password="".join(secrets.choice(alphabet) for _ in range(20)),
            email=os.getenv("EMAIL_ADRESSE"),
            first_name="auto",
            last_name="bot",
        )
    return user

def run() -> None:
    bot_user()

if __name__ == "__main__":
    print('Nothing will happen. Run the script in a Djang environment.')
