from sqlalchemy.orm import Session

import random

from einheit import Einheit
from einsatzstelle import Einsatzstelle
from eintrag import Eintrag
from database import verbinde_datenbank

def erstelle_zufalls_einsatz(session: Session) -> None:
    nr = random.randint(10_000, 99_999)
    stichwort = random.choice(
        [
            "TH0 - Baum auf Straße",
            "B0 - gelöschtes Feuer",
            "CBRN0 - Betriebsmittel laufen nach VU",
        ]
    )
    anschrift = (
        random.choice(
            [
                "Große Straße 1",
                "Brandweg 7",
                "Kurze Allee 10",
                "Ringstraße 8"
            ]
        )        
    )
    anschrift = anschrift + ", 12345 Musterstadt"

    est = Einsatzstelle(nr, stichwort, anschrift)
    eintrag = Eintrag(est, 'M. Mustermann')
    session.add_all([est, eintrag])
    session.commit()


def erstelle_zufalls_einheit(session: Session) -> None:
    
    funkrufname = random.choice(
        [
            "Fl. MUS 1 ELW1 1",
            "Fl. MUS 1 HLF20 1",
            "Fl. MUS 1 LF20 1",
            "Fl. MUS 1 MTF 1",
            "Fl. MUS 1 RW2 1",
            "Fl. MUS 1 DLK23 1",
        ]
    )
    vf = random.randint(0, 2)
    zf = random.randint(0, 2)
    gf = random.randint(0, 2)
    ms = random.randint(1, 4)
    agt = random.randint(1, 4)

    einheit = Einheit(funkrufname,vf,zf,gf,ms,agt,'Zufallsgenerator')
    session.add(einheit)
    session.commit()


if __name__ == '__main__':
    session = verbinde_datenbank()
    erstelle_zufalls_einsatz(session)
    erstelle_zufalls_einheit(session)