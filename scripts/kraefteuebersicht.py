import os
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime
import fpdf
from pymongo import ReturnDocument
import json
import sqlite3

class Kraefteuebersicht(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.db = self.verbinde_datenbank()
        
        # Alle Kräfte
        self.kraefte: list[dict] = None

        self.label = ttk.Label(self, text='Kräfteübersicht', style='bolt')
        
        # Übersichtstabelle
        self.headings = ['funkrufname', 'kraft', 'agt', 'anmerkung']
        self.table = ttk.Treeview(master=self, columns=self.headings, displaycolumns=self.headings, show='headings')
        for head in self.headings:
            self.table.heading(head, text=head.capitalize(), anchor='w')
        self.table.column('funkrufname', width=140, minwidth=10, stretch=False)
        self.table.column('kraft', width=80, minwidth=10, stretch=False)
        self.table.column('agt', width=40, minwidth=10, stretch=False)
        self.table.column('anmerkung', minwidth=10)
        self.table.bind('<<TreeviewSelect>>', self.item_selection)
        
        # Bearbeitungsmaske
        self.bearbeitungsmaske = ttk.Frame(self)
        self.funkrufname_entry = ctk.CTkEntry(self.bearbeitungsmaske, placeholder_text='Funkrufname')
        
        self.verbandsfuhrer = ttk.Combobox(self.bearbeitungsmaske, values=list(range(100)), width=8)
        self.verbandsfuhrer.current(0)
        
        self.zugfuhrer = ttk.Combobox(self.bearbeitungsmaske, values=list(range(100)), width=8)
        self.zugfuhrer.current(0)
        
        self.gruppenfuhrer = ttk.Combobox(self.bearbeitungsmaske, values=list(range(100)), width=8)
        self.gruppenfuhrer.current(0)
        
        self.mannschaft = ttk.Combobox(self.bearbeitungsmaske, values=list(range(1000)), width=8)
        self.mannschaft.current(0)
        
        self.agt = ttk.Combobox(self.bearbeitungsmaske, values=list(range(1000)), width=8)
        self.agt.current(0)
        
        self.anmerkung_entry = ctk.CTkEntry(self.bearbeitungsmaske, placeholder_text='Anmerkung')
        
        self.btn_leiste = ttk.Frame(self.bearbeitungsmaske)        
        self.btn_save = ctk.CTkButton(self.btn_leiste, text='Speichern', command=self.speicher_eintrag)
        self.btn_delete = ctk.CTkButton(self.btn_leiste, text='Löschen', command=self.entferne_eintrag)
        
        ttk.Label(self.bearbeitungsmaske, text='Funkrufname').grid(row=1, column=1, columnspan=7, sticky='w')
        self.funkrufname_entry.grid(row=2, column=1, columnspan=7, sticky='we')
        ttk.Label(self.bearbeitungsmaske, text='Kräftaufstellung').grid(row=3, column=1, columnspan=7, sticky='w')
        self.verbandsfuhrer.grid(row=4, column=1)
        ttk.Label(self.bearbeitungsmaske, text='/').grid(row=4, column=2)
        self.zugfuhrer.grid(row=4, column=3)
        ttk.Label(self.bearbeitungsmaske, text='/').grid(row=4, column=4)
        self.gruppenfuhrer.grid(row=4, column=5)
        ttk.Label(self.bearbeitungsmaske, text='/').grid(row=4, column=6)
        self.mannschaft.grid(row=4, column=7)
        ttk.Label(self.bearbeitungsmaske, text='Anzahl Atemschutzgeräteträger').grid(row=5, column=1, columnspan=7, sticky='w')
        self.agt.grid(row=6, column=1)
        ttk.Label(self.bearbeitungsmaske, text='Anmerkung').grid(row=7, column=1, columnspan=7, sticky='w')
        self.anmerkung_entry.grid(row=8, column=1, columnspan=7, sticky='we')        
        self.btn_leiste.grid(row=9, column=1, columnspan=7, sticky='news')
        
        self.btn_leiste.columnconfigure(1, weight=1)
        self.btn_delete.grid(row=1, column=1, sticky='e', pady=5)
        self.btn_save.grid(row=1, column=2, sticky='e', pady=5, padx=5)        
        
        # Gesamtübersicht
        self.vf_ges = tk.IntVar(self, 0)
        self.zf_ges = tk.IntVar(self, 0)
        self.gf_ges = tk.IntVar(self, 0)
        self.ms_ges = tk.IntVar(self, 0)
        self.agt_ges = tk.IntVar(self, 0)
        self.fzg_ges = tk.IntVar(self, 0)
        self.anzeige_ges1 = tk.StringVar(self)
        self.anzeige_ges2 = tk.StringVar(self)
        self.anzeige_ges3 = tk.StringVar(self, f'Atemschutzgeräteträger: {self.agt_ges}')
        
        self.label_frame = ttk.Frame(self)
        self.label_ges1 = ttk.Label(self.label_frame, textvariable=self.anzeige_ges1, font={'size':20})
        self.label_ges2 = ttk.Label(self.label_frame, textvariable=self.anzeige_ges2, font={'size':20})
        self.label_ges3 = ttk.Label(self.label_frame, textvariable=self.anzeige_ges3, font={'size':16})
        self.f = font.Font(self.label_ges2, self.label_ges2.cget("font"))
        self.f.configure(underline=True)
        self.label_ges2.configure(font=self.f)
            
        # Elemente ausrichten
        self.columnconfigure(1, weight=1)
        self.label.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='n')
        self.table.grid(row=2, column=1, padx=5, pady=5, sticky='news')
        self.bearbeitungsmaske.grid(row=2, column=2, padx=5, pady=5, sticky='news')
        self.label_frame.grid(row=3, column=1, sticky='n')
        
        self.label_ges1.grid(row=1, column=1, sticky='ne', pady=10, padx=(5,0))
        self.label_ges2.grid(row=1, column=2, sticky='nw', pady=10, padx=(0,5))
        self.label_ges3.grid(row=1, column=3, sticky='ne', pady=10, padx=(30,5))
        
        ctk.CTkButton(self.label_frame, text='Kräftübersicht ausleiten', command=self.create_report).grid(row=2, column=1, columnspan=3, sticky='n', pady=10, padx=(5,5))
        
        #self.loop()      
        

    def loop(self):
        self.after(10_000, self.loop)
        self.fill_table()
    
    def pack_me(self):
        self.pack(pady=5, padx=5, fill='both', expand=True)
    
    def fill_table(self):
        self.clear_table()
        
        vf_ges = 0
        zf_ges = 0
        gf_ges = 0
        ms_ges = 0
        agt_ges = 0
        fzg_ges = 0
        
        for i, kraft in enumerate(self.kraefte):
            row_tag = 'even' if (i%2==0) else 'odd'
            
            funk = kraft['funkrufname']
            vf = kraft['vf']
            zf = kraft['zf']
            gf = kraft['gf']
            ms = kraft['ms']
            agt = kraft['agt']
            anmerkung = kraft['anmerkung']
            
            zeile = (funk, f'{vf}/{zf}/{gf}/{ms}', agt, anmerkung)
            self.table.insert(parent='', index='end', values=zeile, tags=(row_tag,))
            
            vf_ges += int(vf)
            zf_ges += int(zf)
            gf_ges += int(gf)
            ms_ges += int(ms)
            agt_ges += int(agt)
            fzg_ges += 1
        
        self.vf_ges.set(vf_ges)
        self.zf_ges.set(zf_ges)
        self.gf_ges.set(gf_ges)
        self.ms_ges.set(ms_ges)
        self.agt_ges.set(agt_ges)
        self.fzg_ges.set(fzg_ges)
        gesamt = vf_ges+zf_ges+gf_ges+ms_ges
        self.anzeige_ges1.set(f'{vf_ges} / {zf_ges} / {gf_ges} / {ms_ges} / ')
        self.anzeige_ges2.set(gesamt)
        self.anzeige_ges3.set(f'Atemschutzgeräteträger: {agt_ges}')
    
    def clear_table(self):
        for element in self.table.get_children():
            self.table.delete(element)
            
    def verbinde_datenbank(self, einzelplatznutzung:bool=True):
        if einzelplatznutzung:
            db = sqlite3.connect(os.path.join('data', 'db.sqlite3'))
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS einheiten(
                    funkrufname TEXT PRIMARY KEY,
                    vf INTEGER,
                    zf INTEGER,
                    gf INTEGER,
                    ms INTEGER,
                    agt INTEGER,
                    anmerkung TEXT,
                    datum TEXT
                )
            ''')
            db.commit()
            return db
        
    def lese_datenbank(self):
        db = self.db
        einzelplatznutzung:bool=True
        
        if einzelplatznutzung:
            cursor = db.cursor.execute('''SELECT * FROM einheiten''')
            alle_einheiten = cursor.fetchall()
            
    
    def item_selection(self, _):
        selection = self.table.selection()        
        if selection:            
            values = self.table.item(selection[0])['values']
            kraft = [int(x) for x in values[1].split('/')]
            
            self.anmerkung_entry.delete(0, 'end')
            self.anmerkung_entry.insert(0, values[3])
            
            self.funkrufname_entry.delete(0, 'end')
            self.funkrufname_entry.insert(0, values[0])
            
            self.verbandsfuhrer.current(kraft[0])
            self.zugfuhrer.current(kraft[1])
            self.gruppenfuhrer.current(kraft[2])
            self.mannschaft.current(kraft[3])
            self.agt.current(int(values[2]))   
    
    def speicher_eintrag(self):
        db = self.db
        einzelplatznutzung:bool=True
        
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
        
        agt = self.agt.get()
        self.agt.current(0)
        
        einheit = {
            'funkrufname': funk,
            'vf': int(vf),
            'zf': int(zf),
            'gf': int(gf),
            'ms': int(ms),
            'agt': int(agt),
            'anmerkung': anmerkung,
            'datum': datetime.datetime.now()
        }
        
        if einzelplatznutzung:
            cursor = db.cursor()
            cnt = cursor.execute('''SELECT COUNT(funkrufname) FROM einheiten WHERE funkrufname=?''', (funk,))
            cnt = cnt.fetchone
            if cnt is None:
                cursor.execute('''INSERT INTO einheiten(funkrufname, vf, zf, gf, ms, agt, anmerkung, datum)
                  VALUES(?,?,?,?,?,?,?,?)''', tuple(list(einheit.values())))
                db.commit()
            else:
                pass
                # Todo: Datensatz aktualisieren, wenn bereits vorhanden.
        
    def entferne_eintrag(self):
        funk = self.funkrufname_entry.get()        
        res = tk.messagebox.askquestion('Löschen', 'Wirklich löschen?')        
        if res == 'yes':
            print({'funkrufname': funk})
            self.fill_table()

    def create_report(self):        
        pass
        #report = Bericht(self.db.krafte.find(), self.einstellungen.orga_name.get())
            
    
class Bericht(fpdf.FPDF):
    def __init__(self, eintrage, organisation = 'Feuerwehr Musterstadt', orientation = "portrait", unit = "mm", format = "A4", font_cache_dir = "DEPRECATED") -> None:
        super().__init__(orientation, unit, format, font_cache_dir)
        
        self.jetzt = datetime.datetime.now()
        self.jetzt_einfach = self.jetzt.strftime('%d.%m.%Y %H:%M')
        self.jetzt_einsatz = self.jetzt.strftime('%d%H%M%b%y')
        
        self.ordner_name = 'kraefteuebersicht'
        if not os.path.exists(self.ordner_name):
            os.mkdir(self.ordner_name)
        self.path = os.path.join(self.ordner_name, f'{self.jetzt_einsatz}.pdf')
        
        self.organisation = organisation
        
        self.vf_ges = 0
        self.zf_ges = 0
        self.gf_ges = 0
        self.ms_ges = 0
        self.agt_ges = 0
        
        self.add_page()
        
        # Tabelle
        self.spalten = ['Funkrufname', 'Anmerkung', 'VF', 'ZF', 'GF', 'MS', 'Ges', 'AGT']
        self.spalten_breite = [30, 100, 10, 10, 10, 10, 10, 10]
        with self.table(col_widths=tuple(self.spalten_breite)) as table:
            self.row = table.row()
            for cell in self.spalten:
                self.row.cell(cell)
            for eintrag in eintrage:
                self.row = table.row()
                
                vf, zf, gf, ms = eintrag['vf'], eintrag['zf'], eintrag['gf'], eintrag['ms']
                agt = eintrag['agt']
                ges = vf+zf+gf+ms
                
                self.vf_ges += vf
                self.zf_ges += zf
                self.gf_ges += gf
                self.ms_ges += ms
                self.agt_ges += agt
                
                for cell in [eintrag['funkrufname'], eintrag['anmerkung'], eintrag['vf'], eintrag['zf'], eintrag['gf'], eintrag['ms'], ges, agt]:
                    self.row.cell(str(cell), align=fpdf.Align.L)
                
            self.gesamt = self.vf_ges + self.zf_ges + self.gf_ges + self.ms_ges
            self.row = table.row()
            for cell in ['Gesamt', '', self.vf_ges, self.zf_ges, self.gf_ges, self.ms_ges, self.gesamt, self.agt_ges]:
                self.row.cell(str(cell), align=fpdf.Align.L)
        
        
        self.set_font(family="helvetica", style='', size=16)
        self.ln(5)
        self.cell(0, h=10, text=f'{self.vf_ges} / {self.zf_ges} / {self.gf_ges} / {self.ms_ges} / {self.gesamt}', align=fpdf.Align.R)
        self.set_font(style='U')
        self.cell(0, h=10, ln=1, text=str(self.gesamt), align=fpdf.Align.R)
        
        self.set_font(style='', size=12)
        self.cell(0, 10, text=f'Atemschutzgeräteträger: {self.agt_ges}', align=fpdf.Align.R)
        
        # Save pdf
        self.output(self.path)
        
    def header(self):
        # Name der Organisation einfügen
        self.set_y(14)
        self.set_font(family="helvetica", style='B', size=16)
        self.cell(text=self.organisation)
        
        # Einsatzdaten
        self.set_font(style='', size=14)
        self.set_y(10)
        self.cell(0, 10, text='Kräfteübersicht', align=fpdf.Align.C)
        
        # Erstelldatum oben rechts einfügen
        self.set_font(style="", size=10)
        self.set_y(10)
        self.cell(0, 10, text=self.jetzt_einfach, align=fpdf.Align.R)
        self.set_y(15)
        self.cell(0, 10, text=self.jetzt_einsatz, align=fpdf.Align.R)
        self.set_y(35)

    
    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "", 8)
        # Printing page number:
        self.cell(0, 10, f"Kräfteübersicht {self.jetzt_einsatz}", align=fpdf.Align.L)
        self.set_y(-15)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align=fpdf.Align.R)