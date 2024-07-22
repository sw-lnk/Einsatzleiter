# Einsatzleiter
Dieses Projekt soll eine kostenlose Möglichkeit bieten die Einsatzleitung bei (Feuerwehr)Einsätzen zu unterstützen.

## Inhaltsverzeichnis
- [Einleitung](#einleitung)
- [Einrichtung](#einrichtung)
- [Funktionen](#funktionen)


## Einleitung
Die Anwendung kann an jeden Endgerät mit Webbrowser verwendet werden, die Zugriff zum lokalen Server haben. Ein Server inkl. Datenbank werden auf einem Raspberry Pi installiert und kann somit im lokalen Netzwerk der Einsatzleitung von mehreren Arbeitsplätzen erreicht werden.

## Einrichtung
dazu sind die folgenden Schritte durchzuführen:
- Installation Raspberry Pi Betriebssystem
- Verbindung zum lokalen Netzwerk
- Einrichtung Docker und Portainer
- Installation vom _Einsatzleiter_


#### Welches Betriebssystem
Es reicht die Installation von Raspberry _Pi OS Lite_ (64-bit). Wer lieber eine grafische Oberfläche nutzen möchte der installiert _Raspberry Pi OS with desktop_ (64-bit). Das Betirebssystem kann nach folgender Anleitung installiert werden: [Videoanleitung](https://www.youtube.com/watch?v=7mOj_Bu7nBA)

#### Netzwerkanbindung
Es wird empfohlen den Raspberry Pi mit einem Netzwerkkabel direkt an das lokale Netzwerk anzuschließen. Eine Drahtlose Verbindung ist ebenfalls möglich, hier ist dann entsprechend bei der Einrichtung die Netzwerkverbindung einzurichten.

*Wichtig*: Dem Raspberry Pi muss im Netzwerk eine Fest IP-Adresse zugewisen werden. Beispielhaft eine Anleitung mit einer FritzBox: [FritzBox - IP fest zuordnen](https://avm.de/service/wissensdatenbank/dok/FRITZ-Box-7590/201_Netzwerkgerat-immer-die-gleiche-IP-Adresse-von-FRITZ-Box-zuweisen-lassen/#:~:text=Benutzeroberfl%C3%A4che%20der%20FRITZ!-,Klicken%20Sie%20im%20Men%C3%BC%20%22Heimnetz%22%20auf%20%22Netzwerk%22.,gleiche%20IPv4%2DAdresse%20zuweisen%22.)

#### Docker einrichten
Auf dem Raspberry Pi wird Docker und Portainer eingerichtet: [Wie man Docker auf dem Raspberry Pi in 15 Minuten einrichtet](https://www.heise.de/news/Wie-man-Docker-auf-dem-Raspberry-Pi-in-15-Minuten-einrichtet-7524692.html)

#### Installation Einsatzleiter
Per ssh auf dem Server (Raspberry Pi) einloggen und die nachfolgenden Schritte ausführen.

```cmd
git clone https://github.com/sw-lnk/Einsatzleiter
cd Einsatzleiter
touch .env
```

```cmd
nano .env
```

Inhalt für .env Datei:
```
PIPELINE = "production" # Auskommentieren um Debug-Mode zu aktivieren
DB_NAME = "einsatzleitung" # Name der Datenbank
DB_USER_NM = "db_user_name" # Datenbank Zugangsdaten -> Anpassen
DB_USER_PW = "secret_user_pwd" # Datenbank Zugangsdaten -> Anpassen
DB_IP = "einsatzleiter-postgres" # IP der Datenbank im Docker-Netzwerk -> nicht verändern
DB_PORT = 5432 # Port der Datenbank -> nicht verändern

DEVICE_IP = "192.168.178.21" # Fest zugeordnete IP im lokalen Netzwerk, siehe Netzwerkanbindung

POSTGRES_USER = "db_user_name" # Datenbank Zugangsdaten -> Gleich wie oben
POSTGRES_PASSWORD = "secret_user_pwd" # Datenbank Zugangsdaten -> Gleich wie oben
POSTGRES_DB = "einsatzleitung" # Datenbankname -> Gleich wie oben

ORGA_NAME = "Feuerwehr Musterstadt" # Name der eigenen Organisation -> Anpassen
EMAIL_ADRESSE = "info@your-mail.xyz" # E-Mail der eigenen Organisation Depechen-Eingang -> Anpassen
EMAIL_PASSWORD = "secret-mail_pwd" # Passwort zum eigenen Mail-postfach -> Anpassen

IMAP_SERVER = "imap.service.xyz" # IMAP der E-Mail der eigenen Organisation -> Anpassen
IMAP_PORT = 993 # IMAP Port -> Anpassen

SMTP_SERVER = "smtp.service.xyz" # SMTP der E-Mail der eigenen Organisation -> Anpassen
SMTP_PORT = 465 # SMTP Port -> Anpassen

EMAIL_LEITSTELLE = "mail@leitstelle.xyz" # E-Mail der Leitstelle die Depechen zustellt -> Anpassen
ANSCHRIFT_LEITSTELLE = "Straße Hausnummer" # Anschrift der Leitstelle -> Anpassen

# TELEGRAM_TOKEN = "telegram_bot_token" # Token vom Telegram-Bot -> Anpassen
# GROUP_CHAT_ID = "telegram_chat_id" # Telegram-Chat-ID für Einsatzticker -> Anpassen

ZIP_CODE = "12345" # Postleitzahl als Standartwert für neue Einsätze -> Anpassen

ALLOWED_HOSTS = "localhost,127.0.0.1,[::1]" # Zulässige IPs -> nicht Anpassen
SECRET_KEY = "secret_django_key_production" # Django Secret Key für die Produktion -> Anpassen

DJANGO_SUPERUSER_PASSWORD = "admin" # Admin Benutzername -> Anpassen
DJANGO_SUPERUSER_USERNAME = "secret-admin_pwd" # Admin Passwort -> Anpassen
DJANGO_SUPERUSER_EMAIL = "user@your-mail.xyz" # Admin Mailadresse -> Anpassen
```

```cmd
docker compose up
```

#### Einsatzleiter starten
Im Webbrowser die IP-Adresse des Servers eingeben gefolgt vom Port 1337, siehe _Installation Einsatzleiter_.
Beispiel: http://192.168.178.21:1337

## Funktionen
Folgende Funktionen sind vorhanden.

### Login Admin
Der Login erfolgt im Login-Menü mit dem Benutzername und Passwort, dass weiter oben definiert wurde. Beides kann vom Admin-Zugang aus angepasst werden.

### Login Nutzer
Der Login erfolgt im Login-Menü mit Benutzername und Passwort. Beides kann vom Admin-Zugang aus erstellt bzw. angepasst werden.

Ist ein E-Mail-Postfach eingerichtet, kann die Passwort-Reset-Funktion genutzt werden.

### Einsatztagebuch
Das Einsatztagebuch ermöglicht es einen Einsatz oder mehrere Einsätze zu dokumentieren. Per Eingabefeld kann einem ausgewählten Einsatz ein Eintrag ergänzt werden. Die Übersichtslisten werden im festen Intervall aktualisiert aus der Datenbank gelesen.

#### Einsatzstellen
Per Eingabemaske werden Einsatzstellen erfasst und bearbeitet.

Ist ein E-Mail-Postfach angegeben, können Einsätze automatisch aus den Einsatzdepechen per Mail generiert werden und auch als abgeschlossen markiert werden. Sind zudem Telegram-Daten angegeben kann ein Einsatzticker aus den automatisch generierten Mails genutzt werden. 

#### Tagebucheintrag
Folgende Daten werden erfasst:
- Zeitstempel
- Bearbeiter
- Tagebucheintrag

Zusätzlich lassen sich folgende Daten erfassen:
- Absender der Nachricht
- Empfänger der Nachricht

Die optionalen Eingabe felder lassen sich in der mission_overview.html Datei anzeigen.

#### Protokoll ausleitung
Je Einsatz lässt sich per Knopfdruck das aktuelle Funkprotokolle als PDF ausleiten.
Der angezeigte Name der Organistion lässt sich über die *.env* Datei anpassen.

### Kräfteübersicht
Einfache Übersicht der vorhandenen Einheiten. Eingabe von Funkrufname, Stärke und Anzahl Atemschutzgeräteträger, zusätzlich kann eine Anmerkung hinterlegt werden. Gesamtstärke wird automatisch ermittelt. Alle Daten werde im festgelegten Aktualisierungintervall aktualisiert. Die Übersicht kann per Klick als PDF ausgeleitet werden.
