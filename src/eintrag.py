from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
import datetime

from base import Base
from einsatzstelle import Einsatzstelle


class Eintrag(Base):
    __tablename__ = "eintrage"   

    id = Column(Integer, primary_key=True, autoincrement=True)
    einsatz_nr = Column("einsatz_nr", ForeignKey("einsatzstellen.nr"))
    eintrag = Column("stichwort", String)
    absender = Column("anschrift", String)
    empfaenger = Column("empfaenger", String)
    bearbeiter = Column("bearbeiter", String)
    zeitstempel = Column("zeitstempel", DateTime)

    def __init__(
        self,
        einsatz: Einsatzstelle,
        bearbeiter: str,
        eintrag: str = None,
        absender: str = None,
        empfaenger: str = None        
        ):
        self.einsatz_nr = einsatz.nr
        self.zeitstempel = datetime.datetime.now()
        self.bearbeiter = bearbeiter
        self.eintrag = eintrag
        self.absender = absender
        self.empfaenger = empfaenger        
        self.einsatz = einsatz
        
        if eintrag is None:
            self.eintrag = f'Einsatz neu: {self.einsatz.stichwort}, {self.einsatz.anschrift} (unbearbeitet) - {self.einsatz.nr}'

    def __repr__(self):
        return f"{self.einsatz_nr} - {self.zeitstempel}: {self.eintrag}"
    
    def tabellen_zeile(self) -> list[str]:
        return [self.zeitstempel.strftime('%d.%m.%Y %H:%M'), self.eintrag, self.absender, self.empfaenger, self.bearbeiter]