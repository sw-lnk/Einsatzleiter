import datetime
from django import forms

from . import models

class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class NewMission(forms.ModelForm):
    class Meta:
        model = models.Mission
        exclude = ('archiv', 'start', 'end', 'status',)

class UpdateMission(forms.ModelForm):
    class Meta:
        model= models.Mission
        exclude = ('archiv', 'start', 'author')
        widgets = {
            'end': DateInput(),
        }
        
class Dashboard(forms.Form):
    year_now = datetime.datetime.now().year
    year = forms.ChoiceField(choices=(("2023", 2023), ("2024", 2024)), initial=year_now)