from django.db import models 
from datetime import datetime
class Bestellanforderung (models.Model): 
    banf_id = models.AutoField(primary_key=True) 
    fabrikat= models.CharField(max_length=50) 
    menge = models.IntegerField(max_length=5)
    bestellt= models.BooleanField(default=False) 
    def __unicode__(self):
        return unicode(self.banf_id)
    
 
class Bestellung (models.Model): 
    bestell_id = models.AutoField(primary_key=True) 
    bestellposition = models.ManyToManyField("Bestellposition") 
    summe = models.DecimalField(max_digits=10, decimal_places=2) 
    status_offen = models.BooleanField(default=True)  
    lieferort = models.CharField(max_length=50) 
    lieferdatum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) 
class Bestellposition (models.Model): 
    position_id = models.AutoField(primary_key=True) 
    fabrikat= models.CharField(max_length=50) 
    menge = models.IntegerField(max_length=5) 
    erhalten = models.BooleanField(default=False)
    def __unicode__(self):
        return unicode(str(self.menge)+'X '+str(self.fabrikat))
class ZahlungBestellung (models.Model): 
    zahlungs_id = models.AutoField(primary_key = True) 
    konto = models.ForeignKey("kunden.Konto") 
    bestellung = models.ForeignKey("Bestellung") 
    verwendungszweck = models.TextField() 
    datum = models.DateField(auto_now=False, auto_now_add=False) 
