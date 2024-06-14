import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime

from database import verbinde_datenbank
from einstellungen import lese_einstellungen
from einheit import Einheit
from einsatzstelle import Einsatzstelle

class Dashboard(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.parent = parent
        
        self.letztes_update: datetime.datetime = None
        
        self.einstellungen = lese_einstellungen()
        
        self.db = verbinde_datenbank()
        
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
    
    def loop(self) -> None:
        self.after(self.einstellungen['update_intervall'], self.loop)
        if self.check_for_update():
            self.letztes_update = datetime.datetime.now()
            self.update_kraefte()
            self.update_einsatz()
    
    def update_kraefte(self) -> None:
        alle_einheiten = self.db.query(Einheit).all()
        
        vf_ges = zf_ges = gf_ges = ms_ges = agt_ges = 0
        
        for _, kraft in enumerate(alle_einheiten):
            vf_ges += kraft.vf
            zf_ges += kraft.zf
            gf_ges += kraft.gf
            ms_ges += kraft.ms
            agt_ges += kraft.agt
        
        self.var_kraefte_fkt.set(f'{vf_ges} / {zf_ges} / {gf_ges} / {ms_ges} / ')
        self.var_kraefte_ges.set(str(vf_ges+zf_ges+gf_ges+ms_ges))
    
    def update_einsatz(self) -> None:
        cnt_unbearbeitet = self.db.query(Einsatzstelle).filter(Einsatzstelle.status == "unbearbeitet").count()
        cnt_in_arbeit = self.db.query(Einsatzstelle).filter(Einsatzstelle.status == "in Arbeit").count()
        self.var_est_unbearbeitet.set(cnt_unbearbeitet)
        self.var_est_in_arbeit.set(cnt_in_arbeit)
    
    def time_loop(self) -> None:
        self.after(5000, self.time_loop)
        jetzt = datetime.datetime.now()
        if self.var_jetzt_einfach.get() != jetzt.strftime(self.format_einfach):            
            self.var_jetzt_einfach.set(jetzt.strftime(self.format_einfach))
            self.var_jetzt_einsatz.set(jetzt.strftime(self.format_einsatz))
    
    def pack_me(self) -> None:
        self.einstellungen = lese_einstellungen()
        self.db = verbinde_datenbank()
        self.update_kraefte()
        self.update_einsatz()
        self.pack(pady=5, padx=5, fill='both', expand=True)
    
    def check_for_update(self) -> bool:
        if self.letztes_update is None:
            return True
        elif not self.einstellungen['einzelplatznutzung']:
            cnt1 = self.db.query(Einsatzstelle).filter(Einsatzstelle.letztes_update > self.letztes_update).count()
            cnt2 = self.db.query(Einheit).filter(Einheit.zeitstempel > self.letztes_update).count()
            cnt = cnt1 + cnt2
            if cnt > 0:
                return True        
        return False
 