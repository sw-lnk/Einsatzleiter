import os
import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime
import fpdf
from pymongo import ReturnDocument, MongoClient
import json
import sqlite3

class Dashboard(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        
        self.letztes_update: datetime.datetime = None
        
        self.einstellungen = self.lese_einstellungen()
        
        self.db = self.verbinde_datenbank()
        
        self.jetzt = datetime.datetime.now()
        self.format_einfach = '%d.%m.%Y - %H:%M'
        self.jetzt_einfach = self.jetzt.strftime(self.format_einfach)
        self.format_einsatz = '%d %H %M %b %y'
        self.jetzt_einsatz = self.jetzt.strftime(self.format_einsatz)
        
        self.var_jetzt_einfach = tk.StringVar(self, self.jetzt_einfach)
        self.var_jetzt_einsatz = tk.StringVar(self, self.jetzt_einsatz)
        
        self.frame_est = ttk.Frame(self)
        
        self.label_datum_einfach = ctk.CTkLabel(
            self,
            textvariable=self.var_jetzt_einfach,
            #text_color='red',
            font=(None, 50),
        )
        
        self.label_datum_einsatz = ctk.CTkLabel(
            self,
            textvariable=self.var_jetzt_einsatz,
            text_color='blue',
            font=(None, 30),
        )
        
        self.var_est_unbearbeitet = tk.IntVar(self, 0)
        self.label_est_unbearbeitet = ctk.CTkLabel(
            self.frame_est, 
            textvariable=self.var_est_unbearbeitet,
            anchor='center',
            fg_color='red',
            text_color='white',
            corner_radius=10,
            font=(None, 100),
            padx=10
        )
        
        self.var_est_in_arbeit = tk.IntVar(self, 0)
        self.label_est_in_arbeit = ctk.CTkLabel(
            self.frame_est,
            textvariable=self.var_est_in_arbeit,
            anchor='center',
            fg_color='orange',
            text_color='white',
            corner_radius=10,
            font=(None, 100),
            padx=10
        )
        
        self.label_est_unbearbeitet.pack(pady=10, padx=(10,5), side='left')
        self.label_est_in_arbeit.pack(pady=10, padx=(5,10))
        
        self.var_kraefte_fkt = tk.StringVar(self, '0 / 0 / 0 / 0 / ')
        self.var_kraefte_ges = tk.StringVar(self, '0')
        
        self.frame_kraefte = ttk.Frame(self)
        self.label_kraefte_fkt = ctk.CTkLabel(self.frame_kraefte, textvariable=self.var_kraefte_fkt, font=(None, 40))
        self.label_kraefte_ges = ctk.CTkLabel(self.frame_kraefte, textvariable=self.var_kraefte_ges, font=(None, 40, 'underline'))
        
        self.label_kraefte_fkt.pack(side='left')
        self.label_kraefte_ges.pack()
        
        # Elemente platzieren
        self.label_datum_einfach.pack(pady=(100,0))
        self.label_datum_einsatz.pack()
        self.frame_est.pack(pady=20)
        self.frame_kraefte.pack()        
        
        # Zeit aktualisieren
        self.time_loop()
        
        if not self.einstellungen['einzelplatznutzung']:
            self.loop()    
    
    def loop(self):
        self.after(self.einstellungen['update_intervall'], self.loop)
        if self.check_for_update():
            self.letztes_update = datetime.datetime.now()
            self.update_kraefte()
            self.update_einsatz()
    
    def update_kraefte(self) -> None:
        alle_einheiten = self.lese_datenbank()
        
        vf_ges = zf_ges = gf_ges = ms_ges = agt_ges = 0
        
        for _, kraft in enumerate(alle_einheiten):
            vf = kraft['vf']
            zf = kraft['zf']
            gf = kraft['gf']
            ms = kraft['ms']
            agt = kraft['agt']
            
            vf_ges += int(vf)
            zf_ges += int(zf)
            gf_ges += int(gf)
            ms_ges += int(ms)
            agt_ges += int(agt)
        
        self.var_kraefte_fkt.set(f'{vf_ges} / {zf_ges} / {gf_ges} / {ms_ges} / ')
        self.var_kraefte_ges.set(str(vf_ges+zf_ges+gf_ges+ms_ges))
    
    def update_einsatz(self) -> None:
        if self.einstellungen['einzelplatznutzung']:
            cnt_unbearbeitet = self.db.cursor().execute('''SELECT Count(*) FROM einsatzstellen WHERE status = "unbearbeitet"''').fetchone()[0]
            cnt_in_arbeit = self.db.cursor().execute('''SELECT Count(*) FROM einsatzstellen WHERE status = "in Arbeit"''').fetchone()[0]
        else:
            cnt_unbearbeitet = self.db.einsatzstellen.count_documents({'status': 'unbearbeitet'})
            cnt_in_arbeit = self.db.einsatzstellen.count_documents({'status': 'in Arbeit'})
        
        self.var_est_unbearbeitet.set(cnt_unbearbeitet)
        self.var_est_in_arbeit.set(cnt_in_arbeit)
    
    def time_loop(self):
        self.after(5000, self.time_loop)
        jetzt = datetime.datetime.now()
        if self.var_jetzt_einfach.get() != jetzt.strftime(self.format_einfach):            
            self.var_jetzt_einfach.set(jetzt.strftime(self.format_einfach))
            self.var_jetzt_einsatz.set(jetzt.strftime(self.format_einsatz))
    
    def pack_me(self):
        self.einstellungen = self.lese_einstellungen()
        self.db = self.verbinde_datenbank()
        self.update_kraefte()
        self.update_einsatz()
        self.pack(pady=5, padx=5, fill='both', expand=True)
    
    def lese_einstellungen(self) -> dict:
        with open('settings.json', 'r') as f:
            einstellungen = json.load(f)
        return einstellungen
    
    def check_for_update(self) -> bool:
        if self.letztes_update is None:
            return True
        elif not self.einstellungen['einzelplatznutzung']:
            cnt1 = self.db.krafte.count_documents({'datum': {'$gt': self.letztes_update}})
            cnt2 = self.db.einsatzstellen.count_documents({'letztes_update': {'$gt': self.letztes_update}})
            if cnt1 > 0 or cnt2 > 0:
                return True
        
        return False
    
    def verbinde_datenbank(self):
        if self.einstellungen['einzelplatznutzung']:
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
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS einsatzstellen(
                    _id INTEGER PRIMARY KEY NOT NULL,
                    einsatznr TEXT NOT NULL,
                    stichwort TEXT,
                    anschrift TEXT,
                    status TEXT,
                    datum TIMESTAMP,
                    letztes_update TIMESTAMP,
                    archiv INTEGER
                )
            ''')
            db.commit()
            return db
        else:
            user = self.einstellungen['db_user']
            pwd = self.einstellungen['db_user_password']
            ip = self.einstellungen['db_ip']
            port = self.einstellungen['db_port']
            db = self.einstellungen['db_name']   
            client = MongoClient(f"mongodb://{user}:{pwd}@{ip}:{port}/{db}")
            db = client[self.einstellungen['db_name']]
            return db
 
    def lese_datenbank(self):
        db = self.db
        
        if self.einstellungen['einzelplatznutzung']:
            alle_einheiten_tuple = db.cursor().execute('''SELECT * FROM einheiten''').fetchall()
            alle_einheiten = [
                dict(zip((
                    'funkrufname',
                    'vf',
                    'zf',
                    'gf',
                    'ms',
                    'agt',
                    'anmerkung',
                    'datum'), einheit)) for einheit in alle_einheiten_tuple
            ]
        else:
            alle_einheiten = self.db.krafte.find()
        
        return alle_einheiten
 