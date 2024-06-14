import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import json


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
        
        # Name der Organisation
        self.label_einzelplatznutzung = ttk.Label(self, text='Einzelplatznutzung')
        self.einzelplatznutzung = tk.BooleanVar(self, self.settings['einzelplatznutzung'])
        self.switch_einzelplatznutzung = ctk.CTkSwitch(self, text='', variable=self.einzelplatznutzung, onvalue=True, offvalue=False, command=self.update_view)
        
        # Datenbankangaben
        self.db_frame = ttk.Frame(self)
        self.label_db_user = ttk.Label(self.db_frame, text='MongoDB: Nutzername')
        self.db_user = tk.StringVar(self.db_frame, self.settings['db_user'])
        self.entry_db_user = ctk.CTkEntry(self.db_frame, textvariable=self.db_user, width=self.entry_width)
        
        self.label_db_user_password = ttk.Label(self.db_frame, text='MongoDB: Nutzerpasswort')
        self.db_user_password = tk.StringVar(self.db_frame, self.settings['db_user_password'])
        self.entry_db_user_password = ctk.CTkEntry(self.db_frame, textvariable=self.db_user_password, width=self.entry_width)
        
        self.label_db_ip = ttk.Label(self.db_frame, text='MongoDB: IP')
        self.db_ip = tk.StringVar(self.db_frame, self.settings['db_ip'])
        self.entry_db_ip = ctk.CTkEntry(self.db_frame, textvariable=self.db_ip, width=self.entry_width)
        
        self.label_db_port = ttk.Label(self.db_frame, text='MongoDB: Port')
        self.db_port = tk.StringVar(self.db_frame, self.settings['db_port'])
        self.entry_db_port = ctk.CTkEntry(self.db_frame, textvariable=self.db_port, width=self.entry_width)
        
        self.label_db_name = ttk.Label(self.db_frame, text='MongoDB: Datenbankname')
        self.db_name = tk.StringVar(self.db_frame, self.settings['db_name'])
        self.entry_db_name = ctk.CTkEntry(self.db_frame, textvariable=self.db_name, width=self.entry_width)
        
        self.label_update_intervall = ttk.Label(self.db_frame, text='Aktualisierungsintervall [ms]')
        self.update_intervall = tk.IntVar(self.db_frame, self.settings['update_intervall'])
        self.entry_update_intervall = ctk.CTkEntry(self.db_frame, textvariable=self.update_intervall, width=self.entry_width)
                
        self.label_zeitschwelle_einsatz_ohne_bearbeitung = ttk.Label(self, text='Zeitschwelle Einsatzliste [Min]')
        self.zeitschwelle_einsatz_ohne_bearbeitung = tk.IntVar(self, self.settings['zeitschwelle_einsatz_ohne_bearbeitung'])
        self.entry_zeitschwelle_einsatz_ohne_bearbeitung = ctk.CTkEntry(self, textvariable=self.zeitschwelle_einsatz_ohne_bearbeitung, width=self.entry_width)
        
        self.label_absender = ttk.Label(self, text='Neustart erfoerderlich.', style='danger')
        self.absender = tk.BooleanVar(self, self.settings['absender'])
        self.check_absender = ctk.CTkSwitch(self, text='Absender erfassen', variable=self.absender, onvalue=True, offvalue=False, command=self.zeige_neustart)
        
        self.empfanger = tk.BooleanVar(self, self.settings['empfaenger'])
        self.check_empfanger = ctk.CTkSwitch(self, text='Empfänger erfassen', variable=self.empfanger, onvalue=True, offvalue=False, command=self.zeige_neustart)
        
        # Elemente ausrichten
        #self.columnconfigure(1, weight=1)
        
        self.label_orga.grid(row=11, column=0, padx=5,  pady=(5,0),sticky='w')
        self.entry_name_orga.grid(row=11, column=1, padx=5, pady=(5,0),sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=20, columnspan=2, sticky='we', pady=20)
        
        self.label_einzelplatznutzung.grid(row=21, column=0, padx=5, sticky='w')
        self.switch_einzelplatznutzung.grid(row=21, column=1, padx=5, sticky='w')        
        
        ttk.Separator(self, orient='horizontal').grid(row=30, columnspan=2, sticky='we', pady=20)
        
        self.update_view()
        
        self.label_db_user.grid(row=31, column=0, padx=5, sticky='w')
        self.entry_db_user.grid(row=31, column=1, padx=5, sticky='w')
        self.label_db_user_password.grid(row=32, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_user_password.grid(row=32, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_db_ip.grid(row=33, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_ip.grid(row=33, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_db_port.grid(row=34, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_port.grid(row=34, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_db_name.grid(row=35, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_db_name.grid(row=35, column=1, padx=5,  pady=(5,0), sticky='w')
        self.label_update_intervall.grid(row=36, column=0, padx=5,  pady=(5,0), sticky='w')
        self.entry_update_intervall.grid(row=36, column=1, padx=5,  pady=(5,0), sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=40, columnspan=2, sticky='we', pady=20)
        
        self.label_zeitschwelle_einsatz_ohne_bearbeitung.grid(row=41, column=0, padx=5, sticky='w')
        self.entry_zeitschwelle_einsatz_ohne_bearbeitung.grid(row=41, column=1, padx=5, sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=50, columnspan=2, sticky='we', pady=20)
        
        self.check_absender.grid(row=51, column=1, sticky='w')
        self.check_empfanger.grid(row=52, column=1, pady=(5,0), sticky='w')
        
        ttk.Separator(self, orient='horizontal').grid(row=100, columnspan=2, sticky='we', pady=20)
        
        self.btn_save.grid(row=101, column=0, padx=5, pady=10, sticky='e')
    
    def zeige_neustart(self):
        self.label_absender.grid(row=51, column=0, rowspan=2, sticky='w')
    
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
        self.settings['einzelplatznutzung'] = self.einzelplatznutzung.get()
        
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
        
        self.pack_forget()
    
    def pack_me(self):
        self.pack(pady=5, padx=5, fill='both', expand=True)
    
    def update_view(self):
        if self.einzelplatznutzung.get():
            self.db_frame.grid_forget()
        else:
            self.db_frame.grid(row=31, column=0, columnspan=2, padx=5, sticky='news')