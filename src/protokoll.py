import os
import fpdf
import datetime

from einsatzstelle import Einsatzstelle
from eintrag import Eintrag

            
class Protokoll(fpdf.FPDF):
    def __init__(
        self, einsatz: Einsatzstelle,
        eintrage: list[Eintrag],
        absender: bool=False,
        empfanger: bool=False,
        organisation: str = 'Feuerwehr Musterstadt',
        orientation: str = "landscape",
        unit: str = "mm",
        format: str = "A4",
        font_cache_dir: str = "DEPRECATED") -> None:
        
        super().__init__(orientation, unit, format, font_cache_dir)
   
        self.stichwort = einsatz.stichwort
        self.anschrift = einsatz.anschrift
        self.nr_lst = einsatz.nr
        self.status = einsatz.status
        
        self.jetzt = datetime.datetime.now()
        self.jetzt_einfach = self.jetzt.strftime('%d.%m.%Y %H:%M')
        self.jetzt_einsatz = self.jetzt.strftime('%d%H%M%b%y')
        
        self.ordner_name = 'protokolle'
        if not os.path.exists(self.ordner_name):
            os.mkdir(self.ordner_name)
        self.path = os.path.join(self.ordner_name, f'{self.stichwort}_{self.anschrift}.pdf')
        
        self.organisation = organisation

        self.set_margin(15)
        self.add_page()
          
        self.spalten = ['Zeitstempel', 'Eintrag', 'Bearbeiter']
        self.spalten_breite = [20,100,15]
        if absender:
            self.spalten.insert(-1, 'Absender')
            self.spalten_breite.append(15)
        if empfanger:
            self.spalten.insert(-1, 'Empfänger')
            self.spalten_breite.append(15)
        
        with self.table(col_widths=tuple(self.spalten_breite)) as table:
            self.row = table.row()
            for cell in self.spalten:
                self.row.cell(cell)
            for eintrag in eintrage:
                zeit = eintrag.zeitstempel.strftime('%d.%m.%Y %H:%M')
                text = eintrag.eintrag
                absender_val = eintrag.absender
                empfanger_val = eintrag.empfaenger
                bearbeiter = eintrag.bearbeiter
                
                row = table.row()
                
                cols = [zeit, text, bearbeiter]
                if absender:
                    cols.insert(-1, absender_val)
                if empfanger:
                    cols.insert(-1, empfanger_val)
                
                
                for cell in cols:
                    row.cell(cell)
                    
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
        self.cell(0, 10, text='Funkprotokoll', align=fpdf.Align.C)
        self.set_y(17)
        self.cell(0, 10, text=f'{self.stichwort} ({self.status})', align=fpdf.Align.C)
        self.set_y(24)
        self.cell(0, 10, text=f'{self.anschrift} ({self.nr_lst})', align=fpdf.Align.C)
        
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
        self.cell(0, 10, f"Funkprotokoll: {self.stichwort}, {self.anschrift}", align=fpdf.Align.L)
        self.set_y(-15)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align=fpdf.Align.R)


if __name__ == '__main__':
    jetzt = datetime.datetime.now()

    einsatz = {
        'nr_lst': 987654321,
        'stichwort': 'TH0 - Baum auf Straße',
        'anschrift': 'Waldstraße 1, 12345 Musterstadt',
        'status': 'unbearbeitet',
        'datum': jetzt,
        'letztes_update': jetzt,
        'archiv': False
    }

    eintrag = {
        'einsatz': 987654321,
        'zeitstempel': jetzt,
        'eintrag': f'Einsatz neu: TH0 - Baum auf Straße, Waldstraße 1, 12345 Musterstadt (unbearbeitet) - 987654321',
        'absender': '',
        'empfanger': '',
        'bearbeiter': 'Max Mustermann'
    }
    eintrage = [eintrag for x in range(30)]

    pdf = Protokoll(einsatz, eintrage)
