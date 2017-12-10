from django import forms
from lager.models import Inventurposition, Produkt, Lautsprecher
from lager.models import Faden, PRODUKTKATEGORIEN, Lieferant,\
    MWST_KLASSEN

class LautsprecherForm (forms.ModelForm):
    class Meta:
        model= Lautsprecher
        exclude=['lagerbestand', 'durchschn_EK', 'letzter_EK']
        
        
class FadenForm (forms.ModelForm):
    class Meta:
        model= Faden
        exclude=['lagerbestand', 'durchschn_EK', 'letzter_EK']
        
class ProduktOverviewForm (forms.ModelForm):
    class Meta:
        model= Produkt
        exclude=['seriennummer', ]
        
class LieferantForm (forms.ModelForm):
    class Meta:
        model=Lieferant
        exclude=['konto_id']
        
class FilterForm (forms.Form):
    fabrikat = forms.CharField(max_length=50)
    seriennummer = forms.IntegerField ()
    kategorie = forms.ChoiceField(choices=PRODUKTKATEGORIEN)
    hersteller = forms.CharField(max_length=50)
    lieferant = forms.ModelChoiceField(queryset=Lieferant.objects.all())
    mwst_klasse = forms.ChoiceField(choices=MWST_KLASSEN)
    
class InventurForm (forms.ModelForm):
    EK = forms.DecimalField(max_digits=8, decimal_places=2, label="Einkaufspreis")
    class Meta:
        model= Inventurposition
        fields =['produkt', 'lagerbestand_real', 'EK', 'gesamtwert']
        widgets={
                 'produkt': forms.TextInput(attrs={'readonly':'readonly'}),
                 'gesamtwert': forms.TextInput(attrs={'readonly':'readonly'}),
                 }