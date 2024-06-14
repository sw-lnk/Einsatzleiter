from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Mission(models.Model):
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
    zip_code=models.CharField(_('zip code'), max_length=10, blank=True)
    
    status=models.CharField(_('status'), max_length=15, choices=STATUS_CHOICES, default=UNTREATED, blank=False)
    prio=models.CharField(_('priority'), max_length=15, choices=PRIO_CHOICES, default=MEDIUM, blank=False)
    
    start=models.DateTimeField(_('start time'), default=timezone.now, blank=False, null=False)
    end=models.DateTimeField(_('end time'), blank=True, null=True)
    
    creation=models.DateTimeField(_('creation time'), auto_now_add=True, editable=False)
    update=models.DateTimeField(_('update time'), auto_now=True)
    
    archiv=models.BooleanField(_('archiv'), default=False)
    
    def address(self) -> str:
        a = self.street
        if self.street_no:
            a += f' {self.street_no}'
        if self.zip_code:
            a += f', {self.zip_code}'
        return a
    
    def __str__(self):
        return f'{self.keyword} - {self.street}'