import os

import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import locale
import ctypes
import json

from src.dashboard import Dashboard
from src.einsatztagebuch import Einsatztagebuch
from src.kraefteuebersicht import Kraefteuebersicht
from src.menu import Einstellungen


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        
        # Grundeinstellungen des Fensters        
        self.screen_factor = 0.9
        self.w = int(self.winfo_screenwidth()*self.screen_factor)
        self.h = int(self.winfo_screenheight()*self.screen_factor)
        self.geometry(f'{self.w}x{self.h}')
        self.title("Einsatzleiter")
        self.wm_title('Einsatzleiter')

        # Icon der Anwendung
        self.main_icon_path = os.path.join('img', 'einsatzleiter.png')
        self.main_icon = tk.PhotoImage(file=self.main_icon_path)
        self.iconphoto(False, self.main_icon)

        # Nutzername: angemeldeten Nutzer des Computers / Eingabe am Arbeitsplatz
        self.user_system = tk.StringVar(self, os.getlogin())
        self.user_login = tk.StringVar(self, 'Benutzername')
        
        # Farben
        self.btn_color_disable = 'grey'
        
        # Einstellungen laden
        with open('settings.json', 'r') as f:
            self.settings = json.load(f)
            
        # Hauptfenster        
        self.hauptfenster = ttk.Frame(self)
        self.dashboard = Dashboard(self.hauptfenster)
        self.einstellungs_fenster = Einstellungen(self.hauptfenster)
        self.einsatztagebuch = Einsatztagebuch(self.hauptfenster, self.user_login)
        self.kraefteuebersicht = Kraefteuebersicht(self.hauptfenster)
        self.list_anwendungen: list[ttk.Frame] = [
            self.dashboard,
            self.einstellungs_fenster,
            self.einsatztagebuch,
            self.kraefteuebersicht,
        ]        

        # Login-Bereich
        self.loginfenster = ttk.Frame(self.hauptfenster)
        ttk.Label(self.loginfenster, text='Benutzeranmeldung', style='info', font='bold').pack()
        self.user_login_entry = ctk.CTkEntry(self.loginfenster, placeholder_text='Vorname Nachname')
        self.user_login_entry.bind('<Return>', self.login)
        self.user_login_entry.pack(padx=(5,5), pady=5, expand=True, fill='both')
        self.login_btn = ctk.CTkButton(self.loginfenster, text='Login', command=lambda: self.login(tk.Event)).pack(padx=5, pady=5, expand=True, fill='both')
        self.loginfenster.pack()
        
        # Kopfleiste
        self.kopfleiste = ttk.Frame(self)
        ttk.Label(self.kopfleiste, textvariable=self.user_login).grid(row=0, column=0, padx=5, pady=2)
        self.btn_logout = ctk.CTkButton(self.kopfleiste, text='Logout', command=self.logout, state='disable', fg_color=self.btn_color_disable)
        self.btn_logout.grid(row=1, column=0, sticky='we', padx=5, pady=(0, 5))
        
        # Seitenleiste
        self.seitenleiste = ttk.Frame(self)
        self.btn_dashboard = ctk.CTkButton(self.seitenleiste, text='Dashboard', command=lambda: self.wechsle_anwendung(self.dashboard))
        self.btn_settings = ctk.CTkButton(self.seitenleiste, text='Einstellungen', command=lambda: self.wechsle_anwendung(self.einstellungs_fenster))
        self.btn_funktagebuch = ctk.CTkButton(self.seitenleiste, text='Funktagebuch', command=lambda: self.wechsle_anwendung(self.einsatztagebuch))
        self.btn_kraefteuebersicht = ctk.CTkButton(self.seitenleiste, text='Kräfteübersicht', command=lambda: self.wechsle_anwendung(self.kraefteuebersicht))
        self.btn_list: list[ctk.CTkButton] = [
            self.btn_dashboard,
            self.btn_funktagebuch,
            self.btn_kraefteuebersicht,
            self.btn_settings
        ]
        
        self.btn_color = self.btn_settings.cget('fg_color')
        
        for btn in self.btn_list:
            btn.pack(fill='x', padx=5, pady=5)
            btn.configure(state='disable', fg_color=self.btn_color_disable)
        
        self.btn_settings.pack(fill='x', padx=5, pady=5, anchor='s', side='left')
        
        # Hauptelemente platzieren
        self.columnconfigure(20, weight=1)
        self.rowconfigure(20, weight=1)        
        self.kopfleiste.grid(row=10, column=20, sticky='ne')
        self.seitenleiste.grid(row=20, column=10, sticky='nws')
        self.hauptfenster.grid(row=20, column=20, sticky='news')
        
        # Loop-Funktion zur Aktualisierung div. Objekte
        #self.loop()
    
    def loop(self):
        # Diese Schleife wird alle X Sekunden ausgeführt  
        self.after(10_000, self.loop)

    def schliesse_anwendungen(self):
        for anwendung in self.list_anwendungen:
            anwendung.pack_forget()
    
    def wechsle_anwendung(self, neue_anwendung) -> None:
        self.schliesse_anwendungen()
        neue_anwendung.pack_me()
    
    def login(self, _):
        user_entry = self.user_login_entry.get()        
        if user_entry:
            self.user_login.set(user_entry)
            self.loginfenster.pack_forget()
            
            self.btn_logout.configure(state='normal', fg_color=self.btn_color)
            for btn in self.btn_list:
                btn.configure(state='normal', fg_color=self.btn_color)
            
            self.dashboard.pack_me()
        
    def logout(self):
        # Login-Maske zurücksetzen
        self.user_login_entry.delete(0, 'end')
        self.user_login.set('Benutzername')
        
        # Alle Anwendungen schließen
        self.schliesse_anwendungen()
        
        # Login-Maske einblenden
        self.loginfenster.pack()
        
        # Alle Button deaktivieren
        self.btn_logout.configure(state='disable', fg_color=self.btn_color_disable)
        for btn in self.btn_list:
            btn.configure(state='disable', fg_color=self.btn_color_disable)


if os.name == 'nt':
    myappid = 'sw-lnk.einsatzleiter.v1.0' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)   

    # Einstellung zu verwendung vom Dezimaltrennzeichen
    # original_locale = locale.getlocale(locale.LC_NUMERIC)
    locale.setlocale(locale.LC_NUMERIC, "C")
    # locale.setlocale(locale.LC_NUMERIC, original_locale)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
