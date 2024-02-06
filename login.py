import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk


class Login(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(pady=20, padx=20)
        
        self.parent = parent
        self.main = parent.main

        ttk.Label(master=self, text='Benutzeranmeldung', style='info', font='bold').pack()
        
        self.user_login = None
        self.user_login_entry = ctk.CTkEntry(master=self, placeholder_text='Vorname Nachname')
        self.user_login_entry.bind('<Return>', self.login_event)

        self.user_login_entry.pack(padx=(5,5), pady=5)
        self.login_btn = ctk.CTkButton(master=self, text='Login', command=lambda: self.login_event(tk.Event)).pack(padx=5, pady=5)
    
    def login_event(self, _):
        user_login = self.user_login_entry.get()
        if user_login:
            self.grid_forget()
            self.user_login = user_login
            self.parent.user_login.set(user_login)
            self.main.grid(pady=10, padx=10)
        else:
            ttk.Label(self, text='enter a valid name', style='warning').pack(pady=(0, 5), padx=20)
