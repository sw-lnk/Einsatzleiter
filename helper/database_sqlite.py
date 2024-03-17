import os

import sqlite3
from scripts.einheit import Einheit

# Sammlung aller Funktion zur interaktion mit Datenbanken

## Erstelle und verbinde eine lokale SQLite-Datenbank für alle Einsatzstellen
def verbinde_datenbank_sqlite_einsatzstellen(ordnername: str = 'data') -> sqlite3.Connection:
    db = sqlite3.connect(os.path.join(ordnername, 'db.sqlite3'))
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS einsatzstellen(
            _id INTEGER PRIMARY KEY NOT NULL,
            einsatznr TEXT NOT NULL,
            stichwort TEXT,
            anschrift TEXT,
            status TEXT,
            datum TIMESTAMP,
            letztes_update TIMESTAMP,
            archiv INTEGER
        )
    ''')
    db.commit()
    return db

## Erstelle und verbinde eine lokale SQLite-Datenbank für alle Einheiten
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

## Einfügen oder aktualisieren einer Einheit in der SQLite-Datenbank
def schreibe_einheit_sqlite(einheit: Einheit, db: sqlite3.Connection) -> None:
    cursor = db.cursor()
    cursor.execute('''INSERT OR REPLACE INTO einheiten(funkrufname, vf, zf, gf, ms, agt, anmerkung, datum) VALUES(?,?,?,?,?,?,?,?)''', einheit.einheit_als_tuple())
    db.commit()

# Funktion die ausgeführt wird, wenn die Datei einzeln verwendet wird
if __name__ == "__main__":
    print('Funktionen zum Aufbau einer SQLite-Datenbankverbindung.')