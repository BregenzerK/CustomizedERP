from django import forms
from kunden.models import Kunde
from kunden.models import Konto, KATEGORIEN
from lager.models import Produkt, PRODUKTKATEGORIEN
class KundenForm (forms.ModelForm):
    class Meta:
        model= Kunde
        exclude = ['konto_id', 'kreditwuerdig']
        
class KontoForm (forms.ModelForm):
    class Meta:
        model= Konto
        fields = '__all__'
        
class FilterForm (forms.Form):
    nachname = forms.CharField(max_length=50)
    organisation = forms.CharField(max_length=50)
    plz = forms.CharField(max_length=50)
    stadt = forms.CharField(max_length=50)
    kundengruppe = forms.ChoiceField(choices= KATEGORIEN)
    privatkunde = forms.BooleanField()
    seriennummer = forms.IntegerField () 
    fabrikat = forms.ModelChoiceField(queryset=Produkt.objects.all().select_subclasses()) 
    kategorie = forms.ChoiceField(choices=PRODUKTKATEGORIEN) 
    kauf_von = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0, label="Kauf von")
    kauf_bis = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0, label="bis")
    