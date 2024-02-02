from pymongo import MongoClient
from getpass import getpass
from einsatzdb import beispiel_einsatz_db
from datetime import datetime

user = 'user' #input('Username: ')
pwd = 'user' #getpass('Password: ')
ip = '192.168.178.41'
port = '27017'
db = 'einsatztagebuch'

client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")

db = client.einsatztagebuch
einsatzstellen = db.einsatzstellen
updates = db.updates

ests = einsatzstellen.find()

for est in ests:
    print(est)

print(list(updates.find()))

# einsatzstellen.insert_many(beispiel_einsatz_db)

# einsatzstellen.insert_one(
#     {'id': 88, 'stichwort': 'TH2', 'strasse': 'Großestr.', 'status': 'offen', 'liste_eintrag': [
#          ['01.02.2024 10:01', 'Einsatz angelegt', '', '', 'Max Mustermann']
#         ]})
    
# updates.insert_one({'date': datetime.now()})

# einsatzstellen.delete_many({})
# updates.delete_many({})
