import json

def lese_einstellungen() -> dict:
        with open('settings.json', 'r') as f:
            einstellungen = json.load(f)
        return einstellungen