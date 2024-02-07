import ttkbootstrap as ttk
import customtkinter as ctk

class Hauptmenu(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)        
        
        self.parent = parent        
        self.funker_name = user
        self.login = parent.parent.login
        
        ttk.Label(self, text='Angemeldet: ').grid(row=0, column=0)
        ttk.Label(self, textvariable=self.funker_name).grid(row=0, column=1)
        ctk.CTkButton(self, text='Logout', command=self.logout).grid(row=1, columnspan=2, sticky='we')
        
    def logout(self):
        self.parent.pack_forget()
        self.login.user_login_entry.delete(0, 'end')
        self.login.login_pack()