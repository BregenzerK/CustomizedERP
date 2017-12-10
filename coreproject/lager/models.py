from django.db import models
from model_utils.managers import InheritanceManager

PRODUKTKATEGORIEN = (("Kurzwaren", "Kurzwaren"),("Elektronik", "Elektronik"),)
MWST_KLASSEN =((19,"19 Prozent"),(7,"7 Prozent"))
 
class Produkt (models.Model):
    fabrikats_id = models.AutoField(primary_key = True)
    fabrikat = models.CharField(max_length=50, unique=True) 
    verkaufspreis = models.DecimalField(max_digits=8, decimal_places=2)
    EK= models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    lagerbestand = models.PositiveIntegerField(default=0) 
    preisart = models.CharField(max_length=50, choices=(("Stueck","Einzelpreis"),("Gewicht", "Gewichtpreis"), ("Meter", "Meterpreis"))) 
    seriennummer = models.BooleanField(default=False)
   
    def __unicode__(self):
        return unicode(self.fabrikat)
    
    objects = InheritanceManager()

class Lautsprecher (Produkt):  
    artikelnummer = models.IntegerField(max_length=50) 
    produktkategorie = models.CharField(max_length=50, choices=PRODUKTKATEGORIEN) 
    hersteller = models.CharField(max_length=50) 
    produktbeschreibung = models.TextField() 
    lieferant = models.ForeignKey("Lieferant") 
    listenpreisVK = models.DecimalField(max_digits=8, decimal_places=2)  
    mwst_klasse = models.IntegerField(max_length=50, choices=MWST_KLASSEN)  
    durchschn_EK= models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
    letzter_EK = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
    bemerkung = models.TextField(blank=True) 
    meldebestand = models.IntegerField(max_length=5)
    
    def to_class_name(self):
        return self.__class__.__name__ 
    
class Instanzen_Lautsprecher (models.Model):
    id = models.AutoField(primary_key=True)
    seriennummer= models.IntegerField(unique=True)
    fabrikat= models.ForeignKey("Lautsprecher")
    verkauft= models.BooleanField(default=False)
    standort= models.CharField(max_length=50)
     
class Faden (Produkt):  
    artikelnummer = models.IntegerField(max_length=50) 
    produktkategorie = models.CharField(max_length=50, choices=PRODUKTKATEGORIEN) 
    hersteller = models.CharField(max_length=50) 
    produktbeschreibung = models.TextField() 
    lieferant = models.ForeignKey("Lieferant") 
    listenpreisVK = models.DecimalField(max_digits=8, decimal_places=2) 
    farben = models.CharField(max_length=50) 
    mwst_klasse = models.IntegerField(max_length=50, choices=MWST_KLASSEN) 
    durchschn_EK= models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
    letzter_EK = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
    bemerkung = models.TextField(blank=True) 
    meldebestand = models.IntegerField(max_length=5)
    
    
    def to_class_name(self):
        return self.__class__.__name__ 
    
class Instanzen_Faden (models.Model):
    id = models.AutoField(primary_key=True)
    seriennummer= models.IntegerField(unique=True)
    fabrikat= models.ForeignKey("Faden")
    verkauft= models.BooleanField(default=False)
    standort= models.CharField(max_length=50)
    
class Lieferant (models.Model): 
    lieferanten_id = models.AutoField(primary_key=True) 
    firmenname = models.CharField(max_length=50) 
    ansprechpartner = models.CharField(max_length=50)
    strasse = models.CharField(max_length=50) 
    plz = models.CharField(max_length=5) 
    stadt = models.CharField(max_length=50) 
    email = models.EmailField(max_length=75) 
    telefon = models.CharField(max_length=50) 
    homepage = models.URLField(max_length=200) 
    ust_id = models.CharField(max_length=50)
    mindestbestellwert = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
    konto_id = models.ForeignKey("kunden.Konto") 
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.firmenname)

class Inventur (models.Model):
    inventur_id = models.AutoField(primary_key=True)
    datum = models.DateField(auto_now=False, auto_now_add=True)
    position = models.ManyToManyField('Inventurposition', blank=True)

class Inventurposition (models.Model): 
    inventurposition_id = models.AutoField(primary_key=True) 
    produkt =  models.CharField(max_length=50)
    lagerbestand_real = models.IntegerField(max_length=50) 
    gesamtwert = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) 
