"""
Definition of models.
"""

from django.db import models
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.


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
    def to_json(self):  
        return '{{"madde": "{0}" ,"firma_id" : {1} }}'.format(self.madde, int(self.firma_id))
    

class EczaneBilgi(object):
    eczane_adi = str
    eczane_id = int
    managed = False
    def as_EczaneBilgi(dct):
        bilgi = EczaneBilgi()
        bilgi.eczane_adi = dct['eczane_adi']
        bilgi.eczane_id = dct['eczane_id']
        return bilgi
    def __init__(self):
        self.eczane_adi = ""
        self.eczane_id =-1
    def __init__(self,*eczane_adi,**eczane_id):
        self.eczane_adi = eczane_adi
        self.eczane_id =eczane_id
    def to_json(self):  
        return '{{"eczane_adi": "{0}" ,"eczane_id" : {1} }}'.format(self.eczane_adi, int(self.eczane_id))

class FirmaBilgi(object):
    firma_adi = str
    firma_id = int
    managed = False
    def as_FirmaBilgi(dct):
        bilgi = FirmaBilgi()
        bilgi.firma_adi = dct['firma_adi']
        bilgi.firma_id = dct['firma_id']
        return bilgi
    def __init__(self,*firma_adi,**firma_id):
        self.firma_adi = firma_adi
        self.firma_id = firma_id
    def __init__(self):
        self.firma_adi = ""
        self.firma_id = -1
    def to_json(self):  
        return '{{"firma_adi": "{0}" ,"firma_id" : {1} }}'.format(self.firma_adi, int(self.firma_id))