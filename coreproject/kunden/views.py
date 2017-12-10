from django.shortcuts import render_to_response
from kunden.forms import KundenForm, KontoForm, FilterForm
from django.http.response import HttpResponseRedirect
from django.core.context_processors import csrf
from kunden.models import Kunde
from django.forms.models import model_to_dict

# Create your views here.
def create_with_account (request):
    if request.POST:
        formKunde = KundenForm(request.POST)
        formKonto = KontoForm (request.POST)
        if formKunde.is_valid() and formKonto.is_valid():
            konto = formKonto.save()
            kunde= formKunde.save(commit=False)
            kunde.konto_id = konto
            kunde.save()
            return HttpResponseRedirect('/kunden/overview')
    else:
        formKunde = KundenForm
        formKonto = KontoForm
        
    c= {'formKunde': formKunde,
        'formKonto': formKonto,
        }
    c.update(csrf(request))
    return render_to_response('createKunde.html', c)

def create_without_account (request):
    if request.POST:
        formKunde = KundenForm(request.POST)
        if formKunde.is_valid():
            formKunde.save()
            return HttpResponseRedirect('/kunden/overview')
    else:
        formKunde = KundenForm
        
    c= {'formKunde': formKunde,
        }
    c.update(csrf(request))
    return render_to_response('createKunde.html', c)

def get_overview_filter (request):
    
    if request.POST:
        formfilter= FilterForm(request.POST)
        if formfilter.is_valid:
            #adaptFilter
            return HttpResponseRedirect('/kunden/overview')
        
    else:
        formfilter = FilterForm
    
    object={}
 
    for kunde in Kunde.objects.all():
        object[kunde.kunden_id] = KundenForm(data=model_to_dict(kunde))
    c= {'kunden': object,
        'filter': formfilter,
        }
    c.update(csrf(request))
    
    return render_to_response('overviewKunde.html', c)

def get_overview (request):
    
    object={}
      
    for kunde in Kunde.objects.all():
        object[kunde.kunden_id] = KundenForm(data=model_to_dict(kunde))

    c= {'kunden': object,
        }
    c.update(csrf(request))
    
    return render_to_response('overviewKunde.html', c)

def details(request, kunden_id):
    kunde = Kunde.objects.get(kunden_id=kunden_id)
    errors=""
    
    if request.POST:
        formKunde = KundenForm(request.POST, instance=kunde)
        if formKunde.is_valid():
            formKunde.save()
            return HttpResponseRedirect('/kunden/overview')
        else:
            errors=formKunde.errors
    
    kunde = KundenForm(data=model_to_dict(kunde))
    c= {'kunde': kunde,
        'id': kunden_id,
        'errors': errors}
    c.update(csrf(request))
    return render_to_response('detailsKunde.html', c)

def details_with_account(request, kunden_id):
    kunde = Kunde.objects.get(kunden_id=kunden_id)
    konto = kunde.konto_id
    errors=""
    errors_konto=""
    
    if request.POST:
        formKunde = KundenForm(request.POST, instance=kunde)
        formKonto = KontoForm(request.POST, instance=konto)
        if formKunde.is_valid() and formKonto.is_valid():
            formKunde.save()
            formKonto.save()
            return HttpResponseRedirect('/kunden/overview')
        else:
            errors=formKunde.errors
            errors_konto=formKonto.errors
    
    kunde = KundenForm(data=model_to_dict(kunde))
    konto = KontoForm(data=model_to_dict(konto))
    c= {'kunde': kunde,
        'konto': konto,
        'id': kunden_id,
        'errors_konto':errors_konto,
        'errors': errors}
    c.update(csrf(request))
    return render_to_response('detailsKunde.html', c)
        

def merge(request):
    
    return HttpResponseRedirect('/kunden/overview')

def export(request):
    
    return HttpResponseRedirect('/kunden/overview')