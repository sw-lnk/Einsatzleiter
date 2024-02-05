# Einsatzleiter
Dieses Projekt soll eine kostenlose Möglichkeit bieten die Einsatzleitung beim (Feuerwehr)Einsätzen zu unterstützen.

## Inhaltsverzeichnis
- [Voraussetzung](#voraussetzung)
- [Funktionen](#funktionen)


## Voraussetzung
Die Anwendung kann an jeden Computer verwendet werden. Als Datenbank wird ein Raspberry Pi verwendet. Auf dem Raspberry Pi wird die Datenbak MongoDB installiert und kann somit im lokalen Netzwerk der Einsatzleitung von mehreren Arbeitsplätzen erreicht werden.

- Computer mit Python3 Umgebung ([Python](https://www.python.org/))
- Raspberry Pi mit Ubuntu 20.04
- MongoDB als Datenbank auf dem RaspberryPi

## Funktionen
Folgende Funktionen sind vorhanden.

### Login
Der Login erfolgt durch einfache Eingabe des Namens der Person am Arbeitsplatz.

### Einsatztagebuch
Das Einsatztagebuch ermöglicht es einen Einsatz oder mehrere Einsätze zu dokumentieren. Per Eingabefeld kann einem ausgewählten Einsatz ein Eintrag ergänzt werden. Zeitstempel und Bearbeiter werden automatisch ergänzt.

Die Übersichtslisten werden alle 5 Sekunden aktualisiert aus der Datenbank gelesen.

