from pymongo import MongoClient
import tkinter as tk
import ttkbootstrap as ttk
import os
import locale
import ctypes
import datetime

import settings

from src.einsatztagebuch import Einsatztagebuch
from src.menu import Login


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

        # Lade Daten
        self.db = self.connect_database()
        self.letzte_aktualisierung = None
        
        # Login Fenster
        self.login = Login(self)        
        
        # Einsatztagebuch
        self.einsatztagebuch = Einsatztagebuch(self, self.user_login, self.db)
        
        # Loop-Funktion zur Aktualisierung div. Objekte
        self.loop()
    
    def loop(self):
        # Diese Schleife wird alle X Sekunden ausgeführt  
        self.after(settings.update_intervall, self.loop)
        
        if self.check_aktualisierung(self.db, self.letzte_aktualisierung):
            self.letzte_aktualisierung = datetime.datetime.now()
            self.einsatztagebuch.eintragliste.update_table(self.einsatztagebuch.einsatzstelle_arbeit)
            self.einsatztagebuch.einsatzliste.update_table()        
      
    def connect_database(self):
        user = settings.db_user
        pwd = settings.db_user_password
        ip = settings.db_ip
        port = settings.db_port
        db = settings.db_name    
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
