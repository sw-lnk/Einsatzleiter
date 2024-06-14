import tkinter as tk
import ttkbootstrap as ttk
import customtkinter as ctk
import datetime

from protokoll import Protokoll
from database import verbinde_datenbank
from einstellungen import lese_einstellungen
from einsatzstelle import Einsatzstelle
from eintrag import Eintrag


class Einsatztagebuch(ttk.Frame):
    def __init__(self, parent, nutzer: tk.StringVar):
        super().__init__(parent)

        self.parent = parent
        self.user_login: tk.StringVar = nutzer
        self.nutzer: str = self.user_login.get()
        
        self.einstellungen = lese_einstellungen()
        
        self.db = verbinde_datenbank()      
        
        self.einsatzstelle_arbeit = None
        self.einsatzstelle_focus = None
        self.letztes_update: datetime.datetime = None
        
        # Einsatzübersicht
        self.einsatzliste = ttk.Frame(self)
        # tablele aller Einsätze
        self.headings = ['id', 'datum', 'stichwort', 'anschrift', 'status']
        self.table_einsatz = ttk.Treeview(master=self.einsatzliste, columns=self.headings, displaycolumns=self.headings[1:], show='headings')
        self.table_einsatz.heading('id', text='Nr.')
        self.table_einsatz.heading('datum', text='Einsatzbeginn', anchor='w')
        self.table_einsatz.column('datum', width=120, minwidth=100, stretch=False)
        self.table_einsatz.heading('stichwort', text='Stichwort', anchor='w')
        self.table_einsatz.column('stichwort')
        self.table_einsatz.heading('anschrift', text='Anschrift', anchor='w')
        self.table_einsatz.column('anschrift', width=200)
        self.table_einsatz.heading('status', text='Status', anchor='w')
        self.table_einsatz.column('status', width=120, minwidth=50, stretch=False)
        self.table_einsatz.tag_configure('late', background='red')
        self.table_einsatz.tag_configure('unbearbeitet', background='#ffcccb')
        self.table_einsatz.tag_configure('in Arbeit', background='#ffffe0')
        self.table_einsatz.tag_configure('abgeschlossen', background='#90ee90')
        self.table_einsatz.bind('<<TreeviewSelect>>', self.item_selection)
        
        self.frame_optionen = ttk.Frame(self.einsatzliste)
        
        # Button zur Bearbeitung und Anlage eines Einsatzes
        self.button_neuer_einsatz = ctk.CTkButton(self.frame_optionen, text='Neuer Einsatz', command=self.einsatz_anlegen_maske)
        self.button_update_einsatz = ctk.CTkButton(self.frame_optionen, text='Einsatz aktualisieren', command=self.einsatz_update_maske)
        self.button_einsatz_ausgabe = ctk.CTkButton(self.frame_optionen, text='Protokoll ausleiten', command=self.protokoll_ausleiten)
        
        # Filter Optionen        
        self.check_arbeit_value = tk.IntVar(self.frame_optionen, 1)        
        self.check_arbeit = ttk.Checkbutton(self.frame_optionen, text='Abgeschlossene Einsätze', variable=self.check_arbeit_value, command=self.update_table_einsatz)
        
        self.check_date_value = tk.IntVar(self.frame_optionen, 1)
        self.check_date = ttk.Checkbutton(self.frame_optionen, text='Zeige nur Einsätze nach', variable=self.check_date_value, command=self.update_table_einsatz)
        
        self.datum_anzeige_filter = datetime.date.today() - datetime.timedelta(days=7)
        self.date_filter = ttk.DateEntry(self.frame_optionen, firstweekday=7, startdate=self.datum_anzeige_filter, dateformat='%d.%m.%Y')
        self.date_filter_var = tk.StringVar(self, self.datum_anzeige_filter.strftime('%d.%m.%Y'))
        self.date_filter_var.trace_add('write', lambda *_: self.update_table_einsatz())
        self.date_filter.entry.configure(textvariable=self.date_filter_var)
        
        # Elemente ausrichten
        self.button_neuer_einsatz.pack(padx=5, pady=(5,0), anchor='w')
        self.button_update_einsatz.pack(padx=5, pady=(5,0), anchor='w')
        self.button_einsatz_ausgabe.pack(padx=5, pady=(5,0), anchor='w')
        self.check_date.pack(padx=5, pady=(20,0), anchor='w')
        self.date_filter.pack(padx=5, pady=(5,0), anchor='w')
        self.check_arbeit.pack(padx=5, pady=(20,5), anchor='w')        

        self.einsatzliste.columnconfigure(0, weight=1)
        ttk.Label(self.einsatzliste, text='Einsatzübersicht', font='bold').grid(row=0, column=0)
        self.table_einsatz.grid(row=1, column=0, padx=5, pady=5, sticky='news')
        self.frame_optionen.grid(row=1, column=1, sticky='news')
        
        # Tagebuch je Einsatz
        self.eintragliste = ttk.Frame(self)
        
        # Anzeige ausgewählter Einsatz
        self.label_einsatz_text = tk.StringVar(self.eintragliste, '- Einsatz -')
        self.label_einsatz = ttk.Label(master=self.eintragliste, textvariable=self.label_einsatz_text, style='primary', font='bold')        
        
        # tablele zur Anzeige alle Einträge zum ausgewähltem Einsatz
        self.headings = ['datum', 'eintrag', 'von', 'an', 'funker']
        self.headings_show = ['datum', 'eintrag', 'funker']
        
        if self.einstellungen['absender']:
            self.headings_show.insert(-1, 'von')
        if self.einstellungen['empfaenger']:
            self.headings_show.insert(-1, 'an')
        
        self.table = ttk.Treeview(master=self.eintragliste, columns=self.headings, displaycolumns=self.headings_show, show='headings', height=15)        
        self.table.heading('datum', text='Zeitstempel', anchor='w')
        self.table.column('datum', width=120, minwidth=100, stretch=False)
        self.table.heading('eintrag', text='Eintrag', anchor='w')
        self.table.column('eintrag', minwidth=100)
        self.table.heading('von', text='Absender', anchor='w')
        self.table.column('von',  width=150, minwidth=100, stretch=False)
        self.table.heading('an', text='Empfänger', anchor='w')
        self.table.column('an',  width=150, minwidth=100, stretch=False)
        self.table.heading('funker', text='Bearbeiter', anchor='w')
        self.table.column('funker', width=150, minwidth=100, stretch=False)
        self.table.tag_configure('odd', background='lightblue')
        
        # Rahmen für Eingaben
        self.frame_entry = ttk.Frame(self.eintragliste)
        self.frame_entry.columnconfigure(0, weight=1)
        
        # Eingabe für den nächsten Eintrag im Funktagebuch
        self.entry_funk = ctk.CTkEntry(master=self.frame_entry, placeholder_text='Eintrag Funktagebuch')
        
        # Empfänger und Absender
        self.entry_absender = ctk.CTkEntry(master=self.frame_entry, placeholder_text='Absender')        
        self.entry_empfang = ctk.CTkEntry(master=self.frame_entry, placeholder_text='Empfänger')
        
        # Eingabe erzeugen beim betätigen der Enter-Taste
        self.entry_funk.bind('<Return>', self.add_entry)
        self.entry_absender.bind('<Return>', self.add_entry)
        self.entry_empfang.bind('<Return>', self.add_entry)  
        
        # Button zur Erstellung eines neuen Eintrags
        self.button_absenden = ctk.CTkButton(self.frame_entry, text='Eintragen', command=lambda: self.add_entry(tk.Event()))
        
        # Elemente ausrichten        
        self.label_einsatz.pack(pady=5, padx=5)
        self.table.pack(pady=0, padx=5, fill='both') 
        self.frame_entry.pack(pady=5, padx=5, fill='x')

        # Eingabeelemente anzeigen / ausrichten        
        if self.einstellungen['absender'] or self.einstellungen['empfaenger']:
            ttk.Label(self.frame_entry, text='Eintrag').grid(row=0, column=0, pady=(5, 0))
        if self.einstellungen['absender']:
            ttk.Label(self.frame_entry, text='Absender').grid(row=0, column=1, pady=(5, 0))
            self.entry_absender.grid(row=1, column=1, padx=(5,0), sticky='ew')
        if self.einstellungen['empfaenger']:
            ttk.Label(self.frame_entry, text='Empfänger').grid(row=0, column=2, pady=(5, 0))
            self.entry_empfang.grid(row=1, column=2, padx=(5,0), sticky='ew')      
        
        self.entry_funk.grid(row=1, column=0, padx=(5,0), sticky='ew')        
        self.button_absenden.grid(row=1, column=3, padx=(5,5), sticky='ew')
        
        #Elemente ausrichten
        self.einsatzliste.pack(expand=True, fill='x')
        self.eintragliste.pack(expand=True, fill='x')

        
        if self.einstellungen['einzelplatznutzung']:
            self.update_table_einsatz()
        else:
            self.loop()
           
        
    def loop(self):
        self.after(self.einstellungen['update_intervall'], self.loop)
        if self.check_for_update():
            self.letztes_update = datetime.datetime.now()
            self.update_table_einsatz()
        
    def pack_me(self):  
        self.einstellungen = lese_einstellungen()
        self.nutzer: str = self.user_login.get()
        self.db = verbinde_datenbank()
        self.update_table_tagebuch()
        self.update_table_einsatz()
        self.pack(pady=(0,10), padx=10, expand=True, fill='both')
    
    def check_for_update(self) -> bool:
        if self.letztes_update is None:
            return True
        elif not self.einstellungen['einzelplatznutzung']:
            cnt = self.db.query(Einsatzstelle).filter(Einsatzstelle.letztes_update > self.letztes_update).count()
            if cnt > 0:
                return True        
        return False
    
    def item_selection(self, _):  
        selection = self.table_einsatz.selection()        
        if selection:            
            id_est = self.table_einsatz.item(selection[0])['values'][0]
            id_est = id_est.split(None, maxsplit=1)[1]
            self.einsatzstelle_focus = id_est
            self.update_table_tagebuch(id_est)
        
        else:
            self.einsatzstelle_focus = None

    def protokoll_ausleiten(self):  
        db = self.db        
        selection = self.table_einsatz.selection()
        if selection:
            for sel in selection:
                id_est = self.table_einsatz.item(sel)['values'][0]
                id_est = id_est.split(None, maxsplit=1)[1]
                einsatzstelle = db.query(Einsatzstelle).filter(Einsatzstelle.nr == id_est).first()             
                eintrage = db.query(Eintrag).filter(Eintrag.einsatz_nr == id_est).all()
                Protokoll(
                    einsatz=einsatzstelle,
                    eintrage=eintrage,
                    absender=self.einstellungen['absender'],
                    empfanger=self.einstellungen['empfaenger'],
                    organisation=self.einstellungen['name_organisation']
                )
    
    def einsatz_update_maske(self):  
        db = self.db
        
        selection = self.table_einsatz.selection()
        if selection:
            id_est = self.table_einsatz.item(selection[0])['values'][0]
            id_est = id_est.split(None, maxsplit=1)[1]
            einsatz = db.query(Einsatzstelle).filter(Einsatzstelle.nr == id_est).first()
            
            stichwort = einsatz.stichwort
            nummer = einsatz.nr     
            anschrift = einsatz.anschrift
            status = einsatz.status
            
            eingabe_maske = ttk.Toplevel('Einsatz aktualisieren')
            einsatz_stichwort = ctk.CTkEntry(eingabe_maske)
            einsatz_stichwort.insert(0, stichwort)
            
            einsatz_nummer = ctk.CTkEntry(eingabe_maske)
            einsatz_nummer.insert(0, nummer)
                
            einsatz_anschrift = ctk.CTkEntry(eingabe_maske)
            einsatz_anschrift.insert(0, anschrift)
            
            status_liste = ['unbearbeitet', 'in Arbeit', 'abgeschlossen']
            
            einsatz_status = ctk.CTkComboBox(eingabe_maske, values=status_liste, state='readonly')
            einsatz_status.set(status)
            
            button_abbruch = ctk.CTkButton(eingabe_maske, text="Abbrechen", command=eingabe_maske.destroy)
            button_update = ctk.CTkButton(
                eingabe_maske,
                text="Einsatz aktualisieren",
                command= lambda: self.einsatz_update_schreiben(
                    id_est,
                    einsatz_nummer.get(),
                    einsatz_status.get(),
                    einsatz_stichwort.get(),
                    einsatz_anschrift.get(),
                    eingabe_maske
                    )
                )
        
            # Elemente ausrichten
            einsatz_stichwort.grid(row=1, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            einsatz_nummer.grid(row=2, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            einsatz_anschrift.grid(row=3, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            einsatz_status.grid(row=4, column=1, pady=5, padx=5, columnspan=2, sticky='we')
            button_abbruch.grid(row=5, column=1, pady=5, padx=5)
            button_update.grid(row=5, column=2, pady=5, padx=5)
    
    def einsatz_update_schreiben(self, nr_alt, nr_neu, status, stichwort, anschrift, fenster):  
        db = self.db
        user = self.nutzer
        now = datetime.datetime.now()       
        
        if nr_neu and stichwort and anschrift:           
            einsatz = db.query(Einsatzstelle).filter(Einsatzstelle.nr == nr_alt).first()            
            
            if nr_neu != nr_alt:
                einsatz.nr = nr_neu
            einsatz.stichwort = stichwort
            einsatz.anschrift = anschrift
            einsatz.status = status
            einsatz.letztes_update = now
            
            eintrag = Eintrag(einsatz, user, f'Einsatz update: {stichwort}, {anschrift} ({status}) - {nr_neu}')
            
            db.add(eintrag)
            db.commit()
            
            if nr_alt != nr_neu:
                eintrage = db.query(Eintrag).filter(Eintrag.einsatz_nr == nr_alt).all()
                
                for eintrag in eintrage:
                    eintrag.einsatz_nr = nr_neu
                
            db.commit()           

            self.update_table_tagebuch(nr_neu)
            self.update_table_einsatz()
            fenster.destroy()
        else:
            tk.messagebox.showwarning(
                title='Einsatz update',
                message='Einsatznummer, Einsatzstichwort und Anschrift sind Pflichangaben.'
            )
    
    def einsatz_anlegen_maske(self):  
        eingabe_maske = ttk.Toplevel('Neuer Einsatz')
        einsatz_stichwort = ctk.CTkEntry(eingabe_maske, placeholder_text='Einsatzstichwort')
        einsatz_nummer = ctk.CTkEntry(eingabe_maske, placeholder_text='Einsatznummer')        
        einsatz_anschrift = ctk.CTkEntry(eingabe_maske, placeholder_text='Anschrift')
        button_abbruch = ctk.CTkButton(eingabe_maske, text="Abbrechen", command=eingabe_maske.destroy)
        button_anlegen = ctk.CTkButton(
            eingabe_maske,
            text="Einsatz anlegen",
            command= lambda: self.einsatz_in_db_schreiben(einsatz_nummer.get(), einsatz_stichwort.get(), einsatz_anschrift.get(), eingabe_maske)
            )
        
        # Elemente ausrichten
        einsatz_stichwort.grid(row=1, column=1, pady=5, padx=5, columnspan=2, sticky='we')
        einsatz_nummer.grid(row=2, column=1, pady=5, padx=5, columnspan=2, sticky='we')
        einsatz_anschrift.grid(row=3, column=1, pady=5, padx=5, columnspan=2, sticky='we')
        button_abbruch.grid(row=4, column=1, pady=5, padx=5)
        button_anlegen.grid(row=4, column=2, pady=5, padx=5)
        
    def einsatz_in_db_schreiben(self, no, stichwort, anschrift, fenster):  
        db = self.db
        user = self.nutzer
        
        if no and stichwort and anschrift:
            einsatz = Einsatzstelle(
                einsatznummer=no,
                stichwort=stichwort,
                anschrift=anschrift
            )
            eintrag = Eintrag(einsatz, user)
            
            db.add(einsatz)
            db.add(eintrag)
            db.commit()
            
            fenster.destroy()
            self.update_table_einsatz()
        else:
            tk.messagebox.showwarning(
                title='Neuer Einsatz',
                message='Einsatznummer, Einsatzstichwort und Anschrift sind Pflichangaben.'
            )
    
    def clear_table_einsatz(self):
        for element in self.table_einsatz.get_children():
            self.table_einsatz.delete(element)

    def update_table_einsatz(self,):  
        db = self.db
        abgeschlossen = not self.check_arbeit_value.get()
        check_datum = self.check_date_value.get()

        if d := self.date_filter_var.get():
            datum = datetime.datetime.strptime(d, '%d.%m.%Y')
        else:
            return

        if abgeschlossen and check_datum:
            einsatzstellen = db.query(Einsatzstelle).filter(Einsatzstelle.status != "abgeschlossen").filter(Einsatzstelle.zeitstempel >= datum)
        elif abgeschlossen:
            einsatzstellen = db.query(Einsatzstelle).filter(Einsatzstelle.status != "abgeschlossen")
        elif check_datum:
            einsatzstellen = db.query(Einsatzstelle).filter(Einsatzstelle.zeitstempel >= datum)
        else:
            einsatzstellen = db.query(Einsatzstelle).all()
            
            
        self.clear_table_einsatz()
        
        for i, einsatz in enumerate(einsatzstellen):            
            status = einsatz.status
            datum = einsatz.zeitstempel
            letztes_update = einsatz.letztes_update
            datum_schwelle = datetime.datetime.now() - datetime.timedelta(minutes=self.einstellungen['zeitschwelle_einsatz_ohne_bearbeitung'])

            tag_row = 'even' if (i%2==0) else 'odd'
            tag_update = 'onTime'
            if (datum_schwelle>letztes_update) and (status != 'abgeschlossen'):
                tag_update = 'late'
            
            self.table_einsatz.insert(parent='', index=0, values=einsatz.tabellen_zeile(), tags=(tag_row, status, tag_update))

        for row in self.table_einsatz.get_children():
            id_est = self.table_einsatz.item(row)['values'][0]
            id_est = id_est.split(None, maxsplit=1)[1]
            if self.einsatzstelle_focus == id_est:
                self.table_einsatz.focus(row)
                self.table_einsatz.selection_set(row)
                break
        else:
            self.einsatzstelle_focus = None
            self.update_table_tagebuch(None)
         
    def update_table_tagebuch(self, id_est=None):  
        db = self.db
        for element in self.table.get_children():
            self.table.delete(element)
        
        if id_est:
            self.einsatzstelle_arbeit = id_est
            einsatzstelle = db.query(Einsatzstelle).filter(Einsatzstelle.nr == id_est).first()
            eintrage = db.query(Eintrag).filter(Eintrag.einsatz_nr == id_est).all()
            
            text = f'{einsatzstelle.stichwort}: {einsatzstelle.anschrift} ({einsatzstelle.status})'
            self.label_einsatz_text.set(text)
            
            
            for i, eintrag in enumerate(eintrage):
                row_tag = 'even' if (i%2==0) else 'odd'
                self.table.insert(parent='', index='end', values=eintrag.tabellen_zeile(), tags=(row_tag,))
        
        else:
            self.label_einsatz_text.set('- Einsatz -')

    def add_entry(self, _):
        db = self.db
        entry = self.entry_funk.get()
        funker = self.nutzer
        
        # Eintrag erzeugen wenn Eingabefeld Inhalt besitzt
        table_einsatz = self.table_einsatz
        selection = table_einsatz.selection()
        if entry and selection:
            for cnt, sel in enumerate(selection):
                id_est = table_einsatz.item(sel)['values'][0]
                id_est = id_est.split(None, maxsplit=1)[1]
                einsatz = db.query(Einsatzstelle).filter(Einsatzstelle.nr == id_est).first()
                eintrag = Eintrag(einsatz, funker, entry, self.entry_absender.get(), self.entry_empfang.get())
                
                if self.entry_absender.get():
                    eintrag.absender = self.entry_absender.get()
                
                if self.entry_empfang.get():
                    eintrag.empfaenger = self.entry_empfang.get()                 
                
                db.add(eintrag)
                db.commit()
                
                if cnt == 0:
                    self.table.insert(parent='', index='end', values=eintrag.tabellen_zeile())
                    self.entry_funk.delete(0, 'end')
                    self.entry_empfang.delete(0, 'end')
                    self.entry_absender.delete(0, 'end')

        self.update_table_tagebuch(self.einsatzstelle_arbeit)       
