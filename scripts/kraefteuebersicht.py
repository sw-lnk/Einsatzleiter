import os
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime
from pymongo import ReturnDocument

class Kraefteuebersicht(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db
        self.parent = parent
        self.einstellungen = parent.einstellungen

        self.label = ttk.Label(self, text='Kräfteübersicht', style='bolt')
        
        # Übersichtstabelle
        self.headings = ['funkrufname', 'kraft', 'anmerkung']
        self.table = ttk.Treeview(master=self, columns=self.headings, displaycolumns=self.headings, show='headings')
        for head in self.headings:
            self.table.heading(head, text=head.capitalize(), anchor='w')
            self.table.column(head) # width=120, minwidth=100, stretch=False
        self.table.bind('<<TreeviewSelect>>', self.item_selection)
        
        self.bearbeitungsmakse = Bearbeitungsmaske(self)
        
        # Gesamtübersicht
        self.vf_ges = tk.IntVar(self, 0)
        self.zf_ges = tk.IntVar(self, 0)
        self.gf_ges = tk.IntVar(self, 0)
        self.ms_ges = tk.IntVar(self, 0)
        self.fzg_ges = tk.IntVar(self, 0)
        self.anzeige_ges1 = tk.StringVar(self)
        self.anzeige_ges2 = tk.StringVar(self)
        
        self.label_frame = ttk.Frame(self)
        self.label_ges1 = ttk.Label(self.label_frame, textvariable=self.anzeige_ges1, font={'size':20})
        self.label_ges2 = ttk.Label(self.label_frame, textvariable=self.anzeige_ges2, font={'size':20})
        self.f = font.Font(self.label_ges2, self.label_ges2.cget("font"))
        self.f.configure(underline=True)
        self.label_ges2.configure(font=self.f)
            
        # Elemente ausrichten
        self.columnconfigure(1, weight=1)
        self.label.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='n')
        self.table.grid(row=2, column=1, padx=5, pady=5, sticky='news')
        self.bearbeitungsmakse.grid(row=2, column=2, padx=5, pady=5, sticky='news')
        self.label_frame.grid(row=3, column=1, sticky='n')
        
        self.label_ges1.grid(row=1, column=1, sticky='ne', pady=10, padx=(5,0))
        self.label_ges2.grid(row=1, column=2, sticky='nw', pady=10, padx=(0,5))
        
        
        self.loop()      
        

    def loop(self):
        self.after(self.einstellungen.update_intervall.get(), self.loop)
        self.fill_table()
    
    def pack_me(self):
        self.pack(pady=5, padx=5, fill='both', expand=True)
        
    def fill_table(self):
        self.clear_table()
        
        krafte = self.db.krafte.find()
        
        vf_ges = 0
        zf_ges = 0
        gf_ges = 0
        ms_ges = 0
        fzg_ges = 0
        
        for i, kraft in enumerate(krafte):
            row_tag = 'even' if (i%2==0) else 'odd'
            values = list(kraft.values())
            funk = values[1]
            vf = values[2]
            zf = values[3]
            gf = values[4]
            ms = values[5]
            anmerkung = values[6]
            zeile = (funk, f'{vf}/{zf}/{gf}/{ms}', anmerkung)
            self.table.insert(parent='', index='end', values=zeile, tags=(row_tag,))
            
            vf_ges += int(vf)
            zf_ges += int(zf)
            gf_ges += int(gf)
            ms_ges += int(ms)
            fzg_ges += 1
        
        self.vf_ges.set(vf_ges)
        self.zf_ges.set(zf_ges)
        self.gf_ges.set(gf_ges)
        self.ms_ges.set(ms_ges)
        self.fzg_ges.set(fzg_ges)
        gesamt = vf_ges+zf_ges+gf_ges+ms_ges
        self.anzeige_ges1.set(f'{vf_ges} / {zf_ges} / {gf_ges} / {ms_ges} / ')
        self.anzeige_ges2.set(gesamt)
    
    def clear_table(self):
        for element in self.table.get_children():
            self.table.delete(element)
            
    def item_selection(self, _):
        selection = self.table.selection()        
        if selection:            
            values = self.table.item(selection[0])['values']
            kraft = [int(x) for x in values[1].split('/')]
            
            self.bearbeitungsmakse.anmerkung_entry.delete(0, 'end')
            self.bearbeitungsmakse.anmerkung_entry.insert(0, values[2])
            
            self.bearbeitungsmakse.funkrufname_entry.delete(0, 'end')
            self.bearbeitungsmakse.funkrufname_entry.insert(0, values[0])
            
            self.bearbeitungsmakse.verbandsfuhrer.current(kraft[0])
            self.bearbeitungsmakse.zugfuhrer.current(kraft[1])
            self.bearbeitungsmakse.gruppenfuhrer.current(kraft[2])
            self.bearbeitungsmakse.mannschaft.current(kraft[3])
            
            #self.bearbeitungsmakse.btn_new.configure(state='disabel', fg_color='grey')
        else:
            pass
            #self.bearbeitungsmakse.btn_new.configure(state='normal', fg_color=self.bearbeitungsmakse.btn_save.cget('fg_color'))


