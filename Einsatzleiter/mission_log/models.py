import os
from dotenv import load_dotenv

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

load_dotenv()

# Create your models here.
class Mission(models.Model):
    ZIP_CODE = os.getenv("ZIP_CODE")
    
    UNTREATED = '0'
    PROCESSING= '1'
    CLOSED = '2'
    
    STATUS_CHOICES=(
        (UNTREATED, 'unbearbeitet'),
        (PROCESSING, 'in Arbeit'),
        (CLOSED, 'abgeschlossen')
    )

    HIGH = '1'
    MEDIUM = '2'
    LOW = '3'

    PRIO_CHOICES=(
        (HIGH, 'hoch'),
        (MEDIUM, 'mittel'),
        (LOW, 'niedrig'),
    )
    
    main_id=models.IntegerField(_('main id'), primary_key=True)
    keyword=models.CharField(_('keyword'), max_length=100, blank=False)
    street=models.CharField(_('street'), max_length=100, blank=False)
    street_no=models.CharField(_('street no'), max_length=10, blank=True)
    zip_code=models.CharField(_('zip code'), max_length=5, default=ZIP_CODE, blank=True)
    
    status=models.CharField(_('status'), max_length=15, choices=STATUS_CHOICES, default=UNTREATED, blank=False)
    prio=models.CharField(_('priority'), max_length=15, choices=PRIO_CHOICES, default=MEDIUM, blank=False)
    
    start=models.DateTimeField(_('start time'), default=timezone.now, blank=False, null=False)
    end=models.DateTimeField(_('end time'), blank=True, null=True)
    
    creation=models.DateTimeField(_('creation time'), auto_now_add=True, editable=False)
    update=models.DateTimeField(_('update time'), auto_now=True)
    
    archiv=models.BooleanField(_('archiv'), default=False)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        editable=False,
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
        for k, v in self.STATUS_CHOICES:
            if k == self.status:
               status_value = v
        
        for k, v in self.PRIO_CHOICES:
            if k == self.prio:
               prio_value = v
        
        return f'{self.keyword}, Status: {status_value}, Prio: {prio_value} - {self.address()}'
    
    def __str__(self):
        return f'{self.keyword} - {self.street}'


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
    
    def __str__(self):
        return f"{self.time.strftime('%d.%m.%Y %H:%M')}: {self.text}"


class Orga(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True, blank=False)
    
    def __str__(self):
        return self.name


class Vehicle(models.Model):
    
    STATUS_CHOICES=(
        (0, 'Priorisierter Sprechwunsch'),
        (1, 'Einsatzbereit Funk'),
        (2, 'Einsatzbereit Wache'),
        (3, 'Einsatz übernommen'),
        (4, 'Einsatzstelle an'),
        (5, 'Sprechwunsch'),
        (6, 'Nicht einsatzbereit'),
        (7, 'Patient aufgenommen'),
        (8, 'Ankunft Krankenhaus'),
        (9, 'Abruf Einsatzauftrag/Fremdanmeldung')
    )
    
    call_sign = models.CharField(_('Call sign'), max_length=100, unique=True, blank=False)
    status=models.IntegerField(_('status'), choices=STATUS_CHOICES, default=6, blank=False)
    
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
        return f"{self.call_sign} ({self.orga})"