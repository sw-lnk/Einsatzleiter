from datetime import datetime
class Einheit(): 
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
    
    def __str__(self) -> str:
        return self.funkrufname
    
    def gesamtstaerke(self) -> int:
        return self.vf + self.zf + self.gf + self.ms
    
    def aktualisiere_einheit(self, zeitstempel: datetime) -> None:
        self.zeitstempel = zeitstempel
        
    def einheit_als_dict(self) -> dict:
        return {
            'funkrufname': self.funkrufname,
            'vf': self.vf,
            'zf': self.zf,
            'gf': self.gf,
            'ms': self.ms,
            'agt': self.agt,
            'anmerkung': self.anmerkung,
            'datum': self.zeitstempel
        }
    
    def einheit_als_tuple(self) -> tuple:
        return tuple(list(self.einheit_als_dict().values()))
    