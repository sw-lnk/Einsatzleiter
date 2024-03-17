from datetime import datetime
import random

from helper import verbinde_datenbank_mongo

user = 'arbeitsplatz1' #input('Username: ')
pwd = 'einsatzleitung1' #getpass('Password: ')
ip = '192.168.178.21'
port = '27017'
db_name = 'einsatzleitung'

db = verbinde_datenbank_mongo(user, pwd, ip, port, db_name)

einsatzstellen = db.einsatzstellen
eintrage = db.eintrage
krafte = db.krafte

# Zeige alle Einträge
# for einsatz in einsatzstellen.find():
#     print(einsatz)

# Zeige alle Einträge
# for eintrag in eintrage.find():
#     print(eintrag)


# Einen Einsatz anlegen
def einen_einsatz():
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
    einsatz = einsatzstellen.insert_one({
        'einsatznr': no,
        'stichwort': stichwort,
        'anschrift': anschrift,
        'status': 'unbearbeitet',
        'datum': jetzt,
        'letztes_update': jetzt,
        'archiv': False
    })

    eintrage.insert_one({
        'einsatz': einsatz.inserted_id,
        'zeitstempel': jetzt,
        'eintrag': f'Einsatz neu: {stichwort}, {anschrift} (unbearbeitet) - {no}',
        'absender': '',
        'empfaenger': '',
        'bearbeiter': 'Max Mustermann'
    })

def eine_einheit():
    jetzt = datetime.now()
    funk = random.choice(['1 HLF20 1', '1 LF20 1', '1 DLK23 1', '1 RW 1', '1 MTF 1'])
    krafte.insert_one({
        'funkrufname': funk,
        'vf': random.choice([0, 1]),
        'zf': random.choice([0, 1]),
        'gf': random.choice([0, 1]),
        'ms': random.choice(range(3,5)),
        'agt': random.choice(range(3,5)),
        'anmerkung': 'Einsatzbereit über Funk',
        'datum': jetzt
    })


# Einen Einsatz anlegen
einen_einsatz()

# Eine Einheit in Kräfteübersicht einfügen
# eine_einheit()

# Mehrer Beispiel Einsätze anlegen
# for i in range(5): einen_einsatz()

# Alle Einsatzstellen aus Datenbank löschen
# einsatzstellen.delete_many({})
# eintrage.delete_many({})
# krafte.delete_many({})
