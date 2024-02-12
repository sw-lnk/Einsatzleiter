import os
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import json

from scripts.einsatztagebuch import Einsatztagebuch

class Hauptmenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)        
        
        self.parent = parent        
        self.funker_name = parent.user_login
        self.login = parent.login
        
        self.icon_power_path = os.path.join('img','IconPower.png')
        self.icon_power = ttk.PhotoImage(file=self.icon_power_path, width=28, height=28) 
        
        self.disabled_btn = None
        self.disabled_btn_color = None
        self.disabled_btn_hover_color = None
        
        self.columnconfigure(0, weight=1)

        self.anwendungen = ttk.Frame(self)
        self.btn_settings = ctk.CTkButton(self.anwendungen, text='Einstellungen', command=lambda: self.switch_anwendung(self.parent.einstellungen, self.btn_settings))
        self.btn_funktagebuch = ctk.CTkButton(self.anwendungen, text='Funktagebuch', command=lambda: self.switch_anwendung(self.parent.einsatztagebuch, self.btn_funktagebuch))
        self.btn_kraefteuebersicht = ctk.CTkButton(self.anwendungen, text='Kräfteübersicht', command=lambda: self.switch_anwendung(self.parent.kraefteuebersicht, self.btn_kraefteuebersicht))
        
        self.btn_settings.grid(row=0, column=0, sticky='w', padx=(5,0))
        self.btn_funktagebuch.grid(row=0, column=1, sticky='w', padx=(5,0))
        self.btn_kraefteuebersicht.grid(row=0, column=2, sticky='w', padx=(5,0))
        self.anwendungen.grid(row=0, column=0, sticky='w')
        
        
        self.logout_frame = ttk.Frame(self)
        ttk.Label(self.logout_frame, text='Angemeldet: ').grid(row=0, column=0, sticky='e')
        ttk.Label(self.logout_frame, textvariable=self.funker_name).grid(row=0, column=1, sticky='e')
        ctk.CTkButton(self.logout_frame, text='Logout', command=self.logout).grid(row=0, column=3, sticky='e', padx=5)
        self.logout_frame.grid(row=0, column=1, sticky='ne')
        
    def logout(self):
        aktuelle_anwendung=self.parent.aktuelle_anwendung
        self.pack_forget()
        if aktuelle_anwendung:
            aktuelle_anwendung.pack_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.pack_me()

    def pack_me(self):
        self.pack(pady=5, padx=5, fill='x')

    def switch_anwendung(self, anwendung, btn):
        self.enable_btn()                
        self.disable_btn(btn)

        self.parent.aktuelle_anwendung.pack_forget()

        self.parent.aktuelle_anwendung = anwendung
        
        self.parent.aktuelle_anwendung.pack_me()

    def disable_btn(self, btn):
        self.disabled_btn = btn
        self.disabled_btn_color = btn.cget('fg_color')
        self.disabled_btn.configure(state='disable', fg_color='grey')
    
    def enable_btn(self):
        if self.disabled_btn:
            self.disabled_btn.configure(state='normal', fg_color=self.disabled_btn_color)


class Login(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)        
        
        self.parent = parent
        self.pack_me()        

        ttk.Label(master=self, text='Benutzeranmeldung', style='info', font='bold').pack()
        
        self.user_login = None
        self.user_login_entry = ctk.CTkEntry(master=self, placeholder_text='Vorname Nachname')
        self.user_login_entry.bind('<Return>', self.login_event)

        self.user_login_entry.pack(padx=(5,5), pady=5, expand=True, fill='both')
        self.login_btn = ctk.CTkButton(master=self, text='Login', command=lambda: self.login_event(tk.Event)).pack(padx=5, pady=5, expand=True, fill='both')
    
    def login_event(self, _):
        user_login = self.user_login_entry.get()
        if user_login:
            self.pack_forget()
            self.user_login = user_login
            self.parent.user_login.set(user_login)
            self.parent.hauptmenu.pack_me()
            
            if self.parent.aktuelle_anwendung:
                self.parent.aktuelle_anwendung.pack_me()

        else:
            ttk.Label(self, text='enter a valid name', style='warning').pack(pady=(0, 5), padx=20)
    
    def pack_me(self) -> None:
        self.pack(pady=20, padx=20, expand=True)
        

