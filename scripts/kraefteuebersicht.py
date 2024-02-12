import os
import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime

class Kraefteuebersicht(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db

        self.label = ttk.Label(self, text='Kräfteübersicht', style='bolt')
        
        # Übersichtstabelle
        self.headings = ['funkrufname', 'kraft', 'anmerkung']
        self.table = ttk.Treeview(master=self, columns=self.headings, displaycolumns=self.headings, show='headings')
        for head in self.headings:
            self.table.heading(head, text=head.capitalize(), anchor='w')
            self.table.column(head) # width=120, minwidth=100, stretch=False
        self.table.bind('<<TreeviewSelect>>', self.item_selection)
        
        self.bearbeitungsmakse = Bearbeitungsmaske(self)
            
        # Elemente ausrichten
        self.columnconfigure(1, weight=1)
        self.label.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='n')
        self.table.grid(row=2, column=1, padx=5, pady=5, sticky='news')
        self.bearbeitungsmakse.grid(row=2, column=2, padx=5, pady=5, sticky='news')
        
        self.fill_table()

    def pack_me(self):
        self.pack(pady=5, padx=5, fill='both', expand=True)
        
    def fill_table(self):
        self.clear_table()
        
        krafte = self.db.krafte.find()
        
        for i, kraft in enumerate(krafte):
            row_tag = 'even' if (i%2==0) else 'odd'
            values = list(kraft.values())
            funk = values[1]
            vb = values[2]
            zf = values[3]
            gf = values[4]
            ms = values[5]
            anmerkung = values[6]
            zeile = (funk, f'{vb}/{zf}/{gf}/{ms}', anmerkung)
            self.table.insert(parent='', index='end', values=zeile, tags=(row_tag,))
    
    def clear_table(self):
        for element in self.table.get_children():
            self.table.delete(element)
            
    def item_selection(self, _):
        selection = self.table.selection()        
        if selection:            
            values = self.table.item(selection[0])['values']
            funk = values[0]
            kraft = [int(x) for x in values[1].split('/')]
            anmerkung = values[2]
            print(funk, kraft, anmerkung)


class Bearbeitungsmaske(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db

        # Eingabe Elemente
        self.funkrufname = tk.StringVar(self)
        self.funkrufname_entry = ctk.CTkEntry(self, textvariable=self.funkrufname, placeholder_text='Funkrufname')
        
        self.anzahl_verbandsfuhrer = tk.IntVar(self, 0)
        self.verbandsfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.verbandsfuhrer.current(self.anzahl_verbandsfuhrer.get())
        
        self.anzahl_zugfuhrer = tk.IntVar(self, 0)
        self.zugfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.zugfuhrer.current(self.anzahl_zugfuhrer.get())
        
        self.anzahl_gruppenfuhrer = tk.IntVar(self, 0)
        self.gruppenfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.gruppenfuhrer.current(self.anzahl_gruppenfuhrer.get())
        
        self.anzahl_mannschaft = tk.IntVar(self, 0)
        self.mannschaft = ttk.Combobox(self, values=list(range(1000)), width=8)
        self.mannschaft.current(self.anzahl_mannschaft.get())
        
        self.anmerkung = tk.StringVar(self)
        self.anmerkung_entry = ctk.CTkEntry(self, textvariable=self.anmerkung, placeholder_text='Anmerkung')
        
        self.btn_text = tk.StringVar(self, 'Speichern')
        self.btn_save = ctk.CTkButton(self, textvariable=self.btn_text)
        self.btn_delete = ctk.CTkButton(self, text='Löschen')
        
        # Elemente ausrichten
        ttk.Label(self, text='Funkrufname').grid(row=1, column=1, columnspan=7, sticky='w')
        self.funkrufname_entry.grid(row=2, column=1, columnspan=7, sticky='we')
        ttk.Label(self, text='Kräftaufstellung').grid(row=3, column=1, columnspan=7, sticky='w')
        self.verbandsfuhrer.grid(row=4, column=1)
        ttk.Label(self, text='/').grid(row=4, column=2)
        self.zugfuhrer.grid(row=4, column=3)
        ttk.Label(self, text='/').grid(row=4, column=4)
        self.gruppenfuhrer.grid(row=4, column=5)
        ttk.Label(self, text='/').grid(row=4, column=6)
        self.mannschaft.grid(row=4, column=7)
        ttk.Label(self, text='Anmerkung').grid(row=5, column=1, columnspan=7, sticky='w')
        self.anmerkung_entry.grid(row=6, column=1, columnspan=7, sticky='we')
        self.btn_save.grid(row=7, column=1, columnspan=3, pady=20)
        self.btn_delete.grid(row=7, column=5, columnspan=3, pady=20)
        
    
    def speicher_eintrag(self):
        pass
    