from django.shortcuts import render_to_response
from lager.models import Produkt, Lieferant
from einkauf.models import Bestellanforderung, Bestellung, Bestellposition
from mitteilungen.views import message_read
from kauf.models import Kauf
from django.http.response import HttpResponseRedirect, HttpResponse
from einkauf.forms import BanfForm, BestellForm, WarenpositionForm,\
    WarenpositionDetailForm, BanfOverviewForm, BestellpositionForm
from django.core.context_processors import csrf
from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory
import json
from mitteilungen.models import MitteilungKauf, MitteilungBanf

# Create your views here.
def show_banf_details(request, banf_id, mitteilung_id=None):
    if mitteilung_id>0:
        message_read(request, mitteilung_id)
    banf = Bestellanforderung.objects.get(banf_id=banf_id)
    fabrikat = Produkt.objects.filter(fabrikat=banf.fabrikat).select_subclasses()[0]
    lieferant = fabrikat.lieferant
    banfs = Bestellanforderung.objects.filter(bestellt=False)
    bestellsumme =0;
    for b in banfs:
        f = Produkt.objects.filter(fabrikat=b.fabrikat).select_subclasses()[0]
        if f.lieferant == lieferant and b.banf_id != banf.banf_id:
            bestellsumme+= b.menge*f.EK
    
    errors=""
    
    if request.POST:
        banfForm = BanfForm(request.POST, instance=banf)
        if banfForm.is_valid():
            banfForm.save()
            return HttpResponseRedirect('/einkauf/Bestellanforderung/overview')
            
        else:
            errors= banfForm.errors
    else:
        ek = fabrikat.EK
        initial={
                 'fabrikat': banf.fabrikat,
                 'menge': banf.menge,
                 'einkaufspreis_banf': ek,
                 'summe_banf': ek*banf.menge,
                 }
        banfForm = BanfForm(initial)
    
    c={
       'form': banfForm,
       'errors': errors,
       'id': banf_id,
       'lieferant': lieferant,
       'bestellsumme': bestellsumme,
       
       }
    
    c.update(csrf(request))
    return render_to_response('banf_Details.html', c)

def create_bestellung_without_banf(request):
    lieferanten = Lieferant.objects.all()
    formsetPosition = formset_factory(BestellpositionForm)
    errors=""
    errors_position =""
    models=[]
    
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        if model not in models:
            models.append(model)
    if request.POST:
        formBestellung=BestellForm(request.POST)
        positionenFormset = formsetPosition(request.POST, request.FILES)
        if positionenFormset.is_valid() and formBestellung.is_valid():
            bestellung = formBestellung.save()
            for form in positionenFormset:
                fabrikat = form.cleaned_data['produkt_bestellung']
                fabrikat = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0]
                menge = form.cleaned_data['anzahl_bestellung']
                position = Bestellposition(fabrikat=fabrikat.fabrikat, menge=menge)
                position.save()
                bestellung.bestellposition.add(position)
                fabrikat.EK = form.cleaned_data['einkaufspreis_bestellung']
                fabrikat.save()
            bestellung.status_offen=True
            bestellung.save()
            return HttpResponseRedirect('/einkauf/Bestellung/overview')
        else:
            errors = formBestellung.errors
            errors_position=positionenFormset
    else:
        positionenFormset=formsetPosition()
        formBestellung= BestellForm

    c={
       'form': formBestellung,
       'positionFormset': positionenFormset,
       'errors': errors,
       'errors_position': errors_position,
       'models': models,
       'lieferanten': lieferanten
       }
    c.update(csrf(request))    
    return render_to_response('createBestellung_withoutBanf.html', c)

def create_wareneingang(request):
    lieferanten = Lieferant.objects.all()
    formsetPosition = formset_factory(BestellpositionForm)
    errors_position =""
    models=[]
    
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        if model not in models:
            models.append(model)
    if request.POST:

        positionenFormset = formsetPosition(request.POST, request.FILES)
        if positionenFormset.is_valid():
            for form in positionenFormset:
                fabrikat = form.cleaned_data['produkt_bestellung']
                fabrikat = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0]
                menge = form.cleaned_data['anzahl_bestellung']
                fabrikat.lagerbestand += menge
                fabrikat.EK = form.cleaned_data['einkaufspreis_bestellung']
                fabrikat.save()
            return HttpResponseRedirect('/lager/overview')
        else:
            errors_position=positionenFormset
    else:
        positionenFormset=formsetPosition()

    c={
       'positionFormset': positionenFormset,
       'errors_position': errors_position,
       'models': models,
       'lieferanten': lieferanten
       }
    c.update(csrf(request))    
    return render_to_response('createWareneingang.html', c)


