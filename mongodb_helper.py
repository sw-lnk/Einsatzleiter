from pymongo import MongoClient
from datetime import datetime
import random
from bson import ObjectId

user = 'user' #input('Username: ')
pwd = 'user' #getpass('Password: ')
ip = '192.168.178.41'
port = '27017'
db = 'einsatztagebuch'

client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")

db = client.einsatztagebuch

einsatzstellen = db.einsatzstellen
eintrage = db.eintrage
krafte = db.krafte

# Zufällige Einsatznummer
no = random.randint(1, 123456789)

# Aktueller Zeitpunkt
jetzt = datetime.now()

# Zufällige Anschrift
anschrift = random.choice(
    ['Marktplatz, 12345 Musterstadt', 'Großestraße, 12345 Musterstadt', 'Hauptstraße, 12345 Musterstadt', 'Nebenstraße, 12345 Musterstadt', 'BAB', 'Langestr., 12345 Musterstadt', 'Baumallee, 12345 Musterstadt']
)

# Zufälliges Einsatzstichwort
stichwort = random.choice(
    ['TH0 - Baum auf Straße', 'B0 - Gelöschtes Feuer', 'TH1 - Baum auf PKW', 'CBRN1 - Ölspur', 'TH1 - Laufen Betriebsmittel', 'B1 - Brennt Mülleimer']
)


# Zeige alle Einträge
# for einsatz in einsatzstellen.find():
#     print(einsatz)

# Zeige alle Einträge
# for eintrag in eintrage.find():
#     print(eintrag)


# Einen Einsatz anlegen
einsatz = einsatzstellen.insert_one({
    'nr_lst': no,
    'stichwort': stichwort,
    'anschrift': anschrift,
    'status': 'unbearbeitet',
    'datum': jetzt,
    'letztes_update': jetzt,
    'archiv': False
})

eintrage.insert_one({
    'einsatz': ObjectId(einsatz.inserted_id),
    'zeitstempel': jetzt,
    'eintrag': f'Einsatz neu: {stichwort}, {anschrift} (unbearbeitet) - {no}',
    'absender': '',
    'empfanger': '',
    'bearbeiter': 'Max Mustermann'
})

krafte.insert_one({
    'funkrufname': '2 HLF20 1',
    'vf': 1,
    'zf': 2,
    'gf': 0,
    'ms': 6,
    'anmerkung': 'Einsatzbereit Feuerwehrhaus LE2',
    'datum': jetzt
})

# Mehrer Beispiel Einsätze anlegen
# for i in range(5):
#     einsatz = einsatzstellen.insert_one({
#         'nr_lst': no,
#         'stichwort': stichwort,
#         'anschrift': anschrift,
#         'status': 'unbearbeitet',
#         'datum': jetzt,
#         'archiv': False
#     })
    
#     eintrage.insert_one({
#     'einsatz': einsatz,
#     'zeitstempel': jetzt,
#     'eintrag': f'Einsatz neu: {stichwort}, {anschrift} (unbearbeitet) - {no}',
#     'absender': '',
#     'empfanger': '',
#     'bearbeiter': 'Max Mustermann'
#     })

# Alle Einsatzstellen aus Datenbank löschen
# einsatzstellen.delete_many({})
# eintrage.delete_many({})
# krafte.delete_many({})
