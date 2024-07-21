import os
import fpdf
import datetime

from django.conf import settings
from mission_log.models import Mission, Entry, Unit
from users.models import CustomUser

            
class Protokoll(fpdf.FPDF):
    def __init__(
        self,
        author: CustomUser,
        mission: Mission,
        entries: list[Entry],
        units: list[Unit],
        sender: bool=False,
        recipient: bool=False,
        orientation: str = "landscape",
        unit: str = "mm",
        format: str = "A4",
        font_cache_dir: str = "DEPRECATED"
        ) -> None:
        
        super().__init__(orientation, unit, format, font_cache_dir)
   
        self.author = author
        
        self.keyword = mission.keyword
        self.address = mission.address()
        self.main_id = mission.main_id
        self.status = mission.status
        
        self.now = datetime.datetime.now()
        self.now_simple = self.now.strftime('%d.%m.%Y %H:%M')
        self.now_mission = self.now.strftime('%d%H%M%b%y')
        
        self.orga = settings.ORGA_NAME

        self.set_margin(15)
        self.add_page()
        
        '''
        Table to show all units
        '''
        
        with self.table(col_widths=(20,5,5,5,5,5,5)) as table:
            self.row = table.row()
            cols = ['Kennung', 'VF', 'ZF', 'GF', 'MS', 'Gesamt', 'AGT']
            for cell in cols:
                self.row.cell(cell, align=fpdf.Align.C)
            for unit in units:
                row = table.row()
                cols = [unit.call_sign, str(unit.vf), str(unit.zf), str(unit.gf), str(unit.ms), str(unit.staff_total()), str(unit.agt)]
                for i, cell in enumerate(cols):
                    align = fpdf.Align.R if i>0 else fpdf.Align.L
                    row.cell(cell, align=align)
            row = table.row()
            staff_total = [
                'Gesamt',
                str(sum([unit.vf for unit in units])),
                str(sum([unit.zf for unit in units])),
                str(sum([unit.gf for unit in units])),
                str(sum([unit.ms for unit in units])),
                str(sum([unit.staff_total() for unit in units])),
                str(sum([unit.agt for unit in units])),                
            ]
            for i, cell in enumerate(staff_total):
                align = fpdf.Align.R if i>0 else fpdf.Align.L
                row.cell(cell, align=align)
            
        
        self.ln()
        
        '''
        Table to show all entries
        '''
        self.cols = ['Zeitstempel', 'Eintrag', 'Bearbeiter']
        self.col_width = [20,100,15]
        if sender:
            self.cols.insert(-1, 'Absender')
            self.col_width.append(15)
        if recipient:
            self.cols.insert(-1, 'Empfänger')
            self.col_width.append(15)
        
        with self.table(col_widths=tuple(self.col_width)) as table:
            self.row = table.row()
            for cell in self.cols:
                self.row.cell(cell)
            for entry in entries:
                zeit = entry.time.strftime('%d.%m.%Y %H:%M')
                text = entry.text
                sender_val = entry.sender
                recipient_val = entry.recipient
                author = entry.author.name()
                
                row = table.row()
                
                cols = [zeit, text, author]
                if sender:
                    cols.insert(-1, sender_val)
                if recipient:
                    cols.insert(-1, recipient_val)                
                
                for cell in cols:
                    row.cell(cell)
    
    def header(self):
        # Add name of Orga
        self.set_y(14)
        self.set_font(family="helvetica", style='B', size=16)
        self.cell(text=self.orga)
        
        # Mission details
        self.set_font(style='', size=14)
        self.set_y(10)
        self.cell(0, 10, text=f'Funkprotokoll Einsatz {self.main_id}', align=fpdf.Align.C)
        self.set_y(17)
        self.cell(0, 10, text=self.keyword, align=fpdf.Align.C)
        self.set_y(24)
        self.cell(0, 10, text=self.address, align=fpdf.Align.C)
        
        # Add date at top right corner
        self.set_font(style="", size=10)
        self.set_y(10)
        self.cell(0, 10, text=self.now_simple, align=fpdf.Align.R)
        self.set_y(15)
        self.cell(0, 10, text=self.now_mission, align=fpdf.Align.R)
        self.set_y(40)

    
    def footer(self):
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "", 8)
        
        # Position cursor at 1.5 cm from bottom
        self.set_y(-15)
        self.cell(0, 10, f"Funkprotokoll: {self.keyword}, {self.address}", align=fpdf.Align.C)
        self.set_y(-15)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align=fpdf.Align.R)
        self.set_y(-15)
        self.cell(0, 10, f"Ersteller: {self.author.name()}", align=fpdf.Align.L)


if __name__ == '__main__':
    pass