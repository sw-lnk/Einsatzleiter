import fpdf
import datetime

from django.conf import settings
from mission_log.models import Unit
from users.models import CustomUser

            
class UnitOverview(fpdf.FPDF):
    def __init__(
        self,
        author: CustomUser,
        units: list[Unit],
        orientation: str = "landscape",
        unit: str = "mm",
        format: str = "A4",
        font_cache_dir: str = "DEPRECATED"
        ) -> None:
        
        super().__init__(orientation, unit, format, font_cache_dir)
   
        self.author = author
        
        self.now = datetime.datetime.now()
        self.now_simple = self.now.strftime('%d.%m.%Y %H:%M')
        self.now_mission = self.now.strftime('%d%H%M%b%y')
        
        self.orga = settings.ORGA_NAME

        self.set_margin(15)
        self.add_page()
        
        '''
        Table to show all units
        '''
        
        with self.table(col_widths=(20,3,3,3,3,3,3,3)) as table:
            self.row = table.row()
            cols = ['Kennung', 'Status', 'VF', 'ZF', 'GF', 'MS', 'Gesamt', 'AGT']
            for cell in cols:
                self.row.cell(cell, align=fpdf.Align.C)
            for unit in units:
                row = table.row()
                cols = [unit.call_sign, str(unit.status), str(unit.vf), str(unit.zf), str(unit.gf), str(unit.ms), str(unit.staff_total()), str(unit.agt)]
                for i, cell in enumerate(cols):
                    if i==0: align = fpdf.Align.L
                    elif i==1: align = fpdf.Align.C
                    else: align = fpdf.Align.R
                    
                    row.cell(cell, align=align)
            row = table.row()
            staff_total = [
                'Gesamt',
                '',
                str(sum([unit.vf for unit in units])),
                str(sum([unit.zf for unit in units])),
                str(sum([unit.gf for unit in units])),
                str(sum([unit.ms for unit in units])),
                str(sum([unit.staff_total() for unit in units])),
                str(sum([unit.agt for unit in units])),                
            ]
            for i, cell in enumerate(staff_total):
                if i==0: align = fpdf.Align.L
                elif i==1: align = fpdf.Align.C
                else: align = fpdf.Align.R
                
                self.set_font(style='B')
                row.cell(cell, align=align)
            
    
    def header(self):
        # Add name of Orga
        self.set_y(14)
        self.set_font(family="helvetica", style='B', size=16)
        self.cell(text=self.orga)
        
        # Mission details
        self.set_font(style='', size=14)
        self.set_y(10)
        self.cell(0, 10, text='Einheitenübersicht', align=fpdf.Align.C)        
        
        # Add date at top right corner
        self.set_font(style="", size=10)
        self.set_y(10)
        self.cell(0, 10, text=self.now_simple, align=fpdf.Align.R)
        self.set_y(15)
        self.cell(0, 10, text=self.now_mission, align=fpdf.Align.R)
        
        self.set_y(30)

    
    def footer(self):
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "", 8)
        
        # Position cursor at 1.5 cm from bottom
        self.set_y(-15)
        self.cell(0, 10, "Einheitenübersicht", align=fpdf.Align.C)
        self.set_y(-15)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align=fpdf.Align.R)
        self.set_y(-15)
        self.cell(0, 10, f"Ersteller: {self.author.name()}", align=fpdf.Align.L)


if __name__ == '__main__':
    pass