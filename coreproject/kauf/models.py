from django.db import models 
from datetime import datetime
class Kauf (models.Model): 
    kauf_id = models.AutoField (primary_key=True) 
    kunde = models.ForeignKey("kunden.Kunde") 
    warenposition = models.ManyToManyField("Warenposition") 
    summe = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    mehrwertsteuer = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    rabatt = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    rabattarten = models.CharField(max_length=50, choices=(("prozentrabatt", "%"),("betragsrabatt", "EUR"),), blank=True) 
    rabattgrund = models.TextField(blank=True) 
    standort = models.CharField(max_length=50) 
    datum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) 
    abgeschlossen = models.BooleanField(default=False)
    def __unicode__(self):
        return unicode(self.kauf_id)
class Angebot (models.Model): 
    angebot_id = models.AutoField (primary_key=True) 
    kunde = models.ForeignKey("kunden.Kunde") 
    warenposition = models.ManyToManyField("Warenposition") 
    summe = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    mehrwertsteuer = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    rabatt = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    rabattarten = models.CharField(max_length=50, choices=(("prozentrabatt", "%"),("betragsrabatt", "EUR"),), blank=True) 
    rabattgrund = models.TextField(blank=True) 
    standort = models.CharField(max_length=50) 
    datum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) 
class Warenposition (models.Model): 
    position_id = models.AutoField(primary_key=True) 
    fabrikat= models.CharField(max_length=50) 
    menge = models.IntegerField(max_length=5) 
    available = models.BooleanField(default=True)
    def __unicode__(self):
        return unicode(str(self.menge)+'X '+str(self.fabrikat))
class ZahlungKauf (models.Model): 
    zahlungs_id = models.AutoField(primary_key = True) 
    konto = models.ForeignKey ("kunden.Konto") 
    kauf = models.ForeignKey("Kauf") 
    verwendungszweck = models.TextField() 
    datum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) 
    zahlart = models.CharField(max_length=20, choices=(("Raten", "Ratenzahlung"),("Kreditkarte", "Kreditkarte"),)) 
 
