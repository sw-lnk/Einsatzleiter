# Einsatzleiter
Dieses Projekt soll eine kostenlose Möglichkeit bieten die Einsatzleitung beim (Feuerwehr)Einsätzen zu unterstützen.

## Inhaltsverzeichnis
- [Voraussetzung und Einrichtung](#voraussetzung-und-einrichtung)
- [Funktionen](#funktionen)


## Voraussetzung und Einrichtung
Die Anwendung kann an jeden Computer verwendet werden. Als Datenbank wird ein Raspberry Pi verwendet. Auf dem Raspberry Pi wird die Datenbak MongoDB installiert und kann somit im lokalen Netzwerk der Einsatzleitung von mehreren Arbeitsplätzen erreicht werden.

- (Funk-)Arbeitsplatz mit Computer
- Raspberry Pi mit Ubuntu 20.04
- MongoDB als Datenbank auf dem RaspberryPi

### Einrichtung Datenbank
In der aktuellen Version wird eine [MongoDB](https://www.mongodb.com/de-de) Datenbank genutzt. Diese kann verschiedenen Geräten installiert werden.Beispielhaft wird hier die Einrichtung auf einem Raspberry Pi 3 aufgezeigt.

- Installation Ubuntu 20.04 LTS: [Ubuntu](https://ubuntu.com/blog/ubuntu-20-04-lts-is-certified-for-the-raspberry-pi)
- Einrichtung MongoDB inkl. Einrichtung RaspberryPi: [MongoDB](https://www.mongodb.com/developer/products/mongodb/mongodb-on-raspberry-pi/)

Zusätzlich in nach oben angebener Anleitung ein weiter Nutzer in der Datenbank anzulegen der nur auf der Datenbank *Einsatzstellen* Lese- und Schreibrechte erhält. Dieser Nutzer wird im weiteren für den Zugang im Programm genutzt.

### Initiale Anpassungen
Mit dem zusätzlich eingerichteten Nutzer (siehe [Einrichtung Datenbak](#einrichtung-datenbank)) sind die Daten in *settings.py* zu aktualisieren.

``` python
# Neuer Nutzer
db_user = 'user'

# Passwort zum Nutzer
db_user_password = 'user'

# Lokale IP des Rechners auf dem die Datenbank eingerichtet ist
db_ip = '192.168.178.41'

# Port auf dem die Datenbank erreichbar ist
db_port = '27017'

# Name der Datenbank
db_name = 'einsatztagebuch'
```

Die IP des Rechners auf dem die Datenbank installiert ist muss dieser IP im Router-Menü fest zugeordnet werden.

### Einrichtung Arbeitsplatz
Um zu überprüfen welche [Python](https://www.python.org/) Version installiert ist, die Eingabeaufforderung öffnen und
```cmd
python --version
```
eintippen und bestätigen. Es wird die installierte Python-Version angezeigt, z.B. Python 3.11.5.

Andernfalls die Python-Umgebung unter [https://www.python.org/](https://www.python.org/) herunterladen und installieren.

#### Download Einsatzleiter
1. Per git clone: In einen beliebigen Ordner wechsel und dort die Eingabeaufforderung starten und folgenden Befehl ausführen:
```cmd
git clone https://github.com/sw-lnk/Einsatzleiter
```

2. Download des [Einsatzleiter Repository](https://github.com/sw-lnk/Einsatzleiter) zip-Files von Github und an einem beliebigen Ort speichern und entpacken.

#### Optional: Virtuelle Python-Umgebung einrichten und starten
In den neuen Ordner **Einsatzleiter** wechseln und dort in der Eingabeaufforderung folgenden Befehl ausführen.
```cmd
python3 -m venv .venv
```
Im Anschluss die Virtuelleumgebung starten
1. Windows
```cmd
.venv\Scripts\activate
```
2. Linux
```cmd
source .venv/bin/activate
```

#### Notwenige Packet installieren
Die notwendigen Pakete werden durch den nachfolgenden Befehl in der Eingabeaufforderung installiert.
```cmd
pip install -r requirements.txt
```

#### Einsatzleiter starten
Durch den Befehl
```cmd
python main.py
```
wird das Programm gestartet.


## Funktionen
Folgende Funktionen sind vorhanden.

### Login
Der Login erfolgt durch einfache Eingabe des Namens der Person am (Funk-)Arbeitsplatz. Diese Eingabe wird bei Eingaben automatisch an die jeweilige Änderung ergänzt.

### Einsatztagebuch
Das Einsatztagebuch ermöglicht es einen Einsatz oder mehrere Einsätze zu dokumentieren. Per Eingabefeld kann einem ausgewählten Einsatz ein Eintrag ergänzt werden. Die Übersichtslisten werden im festen Intervall aktualisiert aus der Datenbank gelesen.

#### Einsatzstellen
Per Eingabemaske werden Einsatzstellen erfasst und bearbeitet.

#### Tagebucheintrag
Folgende Daten werden erfasst:
- Zeitstempel
- Bearbeiter
- Tagebucheintrag

Zusätzlich lassen sich folgende Daten erfassen:
- Absender der Nachricht
- Empfänger der Nachricht

Die optionalen Eingabe felder lassen sich über die *settings.py* (de-)aktivieren.



