from django.db import models 

KATEGORIEN = (("Kate 3", "Kate 3"),("Kate 5", "Kate 5"),)

class Kunde (models.Model): 
    kunden_id = models.AutoField (primary_key = True) 
    nachname = models.CharField(max_length=50) 
    vorname = models.CharField(max_length=50) 
    titel = models.CharField(max_length=50, blank=True) 
    telefonnummer = models.CharField(max_length=50) 
    organisation = models.CharField(max_length=50, blank=True) 
    strasse = models.CharField(max_length=50) 
    plz = models.CharField(max_length=50) 
    stadt = models.CharField(max_length=50) 
    email = models.EmailField(max_length=75) 
    kundengruppe = models.CharField(max_length=50, choices=KATEGORIEN) #Gruppennamen variabel
    privatkunde = models.BooleanField(default=True)
    kreditwuerdig = models.BooleanField(default=False) 
    konto_id = models.ForeignKey("Konto")
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.nachname)
    
class Konto (models.Model): 
    konto_id = models.AutoField(primary_key=True) 
    IBAN = models.PositiveIntegerField(max_length=34) 
    kontoinhaber = models.CharField(max_length=50) 
    BLZ = models.PositiveIntegerField(max_length=30)
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.konto_id) 
    