def create_bestellung(request, lieferanten_id):
    lieferant = Lieferant.objects.get(lieferanten_id=lieferanten_id)
    banfs = Bestellanforderung.objects.filter(bestellt=False)
    bestellpositionen =[]
    for banf in banfs:
        fabrikat = Produkt.objects.filter(fabrikat=banf.fabrikat).select_subclasses()[0]
        if fabrikat.lieferant == lieferant:
            bestellpositionen.append(banf)
            
    errors_bestellung=""
    errors_positionen=""
    mindestbestellwert_error=""
            
    positionenFormset = formset_factory(WarenpositionForm)
    if request.POST:
        bestellForm = BestellForm(request.POST)
        positionenForm = positionenFormset(request.POST, request.FILES)
        if bestellForm.is_valid() and positionenForm.is_valid():
            if bestellForm.cleaned_data['summe']>=lieferant.mindestbestellwert:
                bestellung = bestellForm.save()
                for form in positionenForm:
                    fabrikat = form.cleaned_data['produkt']
                    menge = form.cleaned_data['anzahl']
                    position = Bestellposition(fabrikat=fabrikat, menge=menge)
                    position.save()
                    bestellung.bestellposition.add(position)
                    p = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0]
                    p.EK = form.cleaned_data['einkaufspreis']
                    p.save()
                bestellung.status_offen=True
                bestellung.save()
                for banf in bestellpositionen:
                    banf.bestellt=True
                    banf.save()
                    
                return HttpResponseRedirect('/einkauf/Bestellung/overview')
            else: 
                mindestbestellwert_error="Bestellung kann nur ab einem Mindestbestellwert von "+str(lieferant.mindestbestellwert)+"EUR versandt werden."
        else:
            errors_bestellung=bestellForm.errors
            errors_positionen=positionenForm.errors
    else:
        
        data={
              'form-TOTAL_FORMS': len(bestellpositionen),
              'form-INITIAL_FORMS': len(bestellpositionen),
              'form-MAX_NUM_FORMS': len(bestellpositionen),
              }
        counter=0;
        summe=0;
        for position in bestellpositionen:
            fabrikat = position.fabrikat
            produkt = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0]
            data['form-'+str(counter)+'-produkt']= produkt.fabrikat
            data['form-'+str(counter)+'-anzahl']= position.menge
            data['form-'+str(counter)+'-einkaufspreis']= produkt.EK
            data['form-'+str(counter)+'-summe']= produkt.EK*position.menge
            summe+= produkt.EK*position.menge
            counter+=1

                
        positionenForm = positionenFormset(data=data)
        bestellForm = BestellForm(initial={'summe':summe,})
    c={
       'bestellForm': bestellForm,
       'positionenForm': positionenForm,
       'errors_bestellung': errors_bestellung,
       'errors_positionen': errors_positionen,
       'lieferant': lieferant,
       'mindestbestellwert_error': mindestbestellwert_error,
       }

    c.update(csrf(request))
    return render_to_response('createBestellung.html', c)
    

def show_bestellung_overview(request):
    bestellungen = Bestellung.objects.all().order_by('-bestell_id')
    bestellungen_l ={}
    for bestellung in bestellungen:
        fabrikat = bestellung.bestellposition.all()[0].fabrikat
        fabrikat = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0]
        bestellungen_l[fabrikat.lieferant]={}
    
    for bestellung in bestellungen:
        fabrikat = bestellung.bestellposition.all()[0].fabrikat
        fabrikat = Produkt.objects.filter(fabrikat=fabrikat).select_subclasses()[0]
        bestellungen_l[fabrikat.lieferant][bestellung.bestell_id]=bestellung
    
    c={
       'bestellungen_l': bestellungen_l,
       }
    
    return render_to_response('bestellung_overview.html', c)

def show_banf_overview(request):

    banfs = Bestellanforderung.objects.filter(bestellt=False)
    lieferanten={}
    for banf in banfs:
        fabrikat = Produkt.objects.filter(fabrikat=banf.fabrikat).select_subclasses()[0]
        lieferanten[fabrikat.lieferant]={}
    for banf in banfs:
        fabrikat = Produkt.objects.filter(fabrikat=banf.fabrikat).select_subclasses()[0]
        lieferanten[fabrikat.lieferant][banf.banf_id]= BanfOverviewForm(data=model_to_dict(banf, fields=('fabrikat', 'menge'),))
        
    c={
       'lieferanten': lieferanten,
       }
    return render_to_response('banf_overview.html', c)
    
