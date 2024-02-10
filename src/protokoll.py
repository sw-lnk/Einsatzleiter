import os
import fpdf
import datetime

jetzt = datetime.datetime.now()
jetzt_einfach = jetzt.strftime('%d.%m.%Y %H:%M')
jetzt_einsatz = jetzt.strftime('%d%H%M%b%y')
path = os.path.join('protokolle', 'TH0 - Große Straße 1.pdf')
            
class MyFPDF(fpdf.FPDF):
   def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "", 8)
        # Printing page number:
        self.cell(0, 10, f"Funkprotokoll: TH0, Große Straße 1, 12345 Musterstadt", align=fpdf.Align.L)
        self.set_y(-15)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align=fpdf.Align.R)

pdf = MyFPDF(orientation='landscape')
pdf.add_page()

# Name der Organisation einfügen
pdf.set_font(family="helvetica", style="B", size=16)
pdf.write(10, 'Feuerwehr Musterstadt')

# Erstelldatum oben rechts einfügen
pdf.set_font(style="", size=10)
pdf.set_x(250)
pdf.write(8, f'{jetzt_einfach}')
pdf.set_x(250)
pdf.write(18, f'{jetzt_einsatz}')

# Einsatzdaten
pdf.set_font(size=14)
pdf.ln()
pdf.set_y(20)
pdf.write(text='Funkprotokoll')
pdf.ln()
pdf.set_x(15)
pdf.write(text='TH0: Baum auf Straße')
pdf.ln()
pdf.set_x(15)
pdf.write(text='Große Straße 1, 12345 Musterstadt')

pdf.set_y(40)
pdf.set_font(size=10)
# Protokolldaten einfügen
with pdf.table(col_widths=(20,100,15,15,15)) as table:
    for data_row in range(15):
        row = table.row()
        for datum in (jetzt_einfach, 'Eintrag: Beispiel Eintrag als Funktionstest für das einfügen einer Tabelle', 'Absender', 'Empfänger', 'Bearbeiter'):
            row.cell(datum)
            
# Save pdf
pdf.output(path)