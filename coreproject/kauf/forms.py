from django import forms
from kauf.models import Angebot, Kauf
from lager.models import Produkt


class AngebotForm (forms.ModelForm):
    class Meta:
        model= Angebot
        exclude=['warenposition', 'kunde']
        widgets={
                 'summe': forms.TextInput(attrs={'readonly':"readonly", 'value': 0}),
                 'mehrwertsteuer': forms.TextInput(attrs={'readonly':"readonly", 'value':0}),
                 }

class KaufForm (forms.ModelForm):
    class Meta:
        model= Kauf
        exclude=['warenposition', 'kunde', 'abgeschlossen']
        widgets={
                 'summe': forms.TextInput(attrs={'readonly':"readonly", 'value': 0}),
                 'mehrwertsteuer': forms.TextInput(attrs={'readonly':"readonly", 'value':0}),
                 }
        
class KaufDetailForm(forms.ModelForm):
    class Meta:
        model=Kauf
        fields="__all__"
        
class WarenpositionForm (forms.Form):
    produkt_kauf = forms.ModelChoiceField(label="Produkt", queryset=Produkt.objects.all().select_subclasses())
    menge = forms.IntegerField(initial=1)
    einzelpreis = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    summe = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'readonly':'readonly'}))
    
class WarenpositionDetailForm (forms.Form):
    produkt = forms.CharField(max_length=50)
    menge = forms.IntegerField(initial=1)
    einzelpreis = forms.DecimalField(max_digits=10, decimal_places=2)
    summe = forms.DecimalField(max_digits=10, decimal_places=2)
    available = forms.BooleanField(label="Auf Lager")
        