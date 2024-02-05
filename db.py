from pymongo import MongoClient
from bson import ObjectId
from getpass import getpass
from datetime import datetime
import time

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

for est in alle_einsatzstellen:
    print(est)

einsatzstellen.insert_one(
    {'nr_lst': 2024000001, 'stichwort': 'TH 0', 'strasse': 'Neustr.', 'status': 'offen', 'datum': datetime.now(), 'liste_eintrag': [
         [datetime.now(), 'Einsatz angelegt', '', '', 'Max Mustermann']
        ]})

# einsatzstellen.delete_many({})
