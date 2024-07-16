from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import load_dotenv
load_dotenv()

import requests
from datetime import datetime
from imap_tools import MailBox, AND
from dateutil import tz

time_zone = tz.gettz("Europe/Berlin")

Base = declarative_base()
class Mission(Base):
    __tablename__ = "mission_log_mission"
    ZIP_CODE = os.getenv("ZIP_CODE")
    
    UNTREATED = '0'
    PROCESSING= '1'
    CLOSED = '2'
    
    STATUS_CHOICES=(
        (UNTREATED, 'unbearbeitet'),
        (PROCESSING, 'in Arbeit'),
        (CLOSED, 'abgeschlossen')
    )

    HIGH = '1'
    MEDIUM = '2'
    LOW = '3'

    PRIO_CHOICES=(
        (HIGH, 'hoch'),
        (MEDIUM, 'mittel'),
        (LOW, 'niedrig'),
    )
    
    main_id=Column(Integer(), primary_key=True)
    keyword=Column(String(100), nullable=False)
    street=Column(String(100), nullable=False)
    street_no=Column(String(10), nullable=True)
    zip_code=Column(String(5), nullable=True, default=ZIP_CODE)
    
    status=Column(String(15), nullable=False, default=UNTREATED)
    prio=Column(String(15), nullable=False, default=MEDIUM)
    
    start=Column(DateTime(), default=datetime.now())
    end=Column(DateTime(), nullable=True)
    
    creation=Column(DateTime(timezone=True), default=datetime.now())
    last_update=Column(DateTime(timezone=True), default=datetime.now())
    
    
    archiv=Column(Boolean(), default=False, nullable=False)
    
    author_id=Column(Integer(), default=1)
    
    def address(self) -> str:
        a = self.street
        if self.street_no:
            a += f' {self.street_no}'
        if self.zip_code:
            a += f', {self.zip_code}'
        return a
    
    def auto_entry(self) -> str:
        for k, v in self.STATUS_CHOICES:
            if k == self.status:
               status_value = v
        
        for k, v in self.PRIO_CHOICES:
            if k == self.prio:
               prio_value = v
        
        return f'{self.keyword}, Status: {status_value}, Prio: {prio_value} - {self.address()}'


class Entry(Base):    
    __tablename__ = "mission_log_entry"
    id=Column(Integer(), primary_key=True)
    text = Column(Text(), nullable=False)
    sender = Column(String(100), default='')
    recipient = Column(String(100), default='')
    
    time = Column(DateTime(), default=datetime.now())
    author_id = Column(Integer(), default=1)
    mission_id = Column(Integer(), nullable=False)
    
    def __str__(self):
        return f"{self.time.strftime('%d.%m.%Y %H:%M')}: {self.text}"


if os.getenv("PIPELINE"):
    url = URL.create(
        drivername="postgresql",
        username=os.getenv("POSTGRES_USER"),
        host=os.getenv("DEVICE_IP"),
        database=os.getenv("POSTGRES_DB"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    engine = create_engine(url)
else:
    engine = create_engine('sqlite:///db.sqlite3')
    
Session = sessionmaker(bind=engine)
session = Session()

email_address = os.getenv("EMAIL_ADRESSE")
email_password = os.getenv("EMAIL_PASSWORD")
email_leitstelle = os.getenv("EMAIL_LEITSTELLE")
imap_server = os.getenv("IMAP_SERVER")
imap_port = os.getenv("IMAP_PORT")


def all_mission() -> list[Mission]:
    return session.query(Mission).all()


def get_mails() -> list[dict]:
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


def clear_inbox() -> None:    
    with MailBox(imap_server, imap_port).login(email_address, email_password) as mailbox:
        list_mails = [msg.uid for msg in mailbox.fetch()]
        mailbox.delete(list_mails)
        

def check_mission_excist(msg) -> bool:
    try: return session.query(Mission).filter(Mission.main_id == msg['main_id']).count()
    except Exception as e: print('...Error message:', e)


def new_mission(msg: dict) -> None:
    new_mission = Mission()
    new_mission.main_id = msg['main_id']
    new_mission.keyword = f"{msg['key_word_short']} - {msg['key_word_long']}"
    new_mission.street = msg['street']
    new_mission.street_no = msg['street_no']
    new_mission.start = msg['date']
    new_mission.status = new_mission.UNTREATED
    new_mission.prio = new_mission.MEDIUM

    entry = Entry()
    entry.text = f"Automatisch erstellt: {new_mission.auto_entry()}"
    entry.time = msg['date']
    entry.author_id = new_mission.author_id
    entry.mission_id = new_mission.main_id
    
    session.add(new_mission)
    session.add(entry)
    session.commit()


def update_mission_end(msg) -> None:
    if not check_mission_excist(msg):
        return
    
    mission = session.query(Mission).filter(Mission.main_id == msg['main_id']).first()
    
    if mission.end:
        return
    
    mission.end = msg['date']
    mission.status = mission.CLOSED
    
    entry = Entry()
    entry.text = f"Automatisch erstellt: {mission.auto_entry()}"
    entry.time = msg['date']
    entry.author_id = mission.author_id
    entry.mission_id = mission.main_id
    session.add(entry)
    
    session.commit()


def send_to_telegram(msg) -> None:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_GROUP_ID = os.getenv("GROUP_CHAT_ID")
    
    year = datetime.now().year
    deadline = datetime(year, 1, 1, 0, 0)
    
    cnt = session.query(Mission).filter(Mission.start > deadline).count()
    
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
        except Exception as e: print('...Error message:', e)
    elif ('Abschlußbericht' in msg['subject']):
        # Einsatz aktualisieren wenn die Abschlussdepeche zugestellt wird.
        try: update_mission_end(msg)
        except Exception as e: print('...Error message:', e)


def delete_mission(main_id: int) -> None:
    mission = session.query(Mission).filter(Mission.main_id == main_id).first()
    session.delete(mission)
    session.commit()


def main() -> None:
    all_mails = get_mails()
    for msg in all_mails:
        create_or_upate_mission(msg)
    session.close()
    clear_inbox()


def main_plus() -> None:
    print('Script is running.')
    start = datetime.now()
    main()
    duration = datetime.now() - start
    print(f"Finished script after {duration.seconds:.1f}s.")

   
if __name__ == "__main__":
    main()
    