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

# python manage.py runscript -v3 script_name

def get_mails() -> list[dict]:
    # Prüfe auf neue Alarmdepeche
    email_address = os.getenv("EMAIL_ADRESSE")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_leitstelle = os.getenv("EMAIL_LEITSTELLE")

    imap_server = os.getenv("IMAP_SERVER")
    imap_port = os.getenv("IMAP_PORT")

    list_mails = []
    with MailBox(imap_server).login(email_address, email_password, imap_port) as mailbox:
        for msg in mailbox.fetch(AND(from_=email_leitstelle)):
            values = [x.strip() for x in msg.text.split(';')]
            keys = ["main_id", "key_word_short", "city", "ward", "street", "street_no", "fire_alarm_system", "object", "comment", "flashing", "key_word_long", "overview", "units", "time"]
            dic = dict(zip(keys, values))
            dic['date'] = msg.date
            dic['subject'] = msg.subject
            
            dic['main_id'] = int(dic['main_id'])
            
            list_mails.append(dic)
    
    return list_mails

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

def check_mission_excist(msg) -> bool:
    return Mission.objects.filter(main_id=msg['main_id']).exists()

def new_mission(msg: dict) -> None:
    user = bot_user()    

    if False:
        Mission.objects.create(
            main_id=random.randint(1_000_000_000, 10_000_000_000),
            keyword="Test: automatische Einsatzanlage",
            street="Musterstraße",
            author=user)
    else:
        Mission.objects.create(
            main_id=msg['main_id'],
            keyword=f"{msg['key_word_short']} - {msg['key_word_long']}",
            street=msg['street'],
            street_no=msg['street_no'],
            start=msg['date'],
            author=user)

def update_mission_end(msg) -> None:
    if not check_mission_excist(msg):
        return
    
    mission = Mission.objects.get(main_id=msg['main_id'])
    
    if mission.end:
        return
    
    mission.end = msg['date']
    mission.status = mission.CLOSED
    mission.save()

def create_or_upate_mission(msg) -> None:
    # print(msg['subject'])
    if not check_mission_excist(msg):
        # Neuen Einsatz anlegen wenn eine Alarmdepeche eingeht.
        try:
            new_mission(msg)
        except: pass # Log-Eintrag erzeugen bei einem Error
    elif ('Abschlußbericht' in msg['subject']):
        # Einsatz aktualisieren wenn die Abschlussdepeche zugestellt wird.
        update_mission_end(msg)

def run():
    for msg in get_mails():
        create_or_upate_mission(msg)

if __name__ == "__main__":
    print('Nothing will happen.')
