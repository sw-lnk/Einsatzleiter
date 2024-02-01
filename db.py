from pymongo import MongoClient
from getpass import getpass

user = input('Username: ')
pwd = getpass('Password: ')
ip = '192.168.178.41'
port = '27017'

client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}")

db = client.einsatz

berichte = db.berichte

berichte.insert_one(
    {'id': 99, 'stichwort': 'TH0 ', 'strasse': 'Neustr.', 'status': 'offen',
     'liste_eintrag': [
         ('01.02.2024 09:55', 'Einsatz angelegt', '', '', 'Max Mustermann')
        ]})

#berichte.delete_many({})
