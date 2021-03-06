from django.shortcuts import render_to_response
from kauf.forms import AngebotForm, WarenpositionForm, KaufForm,\
    WarenpositionDetailForm, KaufDetailForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from kunden.models import Kunde
from django.forms.formsets import formset_factory
from lager.models import Produkt
from django.core import serializers
from kauf.models import Warenposition, Angebot, Kauf
from einkauf.views import check_for_banf
from django.forms.models import model_to_dict
from mitteilungen.views import message_read

# Create your views here.
def create_offer(request, kunden_id):
    
    kunde = Kunde.objects.get(kunden_id=kunden_id)
    formsetPosition = formset_factory(WarenpositionForm)
    errors=""
    errors_position =""
    
    models=[]
    
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        if model not in models:
            models.append(model)
    
    if request.POST:
        formAngebot = AngebotForm(request.POST)
        positionFormset = formsetPosition(request.POST, request.FILES)
        if formAngebot.is_valid() and positionFormset.is_valid():
            
            angebot = formAngebot.save(commit=False)
            angebot.kunde = kunde
            formAngebot.save()
            for form in positionFormset:
                position = Warenposition(fabrikat= form.cleaned_data['produkt'], menge = form.cleaned_data['menge'])
                position.save()
                angebot.warenposition.add(position)
            
            angebot.save()
            
            
            return HttpResponseRedirect('/kunden/'+str(kunde.kunden_id)+'/kaufhistorie')
        else:
            errors =formAngebot.errors
            errors_position = positionFormset.errors
            
    else:
        formAngebot = AngebotForm
        positionFormset = formsetPosition
    
    c={
       'form': formAngebot,
       'positionFormset': positionFormset,
       'id': kunde.kunden_id,
       'errors_offer': errors,
       'errors_position': errors_position,
       'models': models,
       }
    
    c.update(csrf(request))
    return render_to_response('createAngebot.html', c)

def create_purchase(request, kunden_id):
    
    kunde = Kunde.objects.get(kunden_id=kunden_id)
    formsetPosition = formset_factory(WarenpositionForm)
    errors=""
    errors_position =""
    models=[]
    
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        if model not in models:
            models.append(model)
            
    
    if request.POST:
        formKauf = KaufForm(request.POST)
        positionFormset = formsetPosition(request.POST, request.FILES)
        produkte=[]
        if formKauf.is_valid() and positionFormset.is_valid():
            
            kauf = formKauf.save(commit=False)
            kauf.kunde = kunde
            formKauf.save()
            abgeschlossen = True
            for form in positionFormset:
                fabrikat =form.cleaned_data['produkt_kauf']
                menge = form.cleaned_data['menge']
                position = Warenposition(fabrikat=fabrikat , menge = menge)
                position.save()
                kauf.warenposition.add(position)
                produkt = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0] 
                bestand = produkt.lagerbestand
                produkt.lagerbestand =int(bestand) - int(menge)
                if produkt.lagerbestand<=0:
                    produkt.lagerbestand=0
                    position = Warenposition.objects.get(position_id=position.position_id)
                    position.available=False
                    position.save()
                    abgeschlossen=False
                produkt.save()
                produkte.append(produkt)
            kauf.abgeschlossen=abgeschlossen
            kauf.save()
            for produkt in produkte:
                check_for_banf(produkt.fabrikats_id, kauf.kauf_id)
            
            
            return HttpResponseRedirect('/kunden/'+str(kunde.kunden_id)+'/kaufhistorie')
        else:
            errors =formKauf.errors
            errors_position = positionFormset.errors
            
    else:
        formKauf= KaufForm
        positionFormset = formsetPosition
    
    c={
       'form': formKauf,
       'positionFormset': positionFormset,
       'id': kunde.kunden_id,
       'errors': errors,
       'errors_position': errors_position,
       'models': models,
       }
    
    c.update(csrf(request))
    return render_to_response('createKauf.html', c)

