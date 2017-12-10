from django.db import models
from model_utils.managers import InheritanceManager

# Create your models here.
class Mitteilung (models.Model):
    mitteilung_id = models.AutoField(primary_key=True)  
    nachricht = models.TextField() 
    gelesen = models.BooleanField(default=False)
    
    objects = InheritanceManager()
    
class MitteilungKauf (Mitteilung): 
    kauf = models.ForeignKey("kauf.Kauf") 
    
class MitteilungBanf (Mitteilung):  
    bestellanforderung = models.ForeignKey("einkauf.Bestellanforderung") 
