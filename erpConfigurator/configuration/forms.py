from django import forms
from .models import Configuration
from configuration.models import Produkttyp, Kundengruppe, Produktkategorie

BEDARF = ((True, 'automatisiert: zu den Produkten werden Mindestbestaende hinterlegt, Bestellung wird angestossen, sobald weniger Produkte auf Lager sind'), 
          (False,'manuell: wir sehen, wann Produkte zur Neige gehen, wissen wie viel wir bestellen wollen und starten daraufhin die Bestellung'))


class ConfigurationsForm (forms.ModelForm):
    
    class Meta:
        model= Configuration
        exclude = ['produkttypen', 'kundengruppen']
        widgets ={'bedarf': forms.RadioSelect(attrs={'class': 'radio'}, choices=BEDARF),
                  'bestellung': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'bestellung_intern': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'bestellung_extern': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'scanner': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'bezahlung': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'angebot': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'kaufabschluss': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'scanner_kauf': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'zahlung': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'filtern': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'inventur': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  'kunde_filtern': forms.RadioSelect(attrs={'class': 'radio'}, choices=((True,'ja'), (False,'nein'))),
                  } 
                   

class ProdukttypForm (forms.ModelForm):
    
    class Meta: 
        model= Produkttyp
        fields = ['produkttyp_name', 'artikelnummer', 'produktkategorie', 'kategorien', 'hersteller', 'beschreibung', 'lieferant',
                   'listenpreisVK', 'ausmasse', 'farben', 'mwst_klasse', 'durchschn_EK', 'letzter_EK',
                   'bemerkung','ean_nummer']
        
class KundengruppeForm (forms.ModelForm):
    
    class Meta: 
        model= Kundengruppe
        fields = ['name']
        
class ProduktkategorieForm (forms.ModelForm):
    
    class Meta: 
        model= Produktkategorie
        fields = ['kategorie']