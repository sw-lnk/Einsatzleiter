import os
from dotenv import load_dotenv

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

load_dotenv()

# Create your models here.
class Mission(models.Model):
    class Status(models.IntegerChoices):
        UNTREATED = 0, _('Unbearbeitet')
        PROCESSING = 1, _('In Arbeit')
        CLOSED = 2, _('Abgeschlossen')
    
    class Prio(models.IntegerChoices):
        HIGH = 1, _('Hoch')
        MEDIUM = 2, _('Mittel')
        LOW = 3, _('Niedrig')
    
    ZIP_CODE = os.getenv("ZIP_CODE")
    
    main_id=models.IntegerField(_('main id'), primary_key=True)
    keyword=models.CharField(_('keyword'), max_length=100, blank=False)
    street=models.CharField(_('street'), max_length=100, blank=False)
    street_no=models.CharField(_('street no'), max_length=10, blank=True)
    zip_code=models.CharField(_('zip code'), max_length=5, blank=True)
    
    status=models.PositiveSmallIntegerField(_('status'), choices=Status.choices, default=Status.UNTREATED, blank=False)
    prio=models.PositiveSmallIntegerField(_('priority'), choices=Prio.choices, default=Prio.MEDIUM, blank=False)
    
    start=models.DateTimeField(_('start time'), default=timezone.now, blank=False, null=False)
    end=models.DateTimeField(_('end time'), blank=True, null=True)
    
    creation=models.DateTimeField(_('creation time'), auto_now_add=True, editable=False)
    last_update=models.DateTimeField(_('update time'), auto_now=True)
    
    archiv=models.BooleanField(_('archiv'), default=False)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        verbose_name=_("Author")
    )
    
    def address(self) -> str:
        a = self.street
        if self.street_no:
            a += f' {self.street_no}'
        if self.zip_code:
            a += f', {self.zip_code}'
        return a
    
    def auto_entry(self) -> str:
        return f'{self.keyword}, Status: {self.status}, Prio: {self.prio} - {self.address()}'
    
    def short(self):
        return f'{self.keyword} - {self.street}'
    
    def __str__(self):
        return f'{self.main_id}: {self.keyword} - {self.street}'


class Entry(models.Model):
    
    text = models.TextField(_("Entry text"), blank=False)
    sender = models.CharField(_('Sender'), max_length=100, blank=True)
    recipient = models.CharField(_('Recipient'), max_length=100, blank=True)
    
    time = models.DateTimeField(_('Time'), auto_now_add=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        verbose_name=_("Author")
    )
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, verbose_name=_("Mission"))
    
    def local_time(self):
        return self.time.astimezone(timezone.get_current_timezone())
    
    def __str__(self):
        return f"{self.local_time().strftime('%d.%m.%Y %H:%M')}: {self.text}"


class Orga(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True, blank=False)
    
    def __str__(self):
        return self.name


class Unit(models.Model):
    class Status(models.IntegerChoices):
        S0 = 0, _('0 - Priorisierter Sprechwunsch')
        S1 = 1, _('1 - Einsatzbereit Funk')
        S2 = 2, _('2 - Einsatzbereit Wache')
        S3 = 3, _('3 - Einsatz übernommen')
        S4 = 4, _('4 - Einsatzstelle an')
        S5 = 5, _('5 - Sprechwunsch')
        S6 = 6, _('6 - Nicht einsatzbereit')
        S7 = 7, _('7 - Patient aufgenommen')
        S8 = 8, _('8 - Ankunft Krankenhaus')
        S9 = 9, _('9 - Abruf Einsatzauftrag/Fremdanmeldung')
        
    STATUS_ORDER = [0,5,3,4,1,2,7,8,9,6]
    
    call_sign = models.CharField(_('Call sign'), max_length=100, unique=True, blank=False)
    status=models.PositiveSmallIntegerField(_('status'), choices=Status.choices, default=6, blank=False)
    
    vf = models.PositiveIntegerField('VF', default=0)
    zf = models.PositiveIntegerField('ZF', default=0)
    gf = models.PositiveIntegerField('GF', default=0)
    ms = models.PositiveIntegerField('MS', default=0)
    agt = models.PositiveIntegerField('AGT', default=0)
    
    info=models.CharField(_('Info'), max_length=200, blank=True)
    
    orga = models.ForeignKey(Orga, on_delete=models.RESTRICT, verbose_name=_('Organization'))    
    
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, verbose_name=_("Mission"), null=True, blank=True, default=None)
    
    def staff_total(self) -> int:
        return sum([self.vf, self.zf, self.gf, self.ms])
    
    def __str__(self):
        if self.mission:
            return f"{self.call_sign} [{self.status}] - Einsatz: {self.mission}"
        else:
            return f"{self.call_sign} [{self.status}]"

