from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey
)
from datetime import datetime

from base import Base


class Einheit(Base): 
    __tablename__ = "einheiten"

    funkrufname = Column("funkrufname", String, primary_key=True)
    einsatzstelle = Column("einsatz_nr", ForeignKey("einsatzstellen.nr"))
    vf = Column("vf", Integer)
    zf = Column("zf", Integer)
    gf = Column("gf", Integer)
    ms = Column("ms", Integer)
    agt = Column("agt", Integer)
    anmerkung = Column("anmerkung", String)
    zeitstempel = Column("zeitstempel", DateTime)
    
    def __init__(
        self,
        funkrufname: str,
        verbandsfuehrer: int = 0,
        zugfuehrer: int = 0,
        gruppenfuehrer: int = 0,
        mannschaft: int = 0,
        atemschutzgeraetetraeger: int = 0,
        anmerkung: str = ''
        ) -> None:
        self.funkrufname = funkrufname
        self.vf = verbandsfuehrer
        self.zf = zugfuehrer
        self.gf = gruppenfuehrer
        self.ms = mannschaft
        self.agt = atemschutzgeraetetraeger
        self.anmerkung = anmerkung
        self.zeitstempel = datetime.now()
        self.einsatz_nr = None
    
    def __str__(self) -> str:
        return self.funkrufname
    
    def __repr__(self):
        return f"{self.funkrufname}: {self.vf}/{self.zf}/{self.gf}/{self.ms} = {self.gesamtstaerke()} (AGT: {self.agt})"
    
    def gesamtstaerke(self) -> int:
        return self.vf + self.zf + self.gf + self.ms
    
    def aktualisiere_einheit(self, zeitstempel: datetime) -> None:
        self.zeitstempel = zeitstempel
        
    def tabellen_zeile(self) -> list:
        return [
            self.funkrufname,
            self.anmerkung,
            self.vf,
            self.zf,
            self.gf,
            self.ms,
            self.gesamtstaerke(),
            self.agt
        ]
    