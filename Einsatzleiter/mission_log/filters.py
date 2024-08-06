from decimal import Decimal
from django import forms
from django.db.models import Q
import django_filters

from django.utils.translation import gettext_lazy as _

from .models import Mission

class MissionFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="", widget=forms.TextInput(attrs={'placeholder': _('Search')}))

    class Meta:
        model = Mission
        fields = ['query']

    def universal_search(self, queryset, name, value):
        return Mission.objects.filter(
            Q(main_id__icontains=value) | Q(keyword__icontains=value) | Q(street__icontains=value)
        )
