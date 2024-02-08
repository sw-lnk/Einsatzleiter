import os
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
from PIL import Image

class Hauptmenu(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)        
        
        self.parent = parent        
        self.funker_name = user
        self.login = parent.parent.login
        
        self.icon_power_path = os.path.join('img','IconPower.png')
        self.icon_power = ttk.PhotoImage(file=self.icon_power_path, width=28, height=28)
        # self.icon_power = Image.open(fp=self.icon_power_path)        
        
        ttk.Label(self, text='Angemeldet: ').grid(row=0, column=0)
        ttk.Label(self, textvariable=self.funker_name).grid(row=0, column=1)
        ctk.CTkButton(self, text='Logout', command=self.logout).grid(row=0, column=3, sticky='e', padx=5)
        
    def logout(self):
        self.parent.pack_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.login_pack()


class Login(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)        
        
        self.parent = parent
        self.login_pack()
        

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
            self.parent.einsatztagebuch.pack(pady=(0,10), padx=10, expand=True, fill='both')
        else:
            ttk.Label(self, text='enter a valid name', style='warning').pack(pady=(0, 5), padx=20)
    
    def login_pack(self) -> None:
        self.pack(pady=20, padx=20, expand=True)