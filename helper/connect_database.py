import os

from pymongo import ReturnDocument, MongoClient
from pymongo.database import Database
import sqlite3

# Sammlung aller Funktion zur interaktion mit Datenbanken

## Erstelle und verbinde eine lokale SQLite-Datenbank
def verbinde_datenbank_sqlite_einheiten(ordnername: str = 'data') -> sqlite3.Connection:
    db = sqlite3.connect(os.path.join(ordnername, 'db.sqlite3'))
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS einheiten(
            funkrufname TEXT PRIMARY KEY,
            vf INTEGER,
            zf INTEGER,
            gf INTEGER,
            ms INTEGER,
            agt INTEGER,
            anmerkung TEXT,
            datum TEXT
        )
    ''')
    db.commit()
    return db

## Verbindung zu einer MongoDB-Datenbank aufbauen
def verbinde_datenbank_mongo(
    nutzername: str,
    passwort: str,
    ip: str = 'localhost',
    port: str = '27017',
    db_name: str = 'einsatzleitung'
    ) -> Database:
    client = MongoClient(f"mongodb://{nutzername}:{passwort}@{ip}:{port}/{db_name}")
    db = client[db_name]
    return db

## Lese alle Daten zu Einheiten aus einer SQLite-Datenbank
def lese_datenbank_sqlite_einheiten(connection: sqlite3.Connection) -> list[dict]:
    alle_einheiten_tuple = connection.cursor().execute('''SELECT * FROM einheiten''').fetchall()
    alle_einheiten = [
        dict(zip((
            'funkrufname',
            'vf',
            'zf',
            'gf',
            'ms',
            'agt',
            'anmerkung',
            'datum'), einheit)) for einheit in alle_einheiten_tuple
    ]    
    return alle_einheiten

## Lese alle Daten zu Einheiten aus einer MongoDB-Datenbank
def lese_datenbank_mongo_einheiten(database: Database) -> list[dict]:
    alle_einheiten = database.krafte.find()  
    return alle_einheiten


# Funktion die ausgeführt wird, wenn die Datei einzeln verwendet wird
if __name__ == "__main__":
    print('Funktionen zum Aufbau einer Datenbankverbindung.')