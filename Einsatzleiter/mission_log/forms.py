from django import forms

from . import models

class NewMission(forms.ModelForm):
    class Meta:
        model = models.Mission
        fields = "__all__"