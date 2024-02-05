from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
from getpass import getpass
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import os
import datetime
import locale


# Einstellung zu verwendung vom Dezimaltrennzeichen
# original_locale = locale.getlocale(locale.LC_NUMERIC)
locale.setlocale(locale.LC_NUMERIC, "C")
# locale.setlocale(locale.LC_NUMERIC, original_locale)

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        
        # Grundeinstellungen des Fensters
        self.title("Funktagebuch")
        #self.geometry(f"{1000}x{600}")        

        self.user_system = tk.StringVar(value=os.getlogin())
        self.user_login = tk.StringVar()

        # Lade Daten
        self.db = connect_database()
        
        # Hauptfenster
        self.main = Hauptfenster(self)
        
        # Login Fenster
        self.login = Login(self)
        
        # Kopfleiste
        self.kopfleiste = Leiste_Kopf(self.main)
        self.kopfleiste.grid(row=0, column=0, sticky='news')           
        
        # Einsatztagebuch
        self.einsatztagebuch = Einsatztagebuch(self.main)
        self.einsatztagebuch.grid(row=1, column=0, padx=5, pady=5, sticky='news')            

        # Loop-Funktion zur Aktualisierung div. Objekte
        self.loop()    
    
        
    def loop(self):
        # Diese Schleife wird alle 5 Sekunden ausgeführt  
        self.after(5000, self.loop)

        self.einsatztagebuch.update_tabel(self.einsatztagebuch.einsatzstelle_arbeit)
        self.einsatztagebuch.einsatzliste.update_tabel()        
                

