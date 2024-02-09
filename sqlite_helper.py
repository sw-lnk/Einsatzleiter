import os
import sqlite3
from datetime import datetime
import random

db_path = os.path.join('data', 'db.sqlite3')
db = sqlite3.connect(db_path)

# get a cursor object
cursor = db.cursor()

# CREATE TABLE
cursor.execute(
    """CREATE TABLE IF NOT EXISTS einsatzstellen(
                    nr_lst INTEGER,
                    stichwort TEXT,
                    anschrift TEXT,
                    status TEXT,
                    datum TEXT,
                    letztes_update TEXT,
                    archiv INTEGER
            )"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS eintrage(
                    einsatz INTEGER,
                    zeitstempel TEXT,
                    eintrag TEXT,
                    absender TEXT,
                    empfanger TEXT,
                    bearbeiter TEXT
            )"""
)
db.commit()

# Zufällige Einsatznummer
nr_lst = random.randint(1, 123456789)

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

cursor.execute(
    """INSERT INTO einsatzstellen(nr_lst, stichwort, anschrift, status, datum, letztes_update, archiv)
    VALUES (:nr_lst, :stichwort, :anschrift, :status, :datum, :letztes_update, :archiv)""",
    {
        "nr_lst": nr_lst,
        "stichwort": stichwort,
        "anschrift": anschrift,
        "status": 'unbearbeitet',
        "datum": jetzt,
        "letztes_update": jetzt,
        "archiv": 0
    },
)
db.commit()

cursor.execute(
    """INSERT INTO eintrage(einsatz, zeitstempel, eintrag, absender, empfanger, bearbeiter)
    VALUES (:einsatz, :zeitstempel, :eintrag, :absender, :empfanger, :bearbeiter)""",
    {
        "einsatz": nr_lst,
        "zeitstempel": jetzt,
        "eintrag": f'Einsatz neu: {stichwort}, {anschrift} (unbearbeitet) - {nr_lst}',
        "absender": '',
        "empfanger": '',
        "bearbeiter": 'Max Mustermann'
    },
)
db.commit()