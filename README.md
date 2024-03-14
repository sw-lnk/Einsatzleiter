# Einsatzleiter
Dieses Projekt soll eine kostenlose Möglichkeit bieten die Einsatzleitung beim (Feuerwehr)Einsätzen zu unterstützen.

## Inhaltsverzeichnis
- [Voraussetzung und Einrichtung](#voraussetzung-und-einrichtung)
- [Funktionen](#funktionen)


## Voraussetzung und Einrichtung
Die Anwendung kann an jeden Computer verwendet werden. Diese Anwendung kann als Einzelplatzanwendung an jedem Computer local genutzt werden oder mit einer Anbindung an eine Datenbank. Als Datenbank kann ein Raspberry Pi verwendet werden. Auf dem Raspberry Pi wird die Datenbank MongoDB installiert und kann somit im lokalen Netzwerk der Einsatzleitung von mehreren Arbeitsplätzen erreicht werden.

### Nutzung als Einzelplatz
- (Funk-)Arbeitsplatz mit Computer

### Nutzung mehrere vernetzer Arbeitsplätze
- (Funk-)Arbeitsplatz mit Computer
- Raspberry Pi


### Einrichtung bei vernezten Arbeitsplätzen
dazu sind die folgenden Schritte durchzuführen:
- Installation Raspberry Pi Betriebssystem
- Verbindung zum lokalen Netzwerk
- Einrichtung Docker und Portainer
- Datenbank einrichten


#### Welches Betriebssystem
Es reicht die Installation von Raspberry _Pi OS Lite_ (64-bit). Wer lieber eine grafische Oberfläche nutzen möchte der installiert _Raspberry Pi OS with desktop_ (64-bit). Das Betirebssystem kann nach folgender Anleitung installiert werden: [Videoanleitung](https://www.youtube.com/watch?v=7mOj_Bu7nBA)

#### Netzwerkanbindung
Es wird empfohlen den Raspberry Pi mit einem Netzwerkkabel direkt an das lokale Netzwerk anzuschließen. Eine Drahtlose Verbindung ist ebenfalls möglich, hier ist dann entsprechend bei der Einrichtung die Netzwerkverbindung einzurichten.

*Wichtig*: Dem Raspberry Pi muss im Netzwerk eine Fest IP-Adresse zugewisen werden. Beispielhaft eine Anleitung mit einer FritzBox: [FritzBox - IP fest zuordnen](https://avm.de/service/wissensdatenbank/dok/FRITZ-Box-7590/201_Netzwerkgerat-immer-die-gleiche-IP-Adresse-von-FRITZ-Box-zuweisen-lassen/#:~:text=Benutzeroberfl%C3%A4che%20der%20FRITZ!-,Klicken%20Sie%20im%20Men%C3%BC%20%22Heimnetz%22%20auf%20%22Netzwerk%22.,gleiche%20IPv4%2DAdresse%20zuweisen%22.)

#### Docker einrichten
Auf dem Raspberry Pi wird Docker und Portainer eingerichtet: [Wie man Docker auf dem Raspberry Pi in 15 Minuten einrichtet](https://www.heise.de/news/Wie-man-Docker-auf-dem-Raspberry-Pi-in-15-Minuten-einrichtet-7524692.html)

#### Einrichtung Datenbank
In der aktuellen Version wird eine [MongoDB](https://www.mongodb.com/de-de) Datenbank genutzt. Diese kann verschiedenen Geräten installiert werden.Beispielhaft wird hier die Einrichtung auf einem Raspberry Pi 3 aufgezeigt.

Ist, wie im vorherigen Schritt aufgezeigt, Docker und Portainer eingerichtet, ist im Portainer Portal die Datenbank einzurichten. Dazu wird einer neuer Stack erstellt: 

![Stack erstellen](https://github.com/sw-lnk/Einsatzleiter/blob/main/img/portainer_stack1.png)

Dieser Stack beinhaltet die Daten zur Erzeugung der Datenbank.
``` yml
version: '3'

services:

  mongo:
    image: mongo:4.0.28
    restart: unless-stopped
    ports:
      - 27017:27017
    volumes:
      - mongodata:/data/db
    networks:
      - network
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: mongoadmin1

volumes:
  mongodata:
    driver: local

networks:
  network:
    driver: bridge
```

![Stack ausfüllen](https://github.com/sw-lnk/Einsatzleiter/blob/main/img/portainer_stack2.png)

Dabei wird auch der Admin Zugang festgelegt, hier ist ein entsprechend sicheres Passwort zu wählen.
``` yml
MONGO_INITDB_ROOT_USERNAME: root
MONGO_INITDB_ROOT_PASSWORD: mongoadmin1
```

Die Erstellung wird mit dem Klick auf *Deploy the stack* gestartet. Je nach Internetverbindung dauert dieser Schritt einige Zeit.

Ist die Erstellung erfolgreich ist ein Container sichtbar mit dem Status **running**.

![Container Übersicht](https://github.com/sw-lnk/Einsatzleiter/blob/main/img/portainer_container1.png)

Im weiteren ist ein zusätzlicher Nutzer anzulegen, welcher nur Zugriff auf den Bereich der Datenbank hat der die Einsatzdaten beinhaltet. Dazu wird die Konsole der Datenbank gestartet (Markierung 3) und mit _connect_ verbunden.

Zunächst erfolgt die Prüfung, ob die Datenbank MongoDB erreichbar ist. Dazu diesen Befehl eingeben und mit Enter bestätigen:
```
mongo
```

Anschließend wird in die Datenbank *admin* gewechsel:
```
use admin
```

Hier ist zunächst eine Authentifizierung erforderlich, der Benutzername und das Passwort dazu wie oben angelegt:
```
db.auth("root", "mongoadmin1")
```

Im nächsten Schritt ist in die eigentlich zu nutzende Datenbank zu wechseln:
```
use einsatzleiter
```

Hier wird nun der Nutzer für einen Arbeitsplatz angelegt (dieser Schritt kann für jeden Arbeitsplatz wiederholt werden):
```
db.createUser({user: "arbeitsplatz1", pwd: "einsatzleitung1", roles: ["readWrite"]})
```

Die hier festgelegten Zugansdaten werden in der Anwendung als Zugangsdaten verwendet.


#### Initiale Anpassungen
Mit den eingerichteten Nutzern (siehe [Einrichtung Datenbak](#einrichtung-datenbank)) sind die Daten in *settings.py* zu aktualisieren.

``` python
# Nutzername
db_user = 'arbeitsplatz1'

# Passwort
db_user_password = 'einsatzleitung1'

# Lokale IP des Rechners auf dem die Datenbank eingerichtet ist
db_ip = '192.168.178.41'

# Port auf dem die Datenbank erreichbar ist
db_port = '27017'

# Name der Datenbank
db_name = 'einsatzleiter'
```

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
python einsatzleiter.py
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

Die optionalen Eingabe felder lassen sich über die *settings.json* oder über den Bereich *Einstellungen* (de-)aktivieren.

Sind mehrere Einsätze in der Einsatzübersicht angewählt, werden alle diesen Einsätzen ein Eintrag ergänzt.

#### Protokoll ausleitung
Für alle markierte Einsätze in der Einsatzübersicht lassen sich per Knopfdruck die Funkprotokolle als PDF ausleiten.
Der angezeigte Name der Organistion lässt sich über die *settings.json* Datei oder über den Bereich *Einstellungen* anpassen.

### Kräfteübersicht
Einfache Übersicht der vorhandenen Einheiten. Eingabe von Funkrufname, Stärke und Anzahl Atemschutzgeräteträger, zusätzlich kann eine Anmerkung hinterlegt werden. Gesamtstärke wird automatisch ermittelt. Alle Daten werde im festgelegten Aktualisierungintervall an allen Arbeitsplätzen aktualisiert. Die Übersicht kann per Klick als PDF ausgeleitet werden.



