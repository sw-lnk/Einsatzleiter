from pymongo import MongoClient
from bson import ObjectId
from getpass import getpass
from datetime import datetime
import time
import random

user = 'user' #input('Username: ')
pwd = 'user' #getpass('Password: ')
ip = '192.168.178.41'
port = '27017'
db = 'einsatztagebuch'

client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")

db = client.einsatztagebuch

einsatzstellen = db.einsatzstellen
updates = db.updates

alle_einsatzstellen = einsatzstellen.find()

# for est in alle_einsatzstellen:
#     print(est)

# test_liste = [[datetime.now(), 'Test', '', '', 'Max Mustermann'] for x in range(20)]
no = random.randint(1, 123456789)
jetzt = datetime.now()
anschrift = random.choice(
    ['Marktplatz, 12345 Musterstadt', 'Großestraße, 12345 Musterstadt', 'Hauptstraße, 12345 Musterstadt', 'Nebenstraße, 12345 Musterstadt', 'BAB', 'Langestr., 12345 Musterstadt', 'Baumallee, 12345 Musterstadt']
)
stichwort = random.choice(
    ['TH0 - Baum auf Straße', 'B0 - Gelöschtes Feuer', 'TH1 - Baum auf PKW', 'CBRN1 - Ölspur', 'TH1 - Laufen Betriebsmittel', 'B1 - Brennt Mülleimer']
)
einsatzstellen.insert_one(
    {'nr_lst': no, 'stichwort': stichwort, 'anschrift': anschrift, 'status': 'unbearbeitet', 'datum': jetzt,
     'liste_eintrag': [[jetzt, f'Einsatz angelegt: Einsatznummer [{no}], Stichwort [{stichwort}], Anschrift [{anschrift}], Status [unbearbeitet]', '', '', 'Max Mustermann']],
     'letztes_update': jetzt})

# for i in range(20):
#     einsatzstellen.insert_one(
#         {'nr_lst': i, 'stichwort': 'TH 0', 'anschrift': 'Neustr.', 'status': 'offen', 'datum': datetime.now(), 'liste_eintrag': [
#             [datetime.now(), 'Einsatz angelegt', '', '', 'Max Mustermann']
#             ]})

# einsatzstellen.delete_many({})
