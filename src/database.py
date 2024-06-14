import os
from typing import Union
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

from base import Base
from einstellungen import lese_einstellungen
from einheit import Einheit
from einsatzstelle import Einsatzstelle
from eintrag import Eintrag

# Sammlung aller Funktion zur interaktion mit Datenbanken

## Erstelle ein SQL-Alchemy Engine lokal oder remote
def get_engine() -> Engine:
    einstellungen = lese_einstellungen()
    if einstellungen['einzelplatznutzung']:
        if not os.path.exists('data'):
            # Erstelle einen Ordner, falls dieser nicht existiert
            os.makedirs('data')
        
        engine = create_engine("sqlite:///data/sqlite.db", echo=False)
    else:        
        user = einstellungen['db_user']
        pwd = einstellungen['db_user_password']
        db_name = einstellungen['db_name']
        host = einstellungen['db_ip']
        port = einstellungen['db_port']
        
        url = f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}'
        
        if not database_exists(url):
            create_database(url)
        
        engine = create_engine(url=url, echo=False)
    
    return engine

## Erstelle eine SQL-Alchemy Session
def get_session(engine: Engine) -> Session:
    Session = sessionmaker(bind=engine)
    return Session()

## Erstelle alle Tabellen, falls nicht vorhanden
def create_table(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)

## Verbinde die Datenbank
def verbinde_datenbank() -> Session:
    engine = get_engine()
    session = get_session(engine)
    create_table(engine)
    return session

## Einfügen einer Einheit oder Einsatzstelle in die Datenbank
def schreibe_in_datenbank(daten: Union[Einsatzstelle, Einheit, Eintrag], session: Session) -> None:
    session.add(daten)
    session.commit()

## Lese alle Daten zu Einheiten aus der Datenbank
def lese_datenbank_einheiten(session: Session) -> list[Einheit]:
    return session.query(Einheit).all()

## Lese alle Daten zu Einheiten aus der Datenbank
def lese_datenbank_einsatzstellen(session: Session) -> list[Einsatzstelle]:
    return session.query(Einsatzstelle).all()

# Funktion die ausgeführt wird, wenn die Datei einzeln verwendet wird
if __name__ == "__main__":
    print('Funktionen zum Aufbau einer Datenbankverbindung.')