class Bearbeitungsmaske(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db
        self.parent = parent

        # Eingabe Elemente
        #self.funkrufname = tk.StringVar(self)
        self.funkrufname_entry = ctk.CTkEntry(self, placeholder_text='Funkrufname')
        
        #self.anzahl_verbandsfuhrer = tk.IntVar(self, 0)
        self.verbandsfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.verbandsfuhrer.current(0)
        
        #self.anzahl_zugfuhrer = tk.IntVar(self, 0)
        self.zugfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.zugfuhrer.current(0)
        
        #self.anzahl_gruppenfuhrer = tk.IntVar(self, 0)
        self.gruppenfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.gruppenfuhrer.current(0)
        
        #self.anzahl_mannschaft = tk.IntVar(self, 0)
        self.mannschaft = ttk.Combobox(self, values=list(range(1000)), width=8)
        self.mannschaft.current(0)
        
        #self.anmerkung = tk.StringVar(self)
        self.anmerkung_entry = ctk.CTkEntry(self, placeholder_text='Anmerkung')
        
        #self.btn_new = ctk.CTkButton(self, text='Neu')
        self.btn_save = ctk.CTkButton(self, text='Speichern', command=self.speicher_eintrag)
        self.btn_delete = ctk.CTkButton(self, text='Löschen', command=self.entferne_eintrag)
        
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
        # self.btn_new.grid(row=7, column=1, pady=20)
        self.btn_save.grid(row=7, column=3, pady=20)
        self.btn_delete.grid(row=7, column=5, pady=20)
        
    
    def speicher_eintrag(self):
        funk = self.funkrufname_entry.get()
        self.funkrufname_entry.delete(0, 'end')
        
        anmerkung = self.anmerkung_entry.get()
        self.anmerkung_entry.delete(0, 'end')
        
        vf = self.verbandsfuhrer.get()
        self.verbandsfuhrer.current(0)
        
        zf = self.zugfuhrer.get()
        self.zugfuhrer.current(0)
        
        gf = self.gruppenfuhrer.get()
        self.gruppenfuhrer.current(0)
        
        ms = self.mannschaft.get()
        self.mannschaft.current(0)
        
        cnt = self.db.krafte.count_documents({"funkrufname": funk})
        if cnt>0:
            self.db.krafte.find_one_and_update(
                    {'funkrufname': funk},
                    { '$set': {
                        'funkrufname': funk,
                        'vf': vf,
                        'zf': zf,
                        'gf': gf,
                        'ms': ms,
                        'anmerkung': anmerkung,
                        'datum': datetime.datetime.now()
                    }}, 
                    return_document = ReturnDocument.AFTER
                )
        else:
            self.db.krafte.insert_one({
                'funkrufname': funk,
                'vf': vf,
                'zf': zf,
                'gf': gf,
                'ms': ms,
                'anmerkung': anmerkung,
                'datum': datetime.datetime.now()
            })
        
        self.parent.fill_table()
        
    def entferne_eintrag(self):
        funk = self.funkrufname_entry.get()
        
        #ToDo: Abfrage zum löschen einfügen.
        
        self.db.krafte.delete_one({'funkrufname': funk})
        self.parent.fill_table()