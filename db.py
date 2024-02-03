from pymongo import MongoClient
from bson import ObjectId
from getpass import getpass
from einsatzdb import beispiel_einsatz_db
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

eine_einsatzstelle = einsatzstellen.find_one(ObjectId('65be9246b026001556c778ce'))

# print(eine_einsatzstelle)

# for est in alle_einsatzstellen:
#     print(est)

# print(list(updates.find()))

# einsatzstellen.insert_many(beispiel_einsatz_db)

einsatzstellen.insert_one(
    {'nr_lst': 2024000006, 'stichwort': 'TH0', 'strasse': 'Neustr.', 'status': 'offen', 'liste_eintrag': [
         [datetime.now().strftime('%d.%m.%Y %H:%M'), 'Einsatz angelegt', '', '', 'Swen']
        ]})
    
updates.insert_one({'date': datetime.now()})

# einsatzstellen.delete_many({})
# updates.delete_many({})
