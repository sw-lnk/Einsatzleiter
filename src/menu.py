import os
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk

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
        self.btn_funktagebuch = ctk.CTkButton(self.anwendungen, text='Funktagebuch', command=lambda: self.switch_anwendung(self.parent.einsatztagebuch, self.btn_funktagebuch))
        self.btn_fahrzeuge = ctk.CTkButton(self.anwendungen, text='Fahrzeuge', command=lambda: self.switch_anwendung(self.parent.fahrzeuge, self.btn_fahrzeuge))
        
        self.btn_funktagebuch.grid(row=0, column=0, sticky='w', padx=(5,0))
        #self.btn_fahrzeuge.grid(row=0, column=1, sticky='w', padx=(5,0))
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