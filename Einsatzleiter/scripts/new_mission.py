from mission_log.models import Mission
from users.models import CustomUser
import secrets
import string
import os
from dotenv import load_dotenv
from imap_tools import MailBox, AND
import random

load_dotenv()

alphabet = string.ascii_letters + string.digits

# INSTALLED_APPS = [
#     ...,
#     'django_extensions',
# ]

# pip install django-extensions

# python manage.py runscript script_name


def get_mails() -> list[dict]:
    # Prüfe auf neue Alarmdepeche
    email_address = os.getenv("EMAIL_ADRESSE")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_leitstelle = os.getenv("EMAIL_LEITSTELLE")

    imap_server = os.getenv("IMAP_SERVER")
    imap_port = os.getenv("IMAP_PORT")

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")

    list_mails = []
    with MailBox(imap_server).login(email_address, email_password) as mailbox:
        for msg in mailbox.fetch(AND(from_=email_leitstelle)):
            values = [x.strip() for x in msg.text.split(';')]
            keys = ["main_id", "key_word_short", "city", "ward", "street", "street_no", "fire_alarm_system", "object", "comment", "flashing", "key_word_long", "overview", "units", "time"]
            dic = dict(zip(keys, values))
            dic['date'] = msg.date
            list_mails.append(dic)
    
    return list_mails


def new_mission(msg: dict):
    instance = CustomUser
    try:
        user = instance.objects.get(username="bot")
    except instance.DoesNotExist:
        user = instance.objects.create(
            username="bot",
            password="".join(secrets.choice(alphabet) for _ in range(20)),
            email=os.getenv("EMAIL_ADRESSE"),
            first_name="auto",
            last_name="bot",
        )

    if False:
        Mission.objects.create(
            main_id=random.randint(1_000_000_000, 10_000_000_000),
            keyword="Test: automatische Einsatzanlage",
            street="Musterstraße",
            author=user)
    else:
        Mission.objects.create(
            main_id=int(msg['main_id']),
            keyword=f"{msg['key_word_short']} - {msg['key_word_long']}",
            street=msg['street'],
            street_no=msg['street_no'],
            start=msg['date'],
            author=user)

def run():
    all_mails = get_mails()
    ids = []
    for msg in all_mails:
        if not msg['main_id'] in ids:
            try:
                new_mission(msg)
                ids.append(msg['main_id'])
            except:
                continue

if __name__ == "__main__":
    get_mails()
