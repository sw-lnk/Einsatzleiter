import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk
import customtkinter as ctk
import os
import datetime
import locale

from einsatzdb import liste_einsatz # Durch eine Anbindung an eine Datenbank ersetzen


# Einstellung zu verwendung vom Dezimaltrennzeichen
# original_locale = locale.getlocale(locale.LC_NUMERIC)
locale.setlocale(locale.LC_NUMERIC, "C")
# locale.setlocale(locale.LC_NUMERIC, original_locale)

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        
        # Grundeinstellungen des Fensters
        self.title("Funktagebuch")
        self.geometry(f"{1000}x{600}")        

        self.user_system = tk.StringVar(value=os.getlogin())
        self.user_login = tk.StringVar()

        # Hauptfenster
        self.main = Hauptfenster(self)
        
        # Login Fenster
        self.login = Login(self)
        
        # Kopfleiste
        self.kopfleiste = Leiste_Kopf(self.main)       
        
        # Linkes Fenster (Einsatzübersicht)
        self.einsatzliste = Einsatzliste(self.main, liste_einsatz)       
        
        # Arbeitsfenster
        self.arbeitsbereich = Arbeitsbereich(self.main, liste_einsatz)
        self.bind('<Return>', self.arbeitsbereich.add_entry) 


class Hauptfenster(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #self.grid(pady=20, padx=20)
        self.parent = parent


class Arbeitsbereich(ttk.Frame):
    def __init__(self, parent, liste_einsatz):
        super().__init__(parent)

        self.parent = parent
        self.liste_einsatz = liste_einsatz

        self.grid(row=2, column=0, padx=5, pady=5, sticky='news')

        # Eingabe für den nächsten Eintrag im Funktagebuch
        self.entry_funk = ctk.CTkEntry(master=self, placeholder_text='Eintrag Funktagebuch')
        self.entry_funk.grid(row=3, column=0, sticky='news', padx=10)

        # Anzeige ausgewählter Einsatz
        self.label_einsatz = ttk.Label(master=self, text='- ausgewählter Einsatz -', style='primary', font='bold')
        self.label_einsatz.grid(column=0, row=0, sticky='nw')
        
        # Tabelle zur Anzeige alle Einträge zum ausgewähltem Einsatz
        self.tabel = ttk.Treeview(master=self, columns=('datum', 'eintrag', 'von', 'an', 'funker'), show='headings')
        self.tabel.grid(column=0, row=1)
        self.tabel.heading('datum', text='Zeitstempel')
        self.tabel.heading('eintrag', text='Eintrag')
        self.tabel.heading('von', text='Absender')
        self.tabel.heading('an', text='Empfänger')
        self.tabel.heading('funker', text='Bearbeiter')        

    def update_tabel(self, id):
        for element in self.tabel.get_children():
            self.tabel.delete(element)
        
        for einsatz in self.liste_einsatz:
            if einsatz['id'] == id:                
                for eintrag in einsatz['liste_eintrag']:
                    self.tabel.insert(parent='', index='end', values=eintrag)
                break

    def add_entry(self, _):
        entry = self.entry_funk.get()
        funker = self.parent.parent.user_login.get()
        
        # Eintrag erzeugen wenn Eingabefeld Inhalt besitzt
        if entry:
            self.tabel.insert(parent='', index='end', values=(
                datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
                entry,
                'Ab',
                'An',
                funker                   
            ))
            self.entry_funk.delete(0, 'end')


class Leiste_Kopf(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky='news',)
        
        self.parent = parent
        self.login = parent.parent.login
        self.funker_name = self.parent.parent.user_login
        
        ttk.Label(self, text='User: ').grid(row=0, column=0)
        ttk.Label(self, textvariable=self.funker_name).grid(row=0, column=1)
        ttk.Button(self, text='Logout', command=self.logout).grid(row=1, columnspan=2, sticky='we')

        
    def logout(self):
        self.parent.grid_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.grid(pady=20, padx=20)


class Einsatzliste(ttk.Frame):
    def __init__(self, parent, liste_einsatz):
        super().__init__(parent)

        self.parent = parent
        self.liste_einsatz = liste_einsatz

        self.grid(row=1, column=0, pady=5, padx=5, sticky='nw')
        ttk.Label(self, text='Einsatzliste').grid()

        # Tabelle aller Einsätze
        self.tabel_einsatz = ttk.Treeview(master=self, columns=('id', 'stichwort', 'strasse', 'status'), show='headings')
        self.tabel_einsatz.grid(row=1)
        self.tabel_einsatz.heading('id', text='Nr.')
        self.tabel_einsatz.heading('stichwort', text='Stichwort')
        self.tabel_einsatz.heading('strasse', text='Straße')
        self.tabel_einsatz.heading('status', text='Status')

        self.tabel_einsatz.bind('<<TreeviewSelect>>', self.item_selection)

        # Alle Einsätze in Tabelle schreiben
        # ToDo: Lesen der Daten aus einer Datenbank z.B. MongoDB
        for einsatz in liste_einsatz:
            self.tabel_einsatz.insert(parent='', index='end', values=(
                einsatz['id'],
                einsatz['stichwort'],
                einsatz['strasse'],
                einsatz['status']                 
            ))
        
    def item_selection(self, _):
        selection = self.tabel_einsatz.selection()
        id = self.tabel_einsatz.item(selection[0])['values'][0]
        self.parent.parent.arbeitsbereich.update_tabel(id)


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
        self.login_btn = ttk.Button(master=self, text='Login', command=self.login_event).pack(padx=5, pady=5)
    
    def login_event(self):
        user_login = self.user_login_entry.get()
        if user_login:
            self.grid_forget()
            self.user_login = user_login
            self.parent.user_login.set(user_login)
            self.main.grid(pady=10, padx=10)
        else:
            ttk.Label(self, text='enter a valid name', style='warning').pack(pady=(0, 5), padx=20)
    

if __name__ == "__main__":
    app = App()
    app.mainloop()