def show_details_bestellung(request, bestell_id):
    bestellung = Bestellung.objects.get(bestell_id=bestell_id)
    
    formset = formset_factory(WarenpositionDetailForm)
    
    if request.POST:
        positionenForm = formset(request.POST, request.FILES)
        positionen=[]
        for position in bestellung.bestellposition.all():
            positionen.append(position)
        counter=0;
        for form in positionenForm:
            bestellposition = positionen[counter]
            if 'checked' in str(form['erhalten']) and bestellposition.erhalten==False:
                bestellposition.erhalten = True
                bestellposition.save()
                fabrikat = Produkt.objects.filter(fabrikat=bestellposition.fabrikat).select_subclasses()[0]
                if fabrikat.lagerbestand==0:
                    #nicht vorraetigen Produkte
                    kaufe = Kauf.objects.filter(abgeschlossen=False).filter(warenposition__fabrikat=fabrikat)
                    for kauf in kaufe:
                        mitteilung = MitteilungKauf(kauf=kauf, nachricht=str(fabrikat.fabrikat)+" kam an")
                        mitteilung.save()  
                fabrikat.lagerbestand+= bestellposition.menge 
                fabrikat.save()
            counter+=1
        
        return HttpResponseRedirect('/einkauf/Bestellung/overview')
                    
    else:
        initial={
                 'form-TOTAL_FORMS': len(bestellung.bestellposition.all()),
                 'form-INITIAL_FORMS': len(bestellung.bestellposition.all()),
                 'form-MAX_NUM_FORMS': len(bestellung.bestellposition.all()),
                 }
        counter=0;
        for position in bestellung.bestellposition.all():
            produkt = Produkt.objects.filter(fabrikat=position.fabrikat).select_subclasses()[0]

            initial['form-'+str(counter)+'-produkt']= produkt.fabrikat
            initial['form-'+str(counter)+'-anzahl']= position.menge
            initial['form-'+str(counter)+'-einkaufspreis']=produkt.EK
            initial['form-'+str(counter)+'-summe']=position.menge*produkt.EK
            initial['form-'+str(counter)+'-erhalten']=position.erhalten
            counter+=1
            lieferant = produkt.lieferant
            
        bestellung = BestellForm(data=model_to_dict(bestellung))
        positionenForm=formset(data=initial)
        c={
           'bestellung':bestellung,
           'positionen': positionenForm,
           'id': bestell_id,
           'lieferant': lieferant,
           }
        c.update(csrf(request))
        return render_to_response('bestellung_Details.html', c)
        

def close_bestellung(request, bestell_id):
    bestellung = Bestellung.objects.get(bestell_id=bestell_id)
    bestellung.status_offen =False
    bestellung.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def pay_bestellung(request, bestell_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def upload_document(request, bestell_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def download_bestellung(request, bestell_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def scan_products(request, bestell_id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def check_for_banf (fabrikats_id, kauf_id):
    fabrikat = Produkt.objects.get_subclass(fabrikats_id=fabrikats_id)
    amount=0;
    counter=0;
    if fabrikat.lagerbestand<= fabrikat.meldebestand:
        if fabrikat.lagerbestand==0:
            kauf = Kauf.objects.get(kauf_id=kauf_id)
            positionen = kauf.warenposition.filter(fabrikat=fabrikat.fabrikat)
            amount=fabrikat.meldebestand;
            for position in positionen:
                amount+=position.menge

        bestellungen = Bestellung.objects.filter(bestellposition__fabrikat=fabrikat)
        counter=len(bestellungen)
        for bestellung in bestellungen:
            for position in bestellung.bestellposition.all():
                if position.fabrikat==fabrikat.fabrikat:
                    amount += position.menge
        if counter>0:
            amount= amount/counter
        else:
            amount=1
        banf_instance = Bestellanforderung.objects.filter(bestellt=False).filter(fabrikat=fabrikat.fabrikat)
        if len(banf_instance)>0:
            counter+=1
            banf_instance[0].menge+=amount/counter
            banf_instance[0].save()
            mitteilung = MitteilungBanf(bestellanforderung=banf_instance[0], nachricht='Bestellanforderung zu '+str(banf_instance[0].fabrikat)+' aktualisiert.')
            mitteilung.save()
        else:
            banf = Bestellanforderung(fabrikat=fabrikat, menge=amount)
            banf.save()
            
            mitteilung = MitteilungBanf(bestellanforderung=banf, nachricht='Neue Bestellanforderung zu '+str(banf.fabrikat)+' erstellt.')
            mitteilung.save()
        


def get_produkte_zu_lieferant(request):
    lieferant = request.GET['lieferant']
    lieferant = Lieferant.objects.filter(firmenname=lieferant)[0]
    p = Produkt.objects.all().select_subclasses()
    produkte={}
    for produkt in p:
        if produkt.lieferant == lieferant:
            produkte[produkt.fabrikats_id]=produkt.fabrikat

    produkte = json.dumps(produkte, ensure_ascii=False)
    return HttpResponse(produkte,content_type='application/json')
    