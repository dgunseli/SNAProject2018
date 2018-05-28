
from .models import EczaneBilgi,FirmaBilgi,SatisDokumBilgi

def setPharmacySessionData(request):
    pharmacyList = []
    tumEczaneler = EczaneBilgi()
    prm = EczaneBilgi()
    prm.eczane_adi = 'Tümü'
    prm.eczane_id = -1
    pharmacyList.append(prm)
    pharmacyIdList = SatisDokumBilgi.objects.exclude(eczane=None).values_list('eczane',flat = True).distinct().order_by('eczane')
    for val in pharmacyIdList:
        prm = EczaneBilgi()
        prm.eczane_adi = 'Eczane ' + str(val)
        prm.eczane_id = val
        pharmacyList.append(prm)
    return pharmacyList

    
def setFirmSessionData(request):
    firmList = []
    tumFirmalar = FirmaBilgi()
    prm = FirmaBilgi()
    prm.firma_adi = 'Tümü'
    prm.firma_id = -1
    firmList.append(prm)
    firmaList = SatisDokumBilgi.objects.exclude(eczane=None).values_list('firma_id',flat = True).distinct().order_by('firma_id')
    for val in firmaList:
        prm = FirmaBilgi()
        prm.firma_adi = 'Firma ' + str(val)
        prm.firma_id = val
        firmList.append(prm)
    return firmList