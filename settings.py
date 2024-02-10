# Allgemein
name_organisation = 'Feuerwehr Musterstadt'

# Einstellungen zur Nutzung der MongoDB
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


# Benutzereinstellungen
# Aktualisierungsintervall der Daten
update_intervall = 5000 # Millisekunden

# Zeitschwelle ab der Einsätze seit letzter Bearbeitung gekennzeichnet werden
zeitschwelle_einsatz_ohne_bearbeitung = 10 # Minuten

# Optionale Eingabefelder
absender = False # Bei Bedarf nach True ändern
empfaenger = False # Bei Bedarf nach True ändern