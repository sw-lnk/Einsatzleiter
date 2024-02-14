import os
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime
import fpdf
from pymongo import ReturnDocument

class Kraefteuebersicht(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db
        self.parent = parent
        self.einstellungen = parent.einstellungen

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
        
        self.bearbeitungsmakse = Bearbeitungsmaske(self)
        
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
        self.bearbeitungsmakse.grid(row=2, column=2, padx=5, pady=5, sticky='news')
        self.label_frame.grid(row=3, column=1, sticky='n')
        
        self.label_ges1.grid(row=1, column=1, sticky='ne', pady=10, padx=(5,0))
        self.label_ges2.grid(row=1, column=2, sticky='nw', pady=10, padx=(0,5))
        self.label_ges3.grid(row=1, column=3, sticky='ne', pady=10, padx=(30,5))
        
        ctk.CTkButton(self.label_frame, text='Kräftübersicht ausleiten', command=self.create_report).grid(row=2, column=1, columnspan=3, sticky='n', pady=10, padx=(5,5))
        
        self.loop()      
        

    def loop(self):
        self.after(self.einstellungen.update_intervall.get(), self.loop)
        self.fill_table()
    
    def pack_me(self):
        self.pack(pady=5, padx=5, fill='both', expand=True)
    
    def create_report(self):        
        report = Bericht(self.db.krafte.find(), self.einstellungen.orga_name.get())
            
    def fill_table(self):
        self.clear_table()
        
        krafte = self.db.krafte.find()
        
        vf_ges = 0
        zf_ges = 0
        gf_ges = 0
        ms_ges = 0
        agt_ges = 0
        fzg_ges = 0
        
        for i, kraft in enumerate(krafte):
            row_tag = 'even' if (i%2==0) else 'odd'
            values = list(kraft.values())
            #print(values)
            funk = values[1]
            vf = values[2]
            zf = values[3]
            gf = values[4]
            ms = values[5]
            agt = values[6]
            anmerkung = values[7]
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
            
    def item_selection(self, _):
        selection = self.table.selection()        
        if selection:            
            values = self.table.item(selection[0])['values']
            kraft = [int(x) for x in values[1].split('/')]
            
            self.bearbeitungsmakse.anmerkung_entry.delete(0, 'end')
            self.bearbeitungsmakse.anmerkung_entry.insert(0, values[3])
            
            self.bearbeitungsmakse.funkrufname_entry.delete(0, 'end')
            self.bearbeitungsmakse.funkrufname_entry.insert(0, values[0])
            
            self.bearbeitungsmakse.verbandsfuhrer.current(kraft[0])
            self.bearbeitungsmakse.zugfuhrer.current(kraft[1])
            self.bearbeitungsmakse.gruppenfuhrer.current(kraft[2])
            self.bearbeitungsmakse.mannschaft.current(kraft[3])
            self.bearbeitungsmakse.agt.current(int(values[2]))
        

class Bearbeitungsmaske(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = parent.db
        self.parent = parent

        # Eingabe Elemente
        self.funkrufname_entry = ctk.CTkEntry(self, placeholder_text='Funkrufname')
        
        self.verbandsfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.verbandsfuhrer.current(0)
        
        self.zugfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.zugfuhrer.current(0)
        
        self.gruppenfuhrer = ttk.Combobox(self, values=list(range(100)), width=8)
        self.gruppenfuhrer.current(0)
        
        self.mannschaft = ttk.Combobox(self, values=list(range(1000)), width=8)
        self.mannschaft.current(0)
        
        self.agt = ttk.Combobox(self, values=list(range(1000)), width=8)
        self.agt.current(0)
        
        self.anmerkung_entry = ctk.CTkEntry(self, placeholder_text='Anmerkung')
        
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
        ttk.Label(self, text='Anzahl Atemschutzgeräteträger').grid(row=5, column=1, columnspan=7, sticky='w')
        self.agt.grid(row=6, column=1)
        ttk.Label(self, text='Anmerkung').grid(row=7, column=1, columnspan=7, sticky='w')
        self.anmerkung_entry.grid(row=8, column=1, columnspan=7, sticky='we')
        
        self.btn_save.grid(row=9, column=3, pady=20)
        self.btn_delete.grid(row=9, column=5, pady=20)
        
    
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
        
        agt = self.agt.get()
        self.agt.current(0)
        
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
                        'agt': agt,
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
                'agt': agt,
                'anmerkung': anmerkung,
                'datum': datetime.datetime.now()
            })
        
        self.parent.fill_table()
        
    def entferne_eintrag(self):
        funk = self.funkrufname_entry.get()
        
        res = tk.messagebox.askquestion('Löschne', 'Wirklich löschen?')
        
        if res == 'yes':
            self.db.krafte.delete_one({'funkrufname': funk})
            self.parent.fill_table()


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
        
        self.add_page()
        
        # Tabelle
        self.spalten = ['Funkrufname', 'Anmerkung', 'VF', 'ZF', 'GF', 'MS', 'Ges', 'AGT']
        self.spalten_breite = [30, 100, 10, 10, 10, 10, 10, 10]
        with self.table(col_widths=tuple(self.spalten_breite)) as table:
            self.row = table.row()
            for cell in self.spalten:
                self.row.cell(cell)
            for eintrag in eintrage:
                row = table.row()
                
                vf, zf, gf, ms = int(eintrag['vf']), int(eintrag['zf']), int(eintrag['gf']), int(eintrag['ms'])
                agt = int(eintrag['agt'])
                ges = vf+zf+gf+ms
                for cell in [eintrag['funkrufname'], eintrag['anmerkung'], eintrag['vf'], eintrag['zf'], eintrag['gf'], eintrag['ms'], str(ges), str(agt)]:
                    row.cell(cell, align=fpdf.Align.L)
        
        #ToDo: Gesamtzahlen drucken
        
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