import ttkbootstrap as ttk
import customtkinter as ctk

class Hauptmenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)        
        
        self.parent = parent
        self.login = parent.parent.login
        self.funker_name = parent.parent.user_login
        
        ttk.Label(self, text='Angemeldet: ').grid(row=0, column=0)
        ttk.Label(self, textvariable=self.funker_name).grid(row=0, column=1)
        ctk.CTkButton(self, text='Logout', command=self.logout).grid(row=1, columnspan=2, sticky='we')
        
    def logout(self):
        self.parent.pack_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.pack(pady=20, padx=20, expand=True)