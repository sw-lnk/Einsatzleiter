from pymongo import MongoClient
import tkinter as tk
import ttkbootstrap as ttk
import os
import locale
import ctypes
import datetime

from scripts.einsatztagebuch import Einsatztagebuch
from scripts.menu import Login, Hauptmenu, Einstellungen
from scripts.kraefteuebersicht import Kraefteuebersicht


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        
        # Grundeinstellungen des Fensters        
        self.screen_factor = 0.9
        self.w = int(self.winfo_screenwidth()*self.screen_factor)
        self.h = int(self.winfo_screenheight()*self.screen_factor)
        self.geometry(f'{self.w}x{self.h}')
        self.title("Funktagebuch")

        self.main_icon_path = os.path.join('img', 'einsatzleiter.png')
        self.main_icon = tk.PhotoImage(file=self.main_icon_path)
        self.iconphoto(False, self.main_icon)

        self.user_system = tk.StringVar(value=os.getlogin())
        self.user_login = tk.StringVar()                

        # Login Fenster
        self.login = Login(self)        
        
        # Hauptmenü
        self.hauptmenu = Hauptmenu(self)
        
        # Einstellungsmenü
        self.einstellungen = Einstellungen(self)

        # Lade Daten
        self.db = self.connect_database()
        self.letzte_aktualisierung = None
        
        # Einsatztagebuch
        self.einsatztagebuch = Einsatztagebuch(self, self.user_login, self.db)

        # Fahrzeugübersicht
        self.kraefteuebersicht = Kraefteuebersicht(self)

        # Aktive Anwendung
        self.aktuelle_anwendung = self.einsatztagebuch
        
        # Loop-Funktion zur Aktualisierung div. Objekte
        self.loop()
    
    def loop(self):
        # Diese Schleife wird alle X Sekunden ausgeführt  
        self.after(self.einstellungen.update_intervall.get(), self.loop)
        
        if self.check_aktualisierung(self.db, self.letzte_aktualisierung):
            self.letzte_aktualisierung = datetime.datetime.now()
            self.einsatztagebuch.eintragliste.update_table(self.einsatztagebuch.einsatzstelle_arbeit)
            self.einsatztagebuch.einsatzliste.update_table()

    def connect_database(self):
        user = self.einstellungen.db_user.get()
        pwd = self.einstellungen.db_user_password.get()
        ip = self.einstellungen.db_ip.get()
        port = self.einstellungen.db_port.get()
        db = self.einstellungen.db_name.get()    
        client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")
        db = client.einsatztagebuch    
        return db
    
    def check_aktualisierung(self, db, letzte_aktualisierung) -> bool:
        einsatzstellen = db.einsatzstellen.find()
        for einsatz in einsatzstellen:
            letztes_update = einsatz['letztes_update']

            if letzte_aktualisierung == None:
                return True
            elif (letztes_update > letzte_aktualisierung):                
                return True
    
        return False


if os.name == 'nt':
    myappid = 'sw-lnk.einsatzleiter.v0.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)   

    # Einstellung zu verwendung vom Dezimaltrennzeichen
    # original_locale = locale.getlocale(locale.LC_NUMERIC)
    locale.setlocale(locale.LC_NUMERIC, "C")
    # locale.setlocale(locale.LC_NUMERIC, original_locale)


if __name__ == "__main__":
    app = App()
    app.mainloop()
