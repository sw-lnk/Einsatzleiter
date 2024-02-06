from pymongo import MongoClient
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import os
import locale
import ctypes

from einsatztagebuch import Einsatztagebuch
from login import Login


if os.name == 'nt':
    myappid = 'sw-lnk.einsatzleiter.v0.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)   

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

        self.main_icon_path = os.path.join('img', 'einsatzleiter.png')
        self.main_icon = tk.PhotoImage(file=self.main_icon_path)
        self.iconphoto(False, self.main_icon)

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

        self.einsatztagebuch.update_table(self.einsatztagebuch.einsatzstelle_arbeit)
        self.einsatztagebuch.einsatzliste.update_table()        
                

class Hauptfenster(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


class Leiste_Kopf(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)        
        
        self.parent = parent
        self.login = parent.parent.login
        self.funker_name = self.parent.parent.user_login
        
        ttk.Label(self, text='Angemeldet: ').grid(row=0, column=0)
        ttk.Label(self, textvariable=self.funker_name).grid(row=0, column=1)
        ctk.CTkButton(self, text='Logout', command=self.logout).grid(row=1, columnspan=2, sticky='we')

        
    def logout(self):
        self.parent.grid_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.grid(pady=20, padx=20)


def connect_database():
    user = 'user' #input('Username: ')
    pwd = 'user' #getpass('Password: ')
    ip = '192.168.178.41'
    port = '27017'
    db = 'einsatztagebuch'
    
    client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")
    db = client.einsatztagebuch
    
    return db
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
