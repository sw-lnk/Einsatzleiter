from django.db import models
from django.utils import timezone

# Create your models here.
class Mission(models.Model):
    UNTREATED = 'unbearbeitet'.upper()
    PROCESSING= 'bearbeitet'.upper()
    CLOSED = 'abgeschlossen'.upper()
    
    STATUS_CHOICES=(
        (UNTREATED, UNTREATED.lower()),
        (PROCESSING, PROCESSING.lower()),
        (CLOSED, CLOSED.lower())
    )
    
    main_id=models.IntegerField(primary_key=True)
    keyword=models.CharField(max_length=100, blank=False)
    street=models.CharField(max_length=100, blank=False)
    street_no=models.CharField(max_length=10, blank=True)
    zip_code=models.CharField(max_length=10, blank=True)
    
    status=models.CharField(max_length=15, choices=STATUS_CHOICES, default=UNTREATED, blank=False)
    
    start=models.DateTimeField(default=timezone.now, blank=False, null=False)
    end=models.DateTimeField(blank=True, null=True)
    
    creation=models.DateTimeField(auto_now_add=True, editable=False)
    update=models.DateTimeField(auto_now=True)
    
    archiv=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.keyword} - {self.street} ({self.status})'