from pymongo import ReturnDocument, MongoClient
from bson import ObjectId
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime
import json
import sqlite3
import os

from scripts.protokoll import Protokoll


class Einsatztagebuch(ttk.Frame):
    def __init__(self, parent, nutzer: tk.StringVar):
        super().__init__(parent)

        self.parent = parent
        self.user_login: tk.StringVar = nutzer
        self.nutzer: str = self.user_login.get()
        
        self.einstellungen = self.lese_einstellungen()
        
        self.db = self.verbinde_datenbank()        
        
        self.einsatzstelle_arbeit = None
        self.einsatzstelle_focus = None  
        
        # Einsatzübersicht
        self.einsatzliste = ttk.Frame(self)
        # tablele aller Einsätze
        self.headings = ['id', 'datum', 'stichwort', 'anschrift', 'status']
        self.table_einsatz = ttk.Treeview(master=self.einsatzliste, columns=self.headings, displaycolumns=self.headings[1:], show='headings')
        self.table_einsatz.heading('id', text='Nr.')
        self.table_einsatz.heading('datum', text='Einsatzbeginn', anchor='w')
        self.table_einsatz.column('datum', width=120, minwidth=100, stretch=False)
        self.table_einsatz.heading('stichwort', text='Stichwort', anchor='w')
        self.table_einsatz.column('stichwort')
        self.table_einsatz.heading('anschrift', text='Anschrift', anchor='w')
        self.table_einsatz.column('anschrift', width=200)
        self.table_einsatz.heading('status', text='Status', anchor='w')
        self.table_einsatz.column('status', width=120, minwidth=50, stretch=False)
        self.table_einsatz.tag_configure('late', background='red')
        self.table_einsatz.tag_configure('unbearbeitet', background='#ffcccb')
        self.table_einsatz.tag_configure('in Arbeit', background='#ffffe0')
        self.table_einsatz.tag_configure('abgeschlossen', background='#90ee90')
        self.table_einsatz.bind('<<TreeviewSelect>>', self.item_selection)
        
        self.frame_optionen = ttk.Frame(self.einsatzliste)
        
        # Button zur Bearbeitung und Anlage eines Einsatzes
        self.button_neuer_einsatz = ctk.CTkButton(self.frame_optionen, text='Neuer Einsatz', command=self.einsatz_anlegen_maske)
        self.button_update_einsatz = ctk.CTkButton(self.frame_optionen, text='Einsatz aktualisieren', command=self.einsatz_update_maske)
        self.button_einsatz_ausgabe = ctk.CTkButton(self.frame_optionen, text='Protokoll ausleiten', command=self.protokoll_ausleiten)
        
        # Filter Optionen        
        self.check_arbeit_value = tk.IntVar(self.frame_optionen, 1)        
        self.check_arbeit = ttk.Checkbutton(self.frame_optionen, text='Abgeschlossene Einsätze', variable=self.check_arbeit_value, command=self.update_table_einsatz)
        
        self.check_date_value = tk.IntVar(self.frame_optionen, 1)
        self.check_date = ttk.Checkbutton(self.frame_optionen, text='Zeige nur Einsätze nach', variable=self.check_date_value, command=self.update_table_einsatz)
        
        self.yesterday = datetime.date.today() - datetime.timedelta(days=7)
        self.date_filter = ttk.DateEntry(self.frame_optionen, firstweekday=7, startdate=self.yesterday, dateformat='%d.%m.%Y')
        
        # Elemente ausrichten
        self.button_neuer_einsatz.pack(padx=5, pady=(5,0), anchor='w')
        self.button_update_einsatz.pack(padx=5, pady=(5,0), anchor='w')
        self.button_einsatz_ausgabe.pack(padx=5, pady=(5,0), anchor='w')
        self.check_date.pack(padx=5, pady=(20,0), anchor='w')
        self.date_filter.pack(padx=5, pady=(5,0), anchor='w')
        self.check_arbeit.pack(padx=5, pady=(20,5), anchor='w')        

        self.einsatzliste.columnconfigure(0, weight=1)
        ttk.Label(self.einsatzliste, text='Einsatzübersicht', font='bold').grid(row=0, column=0)
        self.table_einsatz.grid(row=1, column=0, padx=5, pady=5, sticky='news')
        self.frame_optionen.grid(row=1, column=1, sticky='news')
        
        # Tagebuch je Einsatz
        self.eintragliste = ttk.Frame(self)
        
        # Anzeige ausgewählter Einsatz
        self.label_einsatz_text = tk.StringVar(self.eintragliste, '- Einsatz -')
        self.label_einsatz = ttk.Label(master=self.eintragliste, textvariable=self.label_einsatz_text, style='primary', font='bold')        
        
        # tablele zur Anzeige alle Einträge zum ausgewähltem Einsatz
        self.headings = ['datum', 'eintrag', 'von', 'an', 'funker']
        self.headings_show = ['datum', 'eintrag', 'funker']
        
        if self.einstellungen['absender']:
            self.headings_show.insert(-1, 'von')
        if self.einstellungen['empfaenger']:
            self.headings_show.insert(-1, 'an')
        
        self.table = ttk.Treeview(master=self.eintragliste, columns=self.headings, displaycolumns=self.headings_show, show='headings', height=15)        
        self.table.heading('datum', text='Zeitstempel', anchor='w')
        self.table.column('datum', width=120, minwidth=100, stretch=False)
        self.table.heading('eintrag', text='Eintrag', anchor='w')
        self.table.column('eintrag', minwidth=100)
        self.table.heading('von', text='Absender', anchor='w')
        self.table.column('von',  width=150, minwidth=100, stretch=False)
        self.table.heading('an', text='Empfänger', anchor='w')
        self.table.column('an',  width=150, minwidth=100, stretch=False)
        self.table.heading('funker', text='Bearbeiter', anchor='w')
        self.table.column('funker', width=150, minwidth=100, stretch=False)
        #self.table.tag_configure('odd', background='lightblue')
        
        # Rahmen für Eingaben
        self.frame_entry = ttk.Frame(self.eintragliste)
        self.frame_entry.columnconfigure(0, weight=1)
        
        # Eingabe für den nächsten Eintrag im Funktagebuch
        self.entry_funk = ctk.CTkEntry(master=self.frame_entry, placeholder_text='Eintrag Funktagebuch')
        
        # Empfänger und Absender
        self.entry_absender = ctk.CTkEntry(master=self.frame_entry, placeholder_text='Absender')        
        self.entry_empfang = ctk.CTkEntry(master=self.frame_entry, placeholder_text='Empfänger')
        
        # Eingabe erzeugen beim betätigen der Enter-Taste
        self.entry_funk.bind('<Return>', self.add_entry)
        self.entry_absender.bind('<Return>', self.add_entry)
        self.entry_empfang.bind('<Return>', self.add_entry)  
        
        # Button zur Erstellung eines neuen Eintrags
        self.button_absenden = ctk.CTkButton(self.frame_entry, text='Eintragen', command=lambda: self.add_entry(tk.Event()))
        
        # Elemente ausrichten        
        self.label_einsatz.pack(pady=5, padx=5)
        self.table.pack(pady=0, padx=5, fill='both') 
        self.frame_entry.pack(pady=5, padx=5, fill='x')

        # Eingabeelemente anzeigen / ausrichten        
        if self.einstellungen['absender'] or self.einstellungen['empfaenger']:
            ttk.Label(self.frame_entry, text='Eintrag').grid(row=0, column=0, pady=(5, 0))
        if self.einstellungen['absender']:
            ttk.Label(self.frame_entry, text='Absender').grid(row=0, column=1, pady=(5, 0))
            self.entry_absender.grid(row=1, column=1, padx=(5,0), sticky='ew')
        if self.einstellungen['empfaenger']:
            ttk.Label(self.frame_entry, text='Empfänger').grid(row=0, column=2, pady=(5, 0))
            self.entry_empfang.grid(row=1, column=2, padx=(5,0), sticky='ew')      
        
        self.entry_funk.grid(row=1, column=0, padx=(5,0), sticky='ew')        
        self.button_absenden.grid(row=1, column=3, padx=(5,5), sticky='ew')
        
        #Elemente ausrichten
        self.einsatzliste.pack(expand=True, fill='x')
        self.eintragliste.pack(expand=True, fill='x')

        self.update_table_einsatz()

    def pack_me(self): # angepasst
        self.einstellungen = self.lese_einstellungen()
        self.nutzer: str = self.user_login.get()
        self.db = self.verbinde_datenbank()
        self.update_table_tagebuch()
        self.update_table_einsatz()
        self.pack(pady=(0,10), padx=10, expand=True, fill='both')
        
    def lese_einstellungen(self) -> dict: # angepasst
        with open('settings.json', 'r') as f:
            einstellungen = json.load(f)
        return einstellungen
    
    def verbinde_datenbank(self): # angepasst
        if self.einstellungen['einzelplatznutzung']:
            if not os.path.exists('data'):
                os.makedirs('data')
            db = sqlite3.connect(os.path.join('data', 'db.sqlite3'))
            cursor = db.cursor()
            # Tabelle für alle Einsätze
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS einsatzstellen(
                    _id INTEGER PRIMARY KEY NOT NULL,
                    einsatznr TEXT NOT NULL,
                    stichwort TEXT,
                    anschrift TEXT,
                    status TEXT,
                    datum TIMESTAMP,
                    letztes_update TIMESTAMP,
                    archiv INTEGER
                )
            ''')
            db.commit()            
                       
            # Tabelle für alle Einträge
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tagebuch(
                    einsatz INTEGER,
                    zeitstempel TIMESTAMP,
                    eintrag TEXT,
                    absender TEXT,
                    empfaenger TEXT,
                    bearbeiter TEXT
                )
            ''')
            db.commit()
            return db
        else:
            user = self.einstellungen['db_user']
            pwd = self.einstellungen['db_user_password']
            ip = self.einstellungen['db_ip']
            port = self.einstellungen['db_port']
            db = self.einstellungen['db_name']   
            client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")
            db = client[self.einstellungen['db_name']]
            return db
        
    def lese_datenbank(self): # angepasst, notwendig?
        db = self.db
        
        if self.einstellungen['einzelplatznutzung']:
            alle_einsatzstellen_tuple = db.cursor().execute('''SELECT * FROM einsatzstellen''').fetchall()
            alle_tagebuch_tuple = db.cursor().execute('''SELECT * FROM tagebuch''').fetchall()
            
            alle_einsatzstellen = [
                dict(zip((
                    'einsatznr',
                    'stichwort',
                    'anschrift',
                    'status',
                    'datum',
                    'letztes_update',
                    'archiv'), einsatz)) for einsatz in alle_einsatzstellen_tuple
            ]
            
            alle_tagebuch = [
                dict(zip((
                    'einsatznr',
                    'zeitstempel',
                    'eintrag',
                    'absender',
                    'empfaenger',
                    'bearbeiter'), tagebuch)) for tagebuch in alle_tagebuch_tuple
            ]
        else:
            alle_einsatzstellen = self.db.einsatzstellen.find()
            alle_tagebuch = self.db.tagebuch.find()
        
        return alle_einsatzstellen, alle_tagebuch

    def item_selection(self, _): # angepasst
        selection = self.table_einsatz.selection()        
        if selection:            
            id = self.table_einsatz.item(selection[0])['values'][0]
            self.einsatzstelle_focus = id
            self.update_table_tagebuch(id)
        
        else:
            self.einsatzstelle_focus = None

    def protokoll_ausleiten(self): # angepasst
        db = self.db
        
        selection = self.table_einsatz.selection()
        if selection:
            for sel in selection:
                id = self.table_einsatz.item(sel)['values'][0]
                if self.einstellungen['einzelplatznutzung']:
                    einsatzstelle = db.cursor().execute(f'''SELECT * FROM einsatzstellen WHERE _id = {id}''').fetchone()
                    einsatzstelle = dict(zip((
                        '_id',
                        'einsatznr',
                        'stichwort',
                        'anschrift',
                        'status',
                        'datum',
                        'letztes_update',
                        'archiv'), einsatzstelle))
                    eintrage = db.cursor().execute(f'''SELECT * FROM tagebuch WHERE einsatz={id}''')
                    eintrage:list = [
                        dict(zip((
                            'einsatz',
                            'zeitstempel',
                            'eintrag',
                            'absender',
                            'empfaenger',
                            'bearbeiter'), eintrag)) for eintrag in eintrage
                            ]
                    
                    einsatzstelle['datum'] = datetime.datetime.strptime(einsatzstelle['datum'], '%Y-%m-%d %H:%M:%S.%f')
                    einsatzstelle['letztes_update'] = datetime.datetime.strptime(einsatzstelle['letztes_update'], '%Y-%m-%d %H:%M:%S.%f')
                    
                    for eintrag in eintrage:
                        eintrag['zeitstempel'] = datetime.datetime.strptime(eintrag['zeitstempel'], '%Y-%m-%d %H:%M:%S.%f')
                else:
                    id = ObjectId(id)
                    einsatzstelle = db.einsatzstellen.find_one(id)                
                    eintrage = db.eintrage.find({'einsatz': id})         
                Protokoll(einsatzstelle, eintrage, self.einstellungen['absender'], self.einstellungen['empfaenger'], self.einstellungen['name_organisation'])
    
    def einsatz_update_maske(self): # angepasst
        db = self.db
        
        selection = self.table_einsatz.selection()
        if selection:
            id = self.table_einsatz.item(selection[0])['values'][0]
            if self.einstellungen['einzelplatznutzung']:
                einsatzstelle = db.cursor().execute(f'''SELECT * FROM einsatzstellen WHERE _id = {id}''').fetchone()
                einsatzstelle = dict(zip((
                    '_id',
                    'einsatznr',
                    'stichwort',
                    'anschrift',
                    'status',
                    'datum',
                    'letztes_update',
                    'archiv'), einsatzstelle))
                einsatz = einsatzstelle
            else:    
                einsatz = db.einsatzstellen.find_one(ObjectId(id))
            
            stichwort = einsatz['stichwort']
            nummer = einsatz['einsatznr']     
            anschrift = einsatz['anschrift']
            status = einsatz['status']
            
            eingabe_maske = ttk.Toplevel('Einsatz aktualisieren')
            #eingabe_maske.iconphoto(False, self.parent.parent.main_icon)
            einsatz_stichwort = ctk.CTkEntry(eingabe_maske)
            einsatz_stichwort.insert(0, stichwort)
            
            einsatz_nummer = ctk.CTkEntry(eingabe_maske)
            einsatz_nummer.insert(0, nummer)
                
            einsatz_anschrift = ctk.CTkEntry(eingabe_maske)
            einsatz_anschrift.insert(0, anschrift)
            
            status_liste = ['unbearbeitet', 'in Arbeit', 'abgeschlossen']
            
            einsatz_status = ctk.CTkComboBox(eingabe_maske, values=status_liste, state='readonly')
            einsatz_status.set(status)
            
            nr_einsatz = einsatz_nummer.get()
            if nr_einsatz.isnumeric():
                nr_einsatz = int(nr_einsatz)
                
            button_abbruch = ctk.CTkButton(eingabe_maske, text="Abbrechen", command=eingabe_maske.destroy)
            button_update = ctk.CTkButton(
                eingabe_maske,
                text="Einsatz aktualisieren",
                command= lambda: self.einsatz_update_schreiben(
                    id,
                    nr_einsatz,
                    einsatz_status.get(),
                    einsatz_stichwort.get(),
                    einsatz_anschrift.get(),
                    eingabe_maske
                    )
                )
        
            # Elemente ausrichten
            einsatz_stichwort.grid(row=1, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            einsatz_nummer.grid(row=2, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            einsatz_anschrift.grid(row=3, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            einsatz_status.grid(row=4, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            button_abbruch.grid(row=5, column=1, pady=5, padx=5)
            button_update.grid(row=5, column=2, pady=5, padx=5)
    
    def einsatz_update_schreiben(self, id, nr, status, stichwort, anschrift, fenster): # angepasst
        db = self.db
        user = self.nutzer
        now = datetime.datetime.now()
        
        if stichwort and anschrift:           
            einsatz = {
                'einsatznr': nr,
                'stichwort': stichwort,
                'anschrift': anschrift,
                'status': status,
                'letztes_update': now
            }
            neuer_eintrag = {
                'einsatz': id,
                'zeitstempel': now,
                'eintrag': f'Einsatz update: {stichwort}, {anschrift} ({status}) - {nr}',
                'absender': '',
                'empfaenger': '',
                'bearbeiter': user
            }

            if self.einstellungen['einzelplatznutzung']:
                db.cursor().execute('''UPDATE einsatzstellen SET einsatznr = ?, stichwort = ?, anschrift = ?, status = ?, letztes_update = ? WHERE _id = ?''', (nr, stichwort, anschrift, status, now, id))
                db.commit()
                db.cursor().execute('''INSERT INTO tagebuch(einsatz, zeitstempel, eintrag, absender, empfaenger, bearbeiter) VALUES(?,?,?,?,?,?)''', tuple(list(neuer_eintrag.values())))
                db.commit()              
            else:
                neuer_eintrag['einsatz'] = ObjectId(neuer_eintrag['einsatz'])
                db.einsatzstellen.find_one_and_update(
                        {'_id': ObjectId(id)},
                        { '$set': einsatz }, 
                        return_document = ReturnDocument.AFTER
                    )                
                db.eintrage.insert_one(neuer_eintrag)
            
            self.update_table_tagebuch(id)
            self.update_table_einsatz()
            fenster.destroy()
        else:
            tk.messagebox.showwarning(
                title='Einsatz update',
                message='Einsatzstichwort und Anschrift sind Pflichangaben.'
            )
    
    def einsatz_anlegen_maske(self): # angepasst
        eingabe_maske = ttk.Toplevel('Neuer Einsatz')
        #eingabe_maske.iconphoto(False, self.parent.parent.main_icon)
        einsatz_stichwort = ctk.CTkEntry(eingabe_maske, placeholder_text='Einsatzstichwort')
        einsatz_nummer = ctk.CTkEntry(eingabe_maske, placeholder_text='Einsatznummer')        
        einsatz_anschrift = ctk.CTkEntry(eingabe_maske, placeholder_text='Anschrift')
        button_abbruch = ctk.CTkButton(eingabe_maske, text="Abbrechen", command=eingabe_maske.destroy)
        button_anlegen = ctk.CTkButton(
            eingabe_maske,
            text="Einsatz anlegen",
            command= lambda: self.einsatz_in_db_schreiben(einsatz_nummer.get(), einsatz_stichwort.get(), einsatz_anschrift.get(), eingabe_maske)
            )
        
        # Elemente ausrichten
        einsatz_stichwort.grid(row=1, column=1, pady=5, padx=5, columnspan=2, sticky='we')
        einsatz_nummer.grid(row=2, column=1, pady=5, padx=5, columnspan=2, sticky='we')
        einsatz_anschrift.grid(row=3, column=1, pady=5, padx=5, columnspan=2, sticky='we')
        button_abbruch.grid(row=4, column=1, pady=5, padx=5)
        button_anlegen.grid(row=4, column=2, pady=5, padx=5)
        
    def einsatz_in_db_schreiben(self, no, stichwort, anschrift, fenster): # angepasst
        db = self.db
        user = self.nutzer
        now = datetime.datetime.now()
        
        if stichwort and anschrift:
            einsatz = {
                    'einsatznr': no,
                    'stichwort': stichwort,
                    'anschrift': anschrift,
                    'status': 'unbearbeitet',
                    'datum': now,
                    'letztes_update': now,
                    'archiv': False
                }
            ersten_eintrag = {
                    'einsatz': None,
                    'zeitstempel': now,
                    'eintrag': f'Einsatz neu: {stichwort}, {anschrift} (unbearbeitet) - {no}',
                    'absender': '',
                    'empfaenger': '',
                    'bearbeiter': user
                }
            
            if self.einstellungen['einzelplatznutzung']:
                cursor = db.cursor()
                cursor.execute('''INSERT OR REPLACE INTO einsatzstellen(einsatznr, stichwort, anschrift, status, datum, letztes_update, archiv) VALUES(?,?,?,?,?,?,?)''', tuple(list(einsatz.values())))
                rowid = cursor.lastrowid
                db.commit()                
                ersten_eintrag['einsatz'] = rowid
                db.cursor().execute('''INSERT INTO tagebuch(einsatz, zeitstempel, eintrag, absender, empfaenger, bearbeiter) VALUES(?,?,?,?,?,?)''', tuple(list(ersten_eintrag.values())))
                db.commit()
            else:
                einsatz = db.einsatzstellen.insert_one(einsatz)
                ersten_eintrag['einsatz'] = einsatz.inserted_id
                db.eintrage.insert_one(ersten_eintrag)
            
            fenster.destroy()
            self.update_table_einsatz()
            
        else:
            tk.messagebox.showwarning(
                title='Neuer Einsatz',
                message='Einsatzstichwort und Anschrift sind Pflichangaben.'
            )
    
    def clear_table_einsatz(self):
        for element in self.table_einsatz.get_children():
            self.table_einsatz.delete(element)

    def update_table_einsatz(self,): # angepasst
        db = self.db
        abgeschlossen = not self.check_arbeit_value.get()
        check_datum = self.check_date_value.get()
        datum = datetime.datetime.strptime(self.date_filter.entry.get(), '%d.%m.%Y')    

        if self.einstellungen['einzelplatznutzung']:
            einsatzstellen_alle = db.cursor().execute('''SELECT * FROM einsatzstellen''').fetchall()
            einsatzstellen_alle = [
                dict(zip((
                    '_id',
                    'einsatznr',
                    'stichwort',
                    'anschrift',
                    'status',
                    'datum',
                    'letztes_update',
                    'archiv'), einsatz)) for einsatz in einsatzstellen_alle
            ]

            for est in einsatzstellen_alle:
                est['datum'] = datetime.datetime.strptime(est['datum'], '%Y-%m-%d %H:%M:%S.%f')
                est['letztes_update'] = datetime.datetime.strptime(est['letztes_update'], '%Y-%m-%d %H:%M:%S.%f')
            
            einsatzstellen = []
            for est in einsatzstellen_alle:
                if abgeschlossen and check_datum:
                    if (est['status'] != "abgeschlossen") and (est['datum']>=datum):
                        einsatzstellen.append(est)
                elif abgeschlossen:
                    if (est['status'] != "abgeschlossen"):
                        einsatzstellen.append(est)
                elif check_datum:
                    if (est['datum']>=datum):
                        einsatzstellen.append(est)
                else:
                    einsatzstellen = einsatzstellen_alle
            
            
        else:
            if abgeschlossen and check_datum:
                query = {'status': {'$nin': ['abgeschlossen']},
                        'datum': {'$gte': datum}}
            elif abgeschlossen:
                query = {'status': {'$nin': ['abgeschlossen']}}
            elif check_datum:
                query = {'datum': {'$gte': datum}}
            else:
                query = {}
        
            einsatzstellen = db.einsatzstellen.find(query)

        
        self.clear_table_einsatz()
        
        for i, einsatz in enumerate(einsatzstellen):            
            status = einsatz['status']
            datum = einsatz['datum']
            letztes_update = einsatz['letztes_update']
            datum_schwelle = datetime.datetime.now() - datetime.timedelta(minutes=self.einstellungen['zeitschwelle_einsatz_ohne_bearbeitung'])

            tag_row = 'even' if (i%2==0) else 'odd'
            tag_update = 'onTime'
            if (datum_schwelle>letztes_update) and (status != 'abgeschlossen'):
                tag_update = 'late'
            
            self.table_einsatz.insert(parent='', index=0, values=(
                einsatz['_id'],
                datum.strftime('%d.%m.%Y %H:%M'),
                einsatz['stichwort'],
                einsatz['anschrift'],
                status                 
            ), tags=(tag_row, status, tag_update))

        for row in self.table_einsatz.get_children():
            id = self.table_einsatz.item(row)['values'][0]
            if self.einsatzstelle_focus == id:
                self.table_einsatz.focus(row)
                self.table_einsatz.selection_set(row)
                break
        else:
            self.einsatzstelle_focus = None
            self.update_table_tagebuch(None)
         
    def update_table_tagebuch(self, id=None): # angepasst
        db = self.db
        for element in self.table.get_children():
            self.table.delete(element)
        
        if id:
            self.einsatzstelle_arbeit = id
            if self.einstellungen['einzelplatznutzung']:
                einsatzstelle = db.cursor().execute(f'''SELECT * FROM einsatzstellen WHERE _id = {id}''').fetchone()
                einsatzstelle = dict(zip((
                    '_id',
                    'einsatznr',
                    'stichwort',
                    'anschrift',
                    'status',
                    'datum',
                    'letztes_update',
                    'archiv'), einsatzstelle))
                eintrage = db.cursor().execute(f'''SELECT * FROM tagebuch WHERE einsatz={id}''')
                eintrage:list = [
                    dict(zip((
                        'einsatz',
                        'zeitstempel',
                        'eintrag',
                        'absender',
                        'empfaenger',
                        'bearbeiter'), eintrag)) for eintrag in eintrage
                        ]
                for eintrag in eintrage:
                    eintrag['zeitstempel'] = datetime.datetime.strptime(eintrag['zeitstempel'], '%Y-%m-%d %H:%M:%S.%f')
            else:
                id = ObjectId(id)
                einsatzstelle = db.einsatzstellen.find_one(id)
                eintrage = db.eintrage.find({'einsatz': id})
            
            stichwort = einsatzstelle['stichwort']
            anschrift = einsatzstelle['anschrift']
            status = einsatzstelle['status']
            text = f'{stichwort}: {anschrift} ({status})'
            self.label_einsatz_text.set(text)
            
            
            for i, eintrag in enumerate(eintrage):
                row_tag = 'even' if (i%2==0) else 'odd'

                zeile = [
                    eintrag['zeitstempel'].strftime('%d.%m.%Y %H:%M'),
                    eintrag['eintrag'],
                    eintrag['absender'],
                    eintrag['empfaenger'],
                    eintrag['bearbeiter']
                ]

                self.table.insert(parent='', index='end', values=zeile, tags=(row_tag,))
        
        else:
            self.label_einsatz_text.set('- Einsatz -')

    def add_entry(self, _): # Funktion mit MongoDB prüfen
        db = self.db
        entry = self.entry_funk.get()
        funker = self.nutzer
        now = datetime.datetime.now()
        
        # Eintrag erzeugen wenn Eingabefeld Inhalt besitzt
        table_einsatz = self.table_einsatz
        selection = table_einsatz.selection()
        if entry and selection:
            for cnt, sel in enumerate(selection):
                id = table_einsatz.item(sel)['values'][0]
                eintrag = {
                    'einsatz': id,
                    'zeitstempel': now,
                    'eintrag': entry,
                    'absender': self.entry_absender.get(),
                    'empfaenger': self.entry_empfang.get(),
                    'bearbeiter': funker
                }  
                
                if self.einstellungen['einzelplatznutzung']:
                    db.cursor().execute('''UPDATE einsatzstellen SET letztes_update = ? WHERE _id = ?''', (now, id))
                    db.commit()
                    db.cursor().execute('''INSERT INTO tagebuch(einsatz, zeitstempel, eintrag, absender, empfaenger, bearbeiter) VALUES(?,?,?,?,?,?)''', tuple(list(eintrag.values())))
                    db.commit()
                else:
                    eintrag['einsatz'] = ObjectId(eintrag['einsatz'])
                    db.einsatzstellen.find_one_and_update(
                        {'_id': ObjectId(id)},
                        { '$set': {'letztes_update': now} }, 
                        return_document = ReturnDocument.AFTER
                    )                
                    db.eintrage.insert_one(eintrag)
                
                if cnt == 0:
                    zeile = list(eintrag.values())[1:]
                    self.table.insert(parent='', index='end', values=zeile)
                    self.entry_funk.delete(0, 'end')

        self.update_table_tagebuch(self.einsatzstelle_arbeit)       
