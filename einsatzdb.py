# Einträge: Zeitstempel, Eintrag, Absender, Empfänger, Bearbeiter

beispiel_einsatz_db = [
    
    {'nr_lst': 2024000001, 'stichwort': 'TH0', 'strasse': 'Musterstr.', 'status': 'abgeschlossen',
     'liste_eintrag': [
         ['01.02.2024 09:00', 'Einsatz angelegt', '', '', 'Max Mustermann'],
         ['01.02.2024 09:05', '1 HLF20 1 alarmiert', 'EL', '1 HLF20 1', 'Max Mustermann'],
         ['01.02.2024 09:07', 'Einsatzstelle an, kleiner Baum auf Straße, wird beiseite geräumt, Einsatzdauer 5 Min.', '1 HLF20 1', 'EL', 'Max Mustermann'],
         ['01.02.2024 09:11', 'EB', '1 HLF20 1', 'EL', 'Max Mustermann'],
         ['01.02.2024 09:11', 'Feuerwehrhaus anfahren', 'EL', '1 HLF20 1', 'Max Mustermann']
        ]},
    
    {'nr_lst': 2024000002, 'stichwort': 'TH0', 'strasse': 'Beispiel Str.', 'status': 'in Arbeit',
     'liste_eintrag': [
         ['01.02.2024 09:03', 'Einsatz angelegt', '', '', 'Max Mustermann'],
         ['01.02.2024 09:11', '2 HLF20 1 alarmiert', 'EL', '2 HLF20 1', 'Max Mustermann'],
         ['01.02.2024 09:14', 'Einsatzstelle an, Baustellenabsperrung auf Straße, wird beiseite geräumt, Einsatzdauer 5 Min.', '2 HLF20 1', 'EL', 'Max Mustermann'],
         ['01.02.2024 09:28', 'Frage? Status?', '2 HLF20 1', 'EL', 'Max Mustermann']
        ]},
    
    {'nr_lst': 2024000003, 'stichwort': 'TH1', 'strasse': 'Hauptstr.', 'status': 'in Arbeit',
     'liste_eintrag': [
         ['01.02.2024 09:10', 'Einsatz angelegt', '', '', 'Emma Müller'],
         ['01.02.2024 09:12', '1 LF10 1 alarmiert', 'EL', '1 LF10 1', 'Emma Müller'],
         ['01.02.2024 09:19', 'Einsatzstelle an, Keller 50cm unter Wasser, Einsatzdauer unbekannt', '1 HLF20 1', 'EL', 'Emma Müller'],         
        ]},
    
    {'nr_lst': 2024000004, 'stichwort': 'TH0', 'strasse': 'Nebenstr.', 'status': 'offen', 'liste_eintrag': [
         ['01.02.2024 09:14', 'Einsatz angelegt', '', '', 'Max Mustermann']
        ]},
]