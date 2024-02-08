from pymongo import ReturnDocument
from bson import ObjectId
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime

import settings

from src.menu import Hauptmenu


class Einsatztagebuch(ttk.Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)

        self.parent = parent
        self.einsatzstelle_arbeit = None
        
        # Hauptmenü
        self.hauptmenu = Hauptmenu(self, user)
        
        # Einsatzübersicht
        self.einsatzliste = Einsatzliste(self, user, db)
        
        # Tagebuch je Einsatz
        self.eintragliste = Eintragliste(self, user, db)
        
        #Elemente ausrichten
        self.hauptmenu.pack(pady=5, padx=5, anchor='e')
        self.einsatzliste.pack(pady=0, padx=5, fill='x')
        self.eintragliste.pack(pady=5, padx=5, fill='both')
        

class Eintragliste(ttk.Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.db = db        
                
        # Anzeige ausgewählter Einsatz
        self.label_einsatz_text = tk.StringVar(self, '- Einsatz -')
        self.label_einsatz = ttk.Label(master=self, textvariable=self.label_einsatz_text, style='primary', font='bold')        
        
        # Tabelle zur Anzeige alle Einträge zum ausgewähltem Einsatz
        self.headings = ['datum', 'eintrag', 'von', 'an', 'funker']
        self.tabel = ttk.Treeview(master=self, columns=self.headings, displaycolumns=['datum', 'eintrag', 'funker'], show='headings', height=15)        
        self.tabel.heading('datum', text='Zeitstempel', anchor='w')
        self.tabel.column('datum', width=120, minwidth=100, stretch=False)
        self.tabel.heading('eintrag', text='Eintrag', anchor='w')
        self.tabel.column('eintrag', minwidth=100)
        self.tabel.heading('von', text='Absender', anchor='w')
        self.tabel.column('von', minwidth=10)
        self.tabel.heading('an', text='Empfänger', anchor='w')
        self.tabel.column('an', minwidth=10)
        self.tabel.heading('funker', text='Bearbeiter', anchor='w')
        self.tabel.column('funker', width=150, minwidth=100, stretch=False)
        #self.tabel.tag_configure('odd', background='lightblue')
        
        # Rahmen für Eingaben
        self.frame_entry = ttk.Frame(self)
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
        self.tabel.pack(pady=0, padx=5, fill='both') 
        self.frame_entry.pack(pady=5, padx=5, fill='x')

        # Eingabeelemente anzeigen / ausrichten        
        if settings.absender or settings.empfaenger:
            ttk.Label(self.frame_entry, text='Eintrag').grid(row=0, column=0, pady=(5, 0))
        if settings.absender:
            ttk.Label(self.frame_entry, text='Absender').grid(row=0, column=1, pady=(5, 0))
            self.entry_absender.grid(row=1, column=1, padx=(5,0), sticky='ew')
        if settings.empfaenger:
            ttk.Label(self.frame_entry, text='Empfänger').grid(row=0, column=2, pady=(5, 0))
            self.entry_empfang.grid(row=1, column=2, padx=(5,0), sticky='ew')      
        self.entry_funk.grid(row=1, column=0, padx=(5,0), sticky='ew')        
        self.button_absenden.grid(row=1, column=3, padx=(5,5), sticky='ew')                
              

    def update_table(self, id):
        db = self.db
        for element in self.tabel.get_children():
            self.tabel.delete(element)
        
        if id:
            self.einsatzstelle_arbeit = id
            einsatzstelle = db.einsatzstellen.find_one(id)
            
            stichwort = einsatzstelle['stichwort']
            anschrift = einsatzstelle['anschrift']
            status = einsatzstelle['status']
            text = f'{stichwort}: {anschrift} ({status})'
            self.label_einsatz_text.set(text)
            
            eintrage = db.eintrage.find({'einsatz': id})
            for i, eintrag in enumerate(eintrage):
                row_tag = 'even' if (i%2==0) else 'odd'

                zeile=list(eintrag.values())[2:]
                zeile[0] = zeile[0].strftime('%d.%m.%Y %H:%M')

                self.tabel.insert(parent='', index='end', values=zeile, tags=(row_tag,))
        
        else:
            self.label_einsatz_text.set('- Einsatz -')

    def add_entry(self, _):
        db = self.db
        entry = self.entry_funk.get()
        funker = self.user.get()
        now = datetime.datetime.now()
        
        # Eintrag erzeugen wenn Eingabefeld Inhalt besitzt
        if entry and self.einsatzstelle_arbeit:           
            
            db.einsatzstellen.find_one_and_update(
                {'_id': self.einsatzstelle_arbeit},
                { '$set': {'letztes_update': now} }, 
                return_document = ReturnDocument.AFTER
            )

            eintrag = {
                'einsatz': self.einsatzstelle_arbeit,
                'zeitstempel': now,
                'eintrag': entry,
                'absender': self.entry_absender.get(),
                'empfanger': self.entry_empfang.get(),
                'bearbeiter': funker
            }
            db.eintrage.insert_one(eintrag)
            
            zeile = list(eintrag.values())[1:]
            self.tabel.insert(parent='', index='end', values=zeile)
            self.entry_funk.delete(0, 'end')            


class Einsatzliste(ttk.Frame):
    def __init__(self, parent, user, db):
        super().__init__(parent)

        self.parent = parent
        self.db = db
        self.user = user
        self.einsatzstelle_focus = None

        self.letzte_aktualisierung = None
        
        # Tabelle aller Einsätze
        self.headings = ['id', 'datum', 'stichwort', 'anschrift', 'status']
        self.tabel_einsatz = ttk.Treeview(master=self, columns=self.headings, displaycolumns=self.headings[1:], show='headings')
        self.tabel_einsatz.heading('id', text='Nr.')
        self.tabel_einsatz.heading('datum', text='Einsatzbeginn', anchor='w')
        self.tabel_einsatz.column('datum', width=120, minwidth=100, stretch=False)
        self.tabel_einsatz.heading('stichwort', text='Stichwort', anchor='w')
        self.tabel_einsatz.column('stichwort')
        self.tabel_einsatz.heading('anschrift', text='Anschrift', anchor='w')
        self.tabel_einsatz.column('anschrift', width=200)
        self.tabel_einsatz.heading('status', text='Status', anchor='w')
        self.tabel_einsatz.column('status', width=120, minwidth=50, stretch=False)
        self.tabel_einsatz.tag_configure('late', background='red')
        self.tabel_einsatz.tag_configure('unbearbeitet', background='#ffcccb')
        self.tabel_einsatz.tag_configure('in Arbeit', background='#ffffe0')
        self.tabel_einsatz.tag_configure('abgeschlossen', background='#90ee90')       

        self.tabel_einsatz.bind('<<TreeviewSelect>>', self.item_selection)

        self.frame_optionen = ttk.Frame(self)
        
        # Button zur Bearbeitung und Anlage eines Einsatzes
        self.button_neuer_einsatz = ctk.CTkButton(self.frame_optionen, text='Neuer Einsatz', command=self.einsatz_anlegen_maske)
        self.button_update_einsatz = ctk.CTkButton(self.frame_optionen, text='Einsatz aktualisieren', command=self.einsatz_update_maske)
        
        # Filter Optionen        
        self.check_arbeit_value = tk.IntVar(self.frame_optionen, 1)        
        self.check_arbeit = ttk.Checkbutton(self.frame_optionen, text='Abgeschlossene Einsätze', variable=self.check_arbeit_value, command=self.update_table)
        
        self.check_date_value = tk.IntVar(self.frame_optionen, 1)
        self.check_date = ttk.Checkbutton(self.frame_optionen, text='Zeige nur Einsätze nach', variable=self.check_date_value, command=self.update_table)
        
        self.yesterday = datetime.date.today() - datetime.timedelta(days=7)
        self.date_filter = ttk.DateEntry(self.frame_optionen, firstweekday=7, startdate=self.yesterday, dateformat='%d.%m.%Y')
        
        # Elemente ausrichten
        self.button_neuer_einsatz.pack(padx=5, pady=(5,0), anchor='w')
        self.button_update_einsatz.pack(padx=5, pady=(5,0), anchor='w')        
        
        self.check_date.pack(padx=5, pady=(20,0), anchor='w')
        self.date_filter.pack(padx=5, pady=(5,0), anchor='w')

        self.check_arbeit.pack(padx=5, pady=(20,5), anchor='w')
        

        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='Einsatzübersicht', font='bold').grid(row=0, column=0)
        self.tabel_einsatz.grid(row=1, column=0, padx=5, pady=5, sticky='news')
        self.frame_optionen.grid(row=1, column=1, sticky='news')
        
    
    def einsatz_update_maske(self):
        db = self.db
        
        selection = self.tabel_einsatz.selection()
        if selection:
            id = self.tabel_einsatz.item(selection[0])['values'][0]        
            einsatz = db.einsatzstellen.find_one(ObjectId(id))
            
            stichwort = einsatz['stichwort']
            nummer = einsatz['nr_lst']     
            anschrift = einsatz['anschrift']
            status = einsatz['status']
            
            eingabe_maske = ttk.Toplevel('Einsatz aktualisieren')
            eingabe_maske.iconphoto(False, self.parent.parent.main_icon)
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
                    ObjectId(id),
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
    
    def einsatz_update_schreiben(self, id, nr, status, stichwort, anschrift, fenster):
        db = self.db
        user = self.user
        now = datetime.datetime.now()
        
        if stichwort and anschrift:           
            db.einsatzstellen.find_one_and_update(
                    {'_id': id},
                    { '$set': {
                        'nr_lst': nr,
                        'stichwort': stichwort,
                        'anschrift': anschrift,
                        'status': status,
                        'letztes_update': now} }, 
                    return_document = ReturnDocument.AFTER
                )
            
            db.eintrage.insert_one({
                'einsatz': id,
                'zeitstempel': now,
                'eintrag': f'Einsatz update: {stichwort}, {anschrift} ({status}) - {nr}',
                'absender': '',
                'empfanger': '',
                'bearbeiter': user.get()
            })
            
            self.update_table()
            fenster.destroy()
        else:
            tk.messagebox.showwarning(
                title='Einsatz update',
                message='Einsatzstichwort und Anschrift sind Pflichangaben.'
            )
    
    def einsatz_anlegen_maske(self):
        eingabe_maske = ttk.Toplevel('Neuer Einsatz')
        eingabe_maske.iconphoto(False, self.parent.parent.main_icon)
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
        
    def einsatz_in_db_schreiben(self, no, stichwort, anschrift, fenster):
        db = self.db
        user = self.user
        now = datetime.datetime.now()
        
        if no.isnumeric():
            no = int(no)
        
        if stichwort and anschrift:
            einsatz = db.einsatzstellen.insert_one({
                'nr_lst': no,
                'stichwort': stichwort,
                'anschrift': anschrift,
                'status': 'unbearbeitet',
                'datum': now,
                'letztes_update': now,
                'archiv': False
            })

            db.eintrage.insert_one({
                'einsatz': ObjectId(einsatz.inserted_id),
                'zeitstempel': now,
                'eintrag': f'Einsatz neu: {stichwort}, {anschrift} (unbearbeitet) - {no}',
                'absender': '',
                'empfanger': '',
                'bearbeiter': user.get()
            })
            self.update_table()
            fenster.destroy()
        else:
            tk.messagebox.showwarning(
                title='Neuer Einsatz',
                message='Einsatzstichwort und Anschrift sind Pflichangaben.'
            )
    
    def update_table(self,):
        db = self.db
        abgeschlossen = not self.check_arbeit_value.get()
        check_datum = self.check_date_value.get()
        datum = datetime.datetime.strptime(self.date_filter.entry.get(), '%d.%m.%Y')    

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

        for element in self.tabel_einsatz.get_children():
            self.tabel_einsatz.delete(element)
        
        for i, einsatz in enumerate(einsatzstellen):            
            status = einsatz['status']
            datum = einsatz['datum']
            letztes_update = einsatz['letztes_update']
            datum_schwelle = datetime.datetime.now() - datetime.timedelta(minutes=settings.zeitschwelle_einsatz_ohne_bearbeitung)

            tag_row = 'even' if (i%2==0) else 'odd'
            tag_update = 'onTime'
            if (datum_schwelle>letztes_update) and (status != 'abgeschlossen'):
                tag_update = 'late'
            
            self.tabel_einsatz.insert(parent='', index=0, values=(
                einsatz['_id'],
                datum.strftime('%d.%m.%Y %H:%M'),
                einsatz['stichwort'],
                einsatz['anschrift'],
                status                 
            ), tags=(tag_row, status, tag_update))

        for row in self.tabel_einsatz.get_children():
            id = ObjectId(self.tabel_einsatz.item(row)['values'][0])
            if self.einsatzstelle_focus == id:
                self.tabel_einsatz.focus(row)
                self.tabel_einsatz.selection_set(row)
                break
        else:
            self.einsatzstelle_focus = None
            self.parent.eintragliste.update_table(None)
 
    def item_selection(self, _):
        selection = self.tabel_einsatz.selection()        
        if selection:            
            id = self.tabel_einsatz.item(selection[0])['values'][0]
            id = ObjectId(id)
            self.einsatzstelle_focus = id
            self.parent.eintragliste.update_table(id)
        
        else:
            self.einsatzstelle_focus = None
