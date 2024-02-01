from pymongo import MongoClient
from getpass import getpass

user = 'swen' #input('Username: ')
pwd = getpass('Password: ')

client = MongoClient(f"mongodb://{user}:{pwd}@192.168.178.41:27017")

db = client.einsatz

berichte = db.berichte

berichte.insert_one({'einsatznummer': 12345678, 'einsatzart': 'Brand'})

for bericht in berichte.find():
    print(bericht)
    
berichte.delete_many({})