class Einstellungen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
        with open('settings.json', 'r') as f:
            self.settings = json.load(f)
        
        self.entry_width = 300
        
        self.btn_save = ctk.CTkButton(self, text='Speichern', command=self.save_settings)
        
        # Name der Organisation
        self.label_orga = ttk.Label(self, text='Name der Organisation')
        self.orga_name = tk.StringVar(self, self.settings['name_organisation'])
        self.entry_name_orga = ctk.CTkEntry(self, textvariable=self.orga_name, width=self.entry_width)
        
        # Datenbankangaben
        self.label_db_user = ttk.Label(self, text='Nutzer MongoDB')
        self.db_user = tk.StringVar(self, self.settings['db_user'])
        self.entry_db_user = ctk.CTkEntry(self, textvariable=self.db_user, width=self.entry_width)
        
        self.label_db_user_password = ttk.Label(self, text='Nutzer MongoDB')
        self.db_user_password = tk.StringVar(self, self.settings['db_user_password'])
        self.entry_db_user_password = ctk.CTkEntry(self, textvariable=self.db_user_password, width=self.entry_width)
        
        self.label_db_ip = ttk.Label(self, text='MongoDB IP')
        self.db_ip = tk.StringVar(self, self.settings['db_ip'])
        self.entry_db_ip = ctk.CTkEntry(self, textvariable=self.db_ip, width=self.entry_width)
        
        self.label_db_port = ttk.Label(self, text='MongoDB Port')
        self.db_port = tk.StringVar(self, self.settings['db_port'])
        self.entry_db_port = ctk.CTkEntry(self, textvariable=self.db_port, width=self.entry_width)
        
        self.label_db_name = ttk.Label(self, text='Datenbankname')
        self.db_name = tk.StringVar(self, self.settings['db_name'])
        self.entry_db_name = ctk.CTkEntry(self, textvariable=self.db_name, width=self.entry_width)
        
        self.label_update_intervall = ttk.Label(self, text='Aktualisierungsintervall [ms]')
        self.update_intervall = tk.IntVar(self, self.settings['update_intervall'])
        self.entry_update_intervall = ctk.CTkEntry(self, textvariable=self.update_intervall, width=self.entry_width)
                
        self.label_zeitschwelle_einsatz_ohne_bearbeitung = ttk.Label(self, text='Zeitschwelle Einsatzliste [Min]')
        self.zeitschwelle_einsatz_ohne_bearbeitung = tk.IntVar(self, self.settings['zeitschwelle_einsatz_ohne_bearbeitung'])
        self.entry_zeitschwelle_einsatz_ohne_bearbeitung = ctk.CTkEntry(self, textvariable=self.zeitschwelle_einsatz_ohne_bearbeitung, width=self.entry_width)
        
        self.absender = tk.BooleanVar(self, self.settings['absender'])
        self.check_absender = ctk.CTkCheckBox(self, text='Absender erfassen', variable=self.absender)
        
        self.empfanger = tk.BooleanVar(self, self.settings['empfaenger'])
        self.check_empfanger = ctk.CTkCheckBox(self, text='Empfänger erfassen', variable=self.empfanger)
        
        # Elemente ausrichten
        #self.columnconfigure(1, weight=1)
        
        self.label_orga.grid(row=1, column=0, padx=5,  pady=(5,0),sticky='w')
        self.entry_name_orga.grid(row=1, column=1, padx=5, pady=(5,0),sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=2, columnspan=2, sticky='we', pady=20)
        
        self.label_db_user.grid(row=3, column=0, padx=5, sticky='w')
        self.entry_db_user.grid(row=3, column=1, padx=5, sticky='w')
        self.label_db_user_password.grid(row=4, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_user_password.grid(row=4, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_db_ip.grid(row=5, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_ip.grid(row=5, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_db_port.grid(row=6, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_port.grid(row=6, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_db_name.grid(row=7, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_name.grid(row=7, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_update_intervall.grid(row=8, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_update_intervall.grid(row=8, column=1, padx=5,  pady=(5,0), sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=9, columnspan=2, sticky='we', pady=20)
        
        self.label_zeitschwelle_einsatz_ohne_bearbeitung.grid(row=10, column=0, padx=5, sticky='w')
        self.entry_zeitschwelle_einsatz_ohne_bearbeitung.grid(row=10, column=1, padx=5, sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=11, columnspan=2, sticky='we', pady=20)
        
        self.check_absender.grid(row=12, column=1, sticky='w')
        self.check_empfanger.grid(row=13, column=1, pady=(5,0), sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=14, columnspan=2, sticky='we', pady=20)
        
        self.btn_save.grid(row=99, column=0, padx=5, pady=10, sticky='e')
        
    def save_settings(self):
        self.settings['name_organisation'] = self.orga_name.get()
        self.settings['db_user'] = self.db_user.get()
        self.settings['db_user_password'] = self.db_user_password.get()
        self.settings['db_ip'] = self.db_ip.get()
        self.settings['db_port'] = self.db_port.get()
        self.settings['db_name'] = self.db_name.get()
        self.settings['update_intervall'] = self.update_intervall.get()
        self.settings['zeitschwelle_einsatz_ohne_bearbeitung'] = self.zeitschwelle_einsatz_ohne_bearbeitung.get()
        self.settings['absender'] = self.absender.get()
        self.settings['empfaenger'] = self.empfanger.get()
        
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
        
        self.parent.einsatztagebuch.destroy()
        self.parent.einsatztagebuch = Einsatztagebuch(self.parent, self.parent.user_login, self.parent.db)
        self.parent.einsatztagebuch.einsatzliste.update_table()
        self.parent.einsatztagebuch.eintragliste.update_table()
    
    def pack_me(self) -> None:
        self.pack(pady=20, padx=20, fill='both')