from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)
import datetime

from base import Base


class Einsatzstelle(Base):
    __tablename__ = "einsatzstellen"

    nr = Column("nr", String, primary_key=True)
    stichwort = Column("stichwort", String)
    anschrift = Column("anschrift", String)
    status = Column("status", String)
    zeitstempel = Column("zeitstempel", DateTime)
    letztes_update = Column("letztes_update", DateTime)
    archiv = Column("archiviert", Boolean)

    def __init__(self, einsatznummer: str, stichwort: str, anschrift: str):
        self.nr = einsatznummer
        self.stichwort = stichwort
        self.anschrift = anschrift
        self.status = "unbearbeitet"
        self.zeitstempel = datetime.datetime.now()
        self.letztes_update = datetime.datetime.now()
        self.archiv = False

    def __repr__(self):
        return f"{self.nr}: {self.stichwort} - {self.anschrift} ({self.status})"
    
    def tabellen_zeile(self) -> list[str]:
        return [f'id: {self.nr}', self.zeitstempel.strftime('%d.%m.%Y %H:%M'), self.stichwort, self.anschrift, self.status]
    