class Hauptfenster(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


class Einsatztagebuch(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.einsatzstelle_arbeit = None
        
        # Linkes Fenster (Einsatzübersicht)
        self.einsatzliste = Einsatzliste(self)        

        # Eingabe für den nächsten Eintrag im Funktagebuch
        self.entry_funk = ctk.CTkEntry(master=self, placeholder_text='Eintrag Funktagebuch')
        
        # Empfänger und Absender
        self.entry_absender = ctk.CTkEntry(master=self, placeholder_text='Absender')        
        self.entry_empfang = ctk.CTkEntry(master=self, placeholder_text='Empfänger')
        
        # Eingabe erzeugen beim betätigen der Enter-Taste
        self.entry_funk.bind('<Return>', self.add_entry)
        self.entry_absender.bind('<Return>', self.add_entry)
        self.entry_empfang.bind('<Return>', self.add_entry)        
        
        # Anzeige ausgewählter Einsatz
        self.label_einsatz = ttk.Label(master=self, text='- Einsatz -', style='primary', font='bold')
        
        # Tabelle zur Anzeige alle Einträge zum ausgewähltem Einsatz
        self.headings = ['datum', 'eintrag', 'von', 'an', 'funker']
        self.tabel = ttk.Treeview(master=self, columns=self.headings, displaycolumns=['datum', 'eintrag', 'funker'], show='headings')
        self.tabel.heading('datum', text='Zeitstempel')
        self.tabel.heading('eintrag', text='Eintrag')
        self.tabel.heading('von', text='Absender')
        self.tabel.heading('an', text='Empfänger')
        self.tabel.heading('funker', text='Bearbeiter')
        
        # Button zur Erstellung eines neuen Eintrags
        self.button_absenden = ctk.CTkButton(self, text='Absenden', command=lambda: self.add_entry(tk.Event()))
        
        # Elemente ausrichten
        self.einsatzliste.grid(row=0, column=0, pady=5, sticky='nw')        
        self.label_einsatz.grid(row=1, column=0, sticky='nw')
        self.tabel.grid(row=2, column=0, sticky='news', columnspan=5)       
        self.entry_funk.grid(row=4, column=0, sticky='news', padx=5, pady=5)
        self.button_absenden.grid(row=4, column=4, sticky='w')

        # Zusätzliche Abfrage von Absender und Empfänger inkl. Überschrift        
        # ttk.Label(self, text='Eintrag').grid(row=3, column=0, pady=(5, 0))
        # ttk.Label(self, text='Absender').grid(row=3, column=2, pady=(5, 0))
        # ttk.Label(self, text='Empfänger').grid(row=3, column=3, pady=(5, 0))      
        # self.entry_absender.grid(row=4, column=2, sticky='nws', padx=5, pady=5)
        # self.entry_empfang.grid(row=4, column=3, sticky='nws', padx=5, pady=5)
                
              

    def update_tabel(self, id):
        db = self.parent.parent.db
        for element in self.tabel.get_children():
            self.tabel.delete(element)
        
        if id:
            self.einsatzstelle_arbeit = id
            einsatzstelle = db.einsatzstellen.find_one(id)
            
            stichwort = einsatzstelle['stichwort']
            strasse = einsatzstelle['strasse']
            status = einsatzstelle['status']
            text = f'{stichwort}: {strasse} ({status})'
            self.label_einsatz.config(text=text)
            
            
            for eintrag in einsatzstelle['liste_eintrag']:
                zeile = eintrag
                zeile[0] = zeile[0].strftime('%d.%m.%Y %H:%M')
                self.tabel.insert(parent='', index='end', values=zeile)

    def add_entry(self, _):
        db = self.parent.parent.db
        entry = self.entry_funk.get()
        funker = self.parent.parent.user_login.get()
        
        # Eintrag erzeugen wenn Eingabefeld Inhalt besitzt
        if entry:
            eintrag = (
                datetime.datetime.now(),
                entry,
                self.entry_absender.get(),
                self.entry_empfang.get(),
                funker                   
            )
            
            est = db.einsatzstellen.find_one(self.einsatzstelle_arbeit)
            liste_eintrag = est['liste_eintrag']
            liste_eintrag.append(list(eintrag))
            
            db.einsatzstellen.find_one_and_update(
                {'_id': self.einsatzstelle_arbeit},
                { '$set': { 'liste_eintrag' : liste_eintrag} }, 
                return_document = ReturnDocument.AFTER
            )
            
            self.tabel.insert(parent='', index='end', values=eintrag)
            self.entry_funk.delete(0, 'end')            


class Leiste_Kopf(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)        
        
        self.parent = parent
        self.login = parent.parent.login
        self.funker_name = self.parent.parent.user_login
        
        ttk.Label(self, text='User: ').grid(row=0, column=0)
        ttk.Label(self, textvariable=self.funker_name).grid(row=0, column=1)
        ctk.CTkButton(self, text='Logout', command=self.logout).grid(row=1, columnspan=2, sticky='we')

        
    def logout(self):
        self.parent.grid_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.grid(pady=20, padx=20)


class Einsatzliste(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.einsatzstelle_focus = None
        
        # Tabelle aller Einsätze
        self.headings = ['id', 'stichwort', 'strasse', 'status']
        self.tabel_einsatz = ttk.Treeview(master=self, columns=self.headings, displaycolumns=self.headings[1:], show='headings')
        self.tabel_einsatz.heading('id', text='Nr.')
        self.tabel_einsatz.heading('stichwort', text='Stichwort')
        self.tabel_einsatz.heading('strasse', text='Straße')
        self.tabel_einsatz.heading('status', text='Status')

        self.tabel_einsatz.bind('<<TreeviewSelect>>', self.item_selection)
        
        # Button zur Bearbeitung und Anlage eines Einsatzes
        self.button_neuer_einsatz = ctk.CTkButton(self, text='Neuer Einsatz', command=self.einsatz_anlegen_maske)
        self.button_update_einsatz = ctk.CTkButton(self, text='Einsatz aktualisieren', command=self.einsatz_update_maske)
        
        # Filter Optionen
        self.check_arbeit_value = tk.IntVar(self, 0)
        self.check_arbeit = ttk.Checkbutton(self, text='Abgeschlossene Einsätze ausblenden', variable=self.check_arbeit_value, command=self.update_tabel)
                
        # Elemente ausrichten
        ttk.Label(self, text='Einsatzliste').grid(row=0, column=0)
        self.button_update_einsatz.grid(row=0, column=1, sticky='e')
        self.button_neuer_einsatz.grid(row=0, column=2, padx=5, sticky='e')
        self.tabel_einsatz.grid(row=1, column=0, columnspan=3, pady=5)
        self.check_arbeit.grid(row=2, column=0, sticky='w', pady=(5,20), padx=10)
    
    def einsatz_update_maske(self):
        db = self.parent.parent.parent.db
        
        selection = self.tabel_einsatz.selection()
        if selection:
            id = self.tabel_einsatz.item(selection[0])['values'][0]        
            einsatz = db.einsatzstellen.find_one(ObjectId(id))
            
            stichwort = einsatz['stichwort']
            nummer = einsatz['nr_lst']     
            strasse = einsatz['strasse']
            status = einsatz['status']
            
            eingabe_maske = ttk.Toplevel('Neuer Einsatz')
            einsatz_stichwort = ctk.CTkEntry(eingabe_maske)
            einsatz_stichwort.insert(0, stichwort)
            
            einsatz_nummer = ctk.CTkEntry(eingabe_maske)
            einsatz_nummer.insert(0, nummer)
                
            einsatz_strasse = ctk.CTkEntry(eingabe_maske)
            einsatz_strasse.insert(0, strasse)
            
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
                    einsatz_strasse.get(),
                    eingabe_maske
                    )
                )
        
            # Elemente ausrichten
            einsatz_stichwort.grid(row=1, column=1, pady=5, columnspan=2)
            einsatz_nummer.grid(row=2, column=1, pady=5, columnspan=2)
            einsatz_strasse.grid(row=3, column=1, pady=5, columnspan=2)
            einsatz_status.grid(row=4, column=1, pady=5, columnspan=2)
            button_abbruch.grid(row=5, column=1, pady=5, padx=5)
            button_update.grid(row=5, column=2, pady=5, padx=5)
    
    def einsatz_update_schreiben(self, id, nr, status, stichwort, strasse, fenster):
        db = self.parent.parent.parent.db
        user = self.parent.parent.parent.user_login.get()
        now = datetime.datetime.now()
        
        if stichwort and strasse:
            eintrag = (
                now,
                'Einsatzdaten aktualisiert',
                '',
                '',
                user                  
            )
            
            est = db.einsatzstellen.find_one(id)
            liste_eintrag = est['liste_eintrag']
            liste_eintrag.append(list(eintrag))
            
            db.einsatzstellen.find_one_and_update(
                    {'_id': id},
                    { '$set': {
                        'nr_lst': nr,
                        'stichwort': stichwort,
                        'strasse': strasse,
                        'status': status,
                        'liste_eintrag': liste_eintrag} }, 
                    return_document = ReturnDocument.AFTER
                )
            
            self.update_tabel()
            fenster.destroy()
        else:
            tk.messagebox.showwarning(
                title='Einsatz update',
                message='Einsatzstichwort und Strasse sind Pflichangaben.'
            )
    
    def einsatz_anlegen_maske(self):
        eingabe_maske = ttk.Toplevel('Neuer Einsatz')
        einsatz_stichwort = ctk.CTkEntry(eingabe_maske, placeholder_text='Einsatzstichwort')
        einsatz_nummer = ctk.CTkEntry(eingabe_maske, placeholder_text='Einsatznummer')        
        einsatz_strasse = ctk.CTkEntry(eingabe_maske, placeholder_text='Straße / Hausnummer')
        button_abbruch = ctk.CTkButton(eingabe_maske, text="Abbrechen", command=eingabe_maske.destroy)
        button_anlegen = ctk.CTkButton(
            eingabe_maske,
            text="Einsatz anlegen",
            command= lambda: self.einsatz_in_db_schreiben(einsatz_nummer.get(), einsatz_stichwort.get(), einsatz_strasse.get(), eingabe_maske)
            )
        
        # Elemente ausrichten
        einsatz_stichwort.grid(row=1, column=1, pady=5, columnspan=2)
        einsatz_nummer.grid(row=2, column=1, pady=5, columnspan=2)
        einsatz_strasse.grid(row=3, column=1, pady=5, columnspan=2)
        button_abbruch.grid(row=4, column=1, pady=5, padx=5)
        button_anlegen.grid(row=4, column=2, pady=5, padx=5)
        
    def einsatz_in_db_schreiben(self, no, stichwort, strasse, fenster):
        db = self.parent.parent.parent.db
        user = self.parent.parent.parent.user_login.get()
        now = datetime.datetime.now()
        
        if no.isnumeric():
            no = int(no)
        
        if stichwort and strasse:
            db.einsatzstellen.insert_one({'nr_lst': no, 'stichwort': stichwort, 'strasse': strasse, 'status': 'unbearbeitet', 'datum': now, 'liste_eintrag': [
            [now, 'Einsatz angelegt', '', '', user]
            ]})
            self.parent.parent.parent.last_update = now
            
            self.update_tabel()
            fenster.destroy()
        else:
            tk.messagebox.showwarning(
                title='Neuer Einsatz',
                message='Einsatzstichwort und Strasse sind Pflichangaben.'
            )
    
    def update_tabel(self):
        db = self.parent.parent.parent.db
        abgeschlossen = self.check_arbeit_value.get()        

        if abgeschlossen:
            query = {'status': {'$nin': ['abgeschlossen']}}
        else:
            query = {}
        
        einsatzstellen = db.einsatzstellen.find(query)

        for element in self.tabel_einsatz.get_children():
            self.tabel_einsatz.delete(element)
        
        for einsatz in einsatzstellen:            
            status = einsatz['status']
            
            self.tabel_einsatz.insert(parent='', index='end', values=(
                einsatz['_id'],
                einsatz['stichwort'],
                einsatz['strasse'],
                status                 
            ))

        for row in self.tabel_einsatz.get_children():
            id = ObjectId(self.tabel_einsatz.item(row)['values'][0])
            if self.einsatzstelle_focus == id:
                self.tabel_einsatz.focus(row)
                self.tabel_einsatz.selection_set(row)
 
    
    def item_selection(self, _):
        selection = self.tabel_einsatz.selection()        
        if selection:            
            id = self.tabel_einsatz.item(selection[0])['values'][0]
            id = ObjectId(id)
            self.einsatzstelle_focus = id
            self.parent.parent.parent.einsatztagebuch.update_tabel(id)
        else:
            self.einsatzstelle_focus = None


class Login(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(pady=20, padx=20)
        
        self.parent = parent
        self.main = parent.main

        ttk.Label(master=self, text='Benutzeranmeldung', style='info', font='bold').pack()
        
        self.user_login = None
        self.user_login_entry = ctk.CTkEntry(master=self, placeholder_text='Vorname Nachname')

        self.user_login_entry.pack(padx=(5,5), pady=5)
        self.login_btn = ctk.CTkButton(master=self, text='Login', command=self.login_event).pack(padx=5, pady=5)
    
    def login_event(self):
        user_login = self.user_login_entry.get()
        if user_login:
            self.grid_forget()
            self.user_login = user_login
            self.parent.user_login.set(user_login)
            self.main.grid(pady=10, padx=10)
        else:
            ttk.Label(self, text='enter a valid name', style='warning').pack(pady=(0, 5), padx=20)


def connect_database():
    user = 'user' #input('Username: ')
    pwd = 'user' #getpass('Password: ')
    ip = '192.168.178.41'
    port = '27017'
    db = 'einsatztagebuch'
    
    client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")
    db = client.einsatztagebuch
    
    return db
    

def check_database(db, last_update):
    try:
        update = list(db.updates.find())[-1]
        update_date = update['date']            
        
        if update_date > last_update:
            last_update = update_date                
            return True
        else:
            return False
        
    except Exception as error:
        print(f'check_database: {error}')
        return False


# def read_database(db):
#     try:
#         einsatzstellen = db.einsatzstellen
#         liste_einsatz = einsatzstellen.find()
#         einsatzstellen = liste_einsatz
    
#     except Exception as error:
#         print(f'read_database: {error}')
#         einsatzstellen = beispiel_einsatz_db
        
#     return einsatzstellen


# def update_database(db):
#     now = datetime.datetime.now()
#     db.updates.insert_one({'date': now})


if __name__ == "__main__":
    app = App()
    app.mainloop()
