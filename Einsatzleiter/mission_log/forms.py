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
        exclude = ('archiv', 'start',)
        widgets = {
            'end': DateInput(),
        }