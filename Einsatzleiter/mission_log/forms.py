import datetime
from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from . import models

class DateTimeInput(DateTimePickerInput):
    input_type = '%d.%m.%Y %H:%M'

class NewMission(forms.ModelForm):
    class Meta:
        model = models.Mission
        exclude = ('archiv', 'author')
        widgets = {
            'start': DateTimeInput(),
            'end': DateTimeInput(),
        }

class UpdateMission(forms.ModelForm):
    class Meta:
        model= models.Mission
        exclude = ('archiv', 'author')
        widgets = {
            'start': DateTimeInput(),
            'end': DateTimeInput(),
        }