def show_kauf_details (request, kunden_id, kauf_id, mitteilung_id=None):
    if mitteilung_id>0:
        message_read(request, mitteilung_id)
    kauf = Kauf.objects.get(kauf_id=kauf_id)
    formset = formset_factory(WarenpositionDetailForm)
    
    if request.POST:
        if kauf.abgeschlossen==True:
            return HttpResponseRedirect('/kunden/'+str(kunden_id)+'/kaufhistorie')
        else:
            positionen=[]
            for position in kauf.warenposition.all():
                positionen.append(position)
            produkte=[]
            abgeschlossen=True
            for position in positionen:
                if position.available==False: 
                    produkt = Produkt.objects.filter(fabrikat=position.fabrikat).select_subclasses()[0]
                    if produkt.lagerbestand>= position.menge:
                        position.available=True
                        produkt.lagerbestand -= position.menge
                        produkt.save()
                        position.save()
                        
                    else:
                        abgeschlossen=False
                        if produkt not in produkte:
                            print str(produkt)+' in Details'
                            produkte.append(produkt)
            kauf.abgeschlossen=abgeschlossen
            kauf.save()            
            for produkt in produkte:
                check_for_banf(produkt.fabrikats_id, kauf_id)
            return HttpResponseRedirect('/kunden/'+str(kunden_id)+'/kaufhistorie')
    else:
        initial={
                 'form-TOTAL_FORMS': len(kauf.warenposition.all()),
                 'form-INITIAL_FORMS': len(kauf.warenposition.all()),
                 'form-MAX_NUM_FORMS': len(kauf.warenposition.all()),
                 }          
        counter=0;
        for position in kauf.warenposition.all():
            produkt = Produkt.objects.filter(fabrikat=position.fabrikat).select_subclasses()[0]
            initial['form-'+str(counter)+'-produkt']=produkt.fabrikat
            initial['form-'+str(counter)+'-menge']=position.menge
            initial['form-'+str(counter)+'-einzelpreis']=produkt.verkaufspreis
            initial['form-'+str(counter)+'-summe']=produkt.verkaufspreis*position.menge
            if kauf.abgeschlossen:
                initial['form-'+str(counter)+'-available']=True
            else:
                initial['form-'+str(counter)+'-available']=produkt.lagerbestand>= position.menge
            counter+=1
        kauf = KaufDetailForm(data=model_to_dict(kauf))
        positionenForm = formset(data=initial)
        c={
           'kauf': kauf,
           'positionen': positionenForm,
           'kauf_id': kauf_id,
           'kunden_id': kunden_id,
           }
            
            
        c.update(csrf(request))
        return render_to_response('kauf_Details.html', c)

def show_orderhistory_with_offer(request, kunden_id):
    kunde = Kunde.objects.get(kunden_id=kunden_id)
    angebote = Angebot.objects.filter(kunde=kunde).order_by('-angebot_id')
    kaufe = Kauf.objects.filter(kunde=kunde).order_by('-kauf_id')
    
    c={
       'kunde':kunde,
       'angebote':angebote,
       'kaufe': kaufe,
       }
    
    c.update(csrf(request))
    return render_to_response('kaufhistorie.html', c)

def show_orderhistory_without_offer(request, kunden_id):
    kunde = Kunde.objects.get(kunden_id=kunden_id)
    kaufe = Kauf.objects.all().order_by('-kauf_id')
    
    c={
       'kunde':kunde,
       'kaufe': kaufe,
       }
    
    c.update(csrf(request))
    return render_to_response('kaufhistorie.html', c)
    
    
def check_credit(request, kunden_id):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def check_payment(request, kunden_id):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def scan_products(request, kunden_id):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def show_angebot_details (request, kunden_id, angebot_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def download_purchase(request, kunden_id, kauf_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def download_offer (request, kunden_id, angebot_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create_purchase_from_offer (request, kunden_id, angebot_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_Preis(request):
    if request.GET:
        fabrikats_id = request.GET['fabrikat']
        fabrikat = Produkt.objects.filter(fabrikats_id=fabrikats_id)
        data = serializers.serialize('json',fabrikat)
        data = data[1:-1]
    return HttpResponse(data,content_type='application/json')