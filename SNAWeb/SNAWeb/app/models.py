"""
Definition of models.
"""

from django.db import models

# Create your models here.
class SatisDokumBilgi(models.Model):
    eczane = models.IntegerField()
    recete_no = models.TextField()
    islem_tarihi = models.DateTimeField(auto_now=False,blank=True, null=True)
    doktor_diploma_tescil_no = models.TextField(blank=True, null=True)
    verilen_adet = models.IntegerField()
    urun_id = models.IntegerField()
    sgketkinkod = models.TextField(blank=True, null=True)
    firma_id = models.IntegerField(blank=True, null=True)
    madde = models.TextField(blank=True, null=True)