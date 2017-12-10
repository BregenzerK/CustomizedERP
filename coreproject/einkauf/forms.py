from django import forms
from einkauf.models import Bestellanforderung, Bestellung
from lager.models import Produkt


class BanfForm (forms.ModelForm):
    einkaufspreis_banf= forms.DecimalField(max_digits=10, decimal_places=2, label="Einkaufspreis")
    summe_banf = forms.DecimalField(max_digits=10, decimal_places=2, label="Summe", widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    
    class Meta:
        model= Bestellanforderung
        exclude=[ 'bestellt']
        widgets = {
                   'fabrikat': forms.TextInput(attrs={'readonly':'readonly'}),
                   }
        
class BanfOverviewForm (forms.ModelForm):   
    class Meta:
        model= Bestellanforderung
        exclude=[ 'bestellt']

class BestellForm (forms.ModelForm):
    class Meta:
        model= Bestellung
        exclude=['bestellposition', 'status']
        widgets = {
                   'summe': forms.NumberInput(attrs={'readonly':'readonly'}),
                   }
        
class BestellpositionForm (forms.Form):
    produkt_bestellung = forms.ModelChoiceField(label="Produkt", queryset=Produkt.objects.all().select_subclasses())
    anzahl_bestellung = forms.IntegerField(initial=1, label="Menge")
    einkaufspreis_bestellung = forms.DecimalField(max_digits=10, decimal_places=2, label="Einkaufspreis")
    summe_bestellung = forms.DecimalField(max_digits=10, decimal_places=2, label="Summe", widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    
class WarenpositionForm (forms.Form):
    produkt = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'readonly':'readonly'}))
    anzahl = forms.IntegerField(initial=1, label="Menge")
    einkaufspreis = forms.DecimalField(max_digits=10, decimal_places=2)
    summe = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'readonly':'readonly'}))

class WarenpositionDetailForm (forms.Form):
    produkt = forms.CharField(max_length=50)
    anzahl = forms.IntegerField(initial=1, label="Menge")
    einkaufspreis = forms.DecimalField(max_digits=10, decimal_places=2)
    summe = forms.DecimalField(max_digits=10, decimal_places=2)
    erhalten = forms.BooleanField(initial=False)
        

        