from mission_log.models import Mission
from users.models import CustomUser

import secrets
import string
import os
from dotenv import load_dotenv
from imap_tools import MailBox, AND
import random
import requests
import datetime

load_dotenv()

alphabet = string.ascii_letters + string.digits

# INSTALLED_APPS = [
#     ...,
#     'django_extensions',
# ]

# pip install django-extensions

# python manage.py runscript -v3 script_name

def get_mails() -> list[dict]:
    email_address = os.getenv("EMAIL_ADRESSE")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_leitstelle = os.getenv("EMAIL_LEITSTELLE")

    imap_server = os.getenv("IMAP_SERVER")
    imap_port = os.getenv("IMAP_PORT")

    list_mails = []
    with MailBox(imap_server, imap_port).login(email_address, email_password) as mailbox:
        for msg in mailbox.fetch(AND(from_=email_leitstelle)):
            values = [x.strip() for x in msg.text.split(';')]
            keys = ["main_id", "key_word_short", "city", "ward", "street", "street_no", "fire_alarm_system", "object", "comment", "flashing", "key_word_long", "overview", "units", "time"]
            dic = dict(zip(keys, values))
            dic['units'] = [e.strip() for e in dic['units'].split(',')]
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
        
def send_to_telegram(msg) -> None:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_GROUP_ID = os.getenv("GROUP_CHAT_ID")
    
    year = datetime.datetime.now().year
    deadline = datetime.datetime(year, 1, 1, 0, 0)
    
    cnt = Mission.objects.filter(start__gte = deadline).count()
    
    content = f"🚨 {cnt} / {year}\n📟 {msg['key_word_long']}\n"

    if "Alarmdruck" in msg['subject']:
        content += f"⏰ {msg['date'].strftime('%d.%m.%Y %H:%M')}\n"
    else:
        content += f"⏰ {msg['subject'].strftime('%d.%m.%Y')}\n"

    content += f"📍 {msg['street']}"
    if msg['street_no']:
        content += f" {msg['street_no']}"
    content += f", {msg['ward']}\n"

    if msg['overview']:
        content += f"ℹ️ {msg['overview']}\n"

    if msg['comment']:
        content += f"ℹ️ {msg['comment']}\n🚒 "
    else:
        content += f"🚒 "

    content += ", ".join(msg['units'])
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_GROUP_ID}&text={content}"
    requests.get(url).json()

def create_or_upate_mission(msg) -> None:
    if not check_mission_excist(msg):
        # Neuen Einsatz anlegen wenn eine Alarmdepeche eingeht.
        try:
            new_mission(msg)
            send_to_telegram(msg)
        except: pass
    elif ('Abschlußbericht' in msg['subject']):
        # Einsatz aktualisieren wenn die Abschlussdepeche zugestellt wird.
        update_mission_end(msg)

def run() -> None:
    all_mails = get_mails()
    for msg in all_mails:
        create_or_upate_mission(msg)

if __name__ == "__main__":
    print('Nothing will happen. Run the script in a Djang environment.')
