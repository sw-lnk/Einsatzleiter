from django.contrib import admin
from .models import Mission
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.action(description=_('Set status of selected mission to closed'))
def mark_as_closed(modeladmin, request, queryset):
    queryset.update(status=Mission.CLOSED)

@admin.action(description=_('Set status of selected mission to untreated'))
def mark_as_untreated(modeladmin, request, queryset):
    queryset.update(status=Mission.UNTREATED)

@admin.action(description=_('Set status of selected mission to processing'))
def mark_as_processing(modeladmin, request, queryset):
    queryset.update(status=Mission.PROCESSING)

@admin.action(description=_('Archiv mission'))
def archiv_mission(modeladmin, request, queryset):
    queryset.update(archiv=True)

@admin.action(description=_('Restore mission from archiv'))
def restore_mission(modeladmin, request, queryset):
    queryset.update(archiv=False)
    
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('archiv', 'main_id', 'keyword', 'street', 'start', 'status')
    list_filter = ('status' ,'start', 'archiv')
    actions = [
        mark_as_untreated,
        mark_as_processing,
        mark_as_closed,
        restore_mission,
        archiv_mission
        ]

