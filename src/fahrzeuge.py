import os
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk

class Fahrzeuge(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text='Fahrzeugübersicht', style='bolt')
        self.label.pack(fill='both', expand=True, anchor='center')

    def pack_me(self):
        self.pack(pady=5, padx=5, fill='both', expand=True)