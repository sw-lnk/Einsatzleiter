import os

from pymongo import ReturnDocument, MongoClient
from pymongo.database import Database
from datetime import datetime
from scripts.einheit import Einheit

# Sammlung aller Funktion zur interaktion mit Datenbanken

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

## Lese alle Daten zu Einheiten aus einer MongoDB-Datenbank
def lese_datenbank_mongo_einheiten(database: Database) -> list[dict]:
    alle_einheiten = database.krafte.find()  
    return alle_einheiten

## Prüfe ob ein Update bei den Einheiten in der MongoDB-Datenbank vorliegt
def check_update_einheiten(database: Database, letztes_update: datetime) -> bool:
    cnt = database.krafte.count_documents({'datum': {'$gt': letztes_update}})
    if cnt > 0:
        return True
    else:
        return False

## Prüfe ob ein Update bei den Einsatzstellen in der MongoDB-Datenbank vorliegt
def check_update_einsatzstellen(database: Database, letztes_update: datetime) -> bool:
    cnt = database.einsatzstellen.count_documents({'letztes_update': {'$gt': letztes_update}})
    if cnt > 0:
        return True
    else:
        return False

## Einfügen oder aktualisieren einer Einheit in der MongoDB-Datenbank
def schreibe_einheit_mongo(einheit: Einheit, db: Database) -> None:
    funk = einheit.funkrufname
    cnt = db.krafte.count_documents({"funkrufname": funk})
    if cnt>0:
        db.krafte.find_one_and_update(
                {'funkrufname': funk}, {'$set': einheit.einheit_als_dict()}, 
                return_document = ReturnDocument.AFTER
            )
    else:
        db.krafte.insert_one(einheit)

# Funktion die ausgeführt wird, wenn die Datei einzeln verwendet wird
if __name__ == "__main__":
    print('Funktionen zum Aufbau einer MongoDB-Datenbankverbindung.')