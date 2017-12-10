from django.shortcuts import render_to_response
from lager.forms import LautsprecherForm, FadenForm,  FilterForm, ProduktOverviewForm,\
    LieferantForm, InventurForm
from django.http.response import HttpResponseRedirect
from django.core.context_processors import csrf
from lager.models import Produkt, Lieferant, Inventur
from django.forms.models import model_to_dict
from django.db.models.loading import get_model
from kunden.forms import KontoForm
from django.forms.formsets import formset_factory

def get_model_name(form):
    model = form.Meta.model
    model = str(model).replace("<class 'lager.models.", "")
    model = model.replace("'>", "") 
    return model

# Create your views here.
def create_Lautsprecher(request):
       
    model = get_model_name(LautsprecherForm)
   
    if request.POST:
        formProdukt = LautsprecherForm(request.POST)
        if formProdukt.is_valid():
            formProdukt.save()
            return HttpResponseRedirect('/lager/overview')
    else:
        formProdukt = LautsprecherForm
   
    c={
       'formProdukt': formProdukt,
       'model': model,
       }
    c.update(csrf(request))
    return render_to_response('createProdukt.html', c)



def create_Faden(request):
    
    model = get_model_name(FadenForm)
   
    if request.POST:
        formProdukt = FadenForm(request.POST)
        if formProdukt.is_valid():
            formProdukt.save()
            return HttpResponseRedirect('/lager/overview')
    else:
        formProdukt = FadenForm
   
    c={
       'formProdukt': formProdukt,
       'model': model,
       }
    c.update(csrf(request))
    return render_to_response('createProdukt.html', c)

def create_Lieferant_with_account (request):
    errorsLieferant=""
    errorsKonto=""
    if request.POST:
        formLieferant = LieferantForm(request.POST)
        formKonto = KontoForm(request.POST)
        if formLieferant.is_valid() and formKonto.is_valid():
            konto= formKonto.save()
            lieferant = formLieferant.save(commit=False)
            lieferant.konto_id = konto
            formLieferant.save()
            
            return HttpResponseRedirect('/lager/overview')
        else:
            errorsKonto = formKonto.errors
            errorsLieferant=formLieferant.errors
    else:
        formLieferant = LieferantForm
        formKonto = KontoForm
    c={
       'form' : formLieferant,
       'formKonto': formKonto,
       'errorsLieferant': errorsLieferant,
       'errorsKonto': errorsKonto,
       }
    
    c.update(csrf(request))
    return render_to_response('createLieferant.html', c) 

def create_Lieferant_without_account (request):
    errors=""
    if request.POST:
        formLieferant = LieferantForm(request.POST)
        if formLieferant.is_valid():
            formLieferant.save()
            
            return HttpResponseRedirect('/lager/overview')
        else:
            errors=formLieferant.errors
    else:
        formLieferant = LieferantForm
    c={
       'form' : formLieferant,
       'errorsLieferant': errors,
       }
    
    c.update(csrf(request))
    return render_to_response('createLieferant.html', c)

def show_overview_lieferant (request):
    lieferanten = Lieferant.objects.all()
    l={}
    for lieferant in lieferanten:
        l[lieferant.lieferanten_id]=LieferantForm(data=model_to_dict(lieferant))
    
    c={
       'lieferanten': l,
       }
    return render_to_response('overviewLieferant.html',c)    

def show_details_lieferant(request, lieferanten_id):
    lieferant = Lieferant.objects.get(lieferanten_id=lieferanten_id)
    errors=""
    if request.POST:
        form = LieferantForm(request.POST, instance=lieferant)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/lager/Lieferant/overview')
        else:
            errors= form.errors
    else:
        form = LieferantForm(data=model_to_dict(lieferant))
    
    c={
       'lieferant': form,
       'errors': errors,
       'id': lieferanten_id,
       }
    c.update(csrf(request))
    return render_to_response('detailsLieferant.html',c)
    
def show_details_lieferant_with_account(request, lieferanten_id):
    lieferant = Lieferant.objects.get(lieferanten_id=lieferanten_id)
    konto = lieferant.konto_id
    errors=""
    errors_konto=""
    if request.POST:
        form = LieferantForm(request.POST, instance=lieferant)
        formKonto = KontoForm(request.POST, instance=konto)
        
        if form.is_valid() and formKonto.is_valid():
            form.save()
            formKonto.save()
            
            return HttpResponseRedirect('/lager/Lieferant/overview')
        else:
            errors= form.errors
            errors_konto=formKonto.errors
    else:
        form = LieferantForm(data=model_to_dict(lieferant))
        formKonto = KontoForm(data=model_to_dict(konto))
    
    c={
       'lieferant': form,
       'konto': formKonto,
       'errors': errors,
       'errors_konto': errors_konto,
       'id': lieferanten_id,
       }
    c.update(csrf(request))
    return render_to_response('detailsLieferant.html',c)

def get_overview (request):
    
    produkte={}
    
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        produkte[model]={}
        
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        produkte[model][produkt.fabrikats_id] = ProduktOverviewForm(data=model_to_dict(produkt))
    
    c={
       'produkte': produkte
              }
    c.update(csrf(request))
    
    return render_to_response('overviewProdukte.html', c)

def get_overview_filter (request):
    if request.POST:
        formfilter= FilterForm(request.POST)
        if formfilter.is_valid:
            #adaptFilter
            return HttpResponseRedirect('/lager/overview')
        
    else:
        formfilter = FilterForm

    produkte={}

    
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        produkte[model]={}
        
    for produkt in Produkt.objects.all().select_subclasses():
        model = produkt.to_class_name()
        produkte[model][produkt.fabrikats_id] = ProduktOverviewForm(data=model_to_dict(produkt))
    
    c={
       'produkte': produkte,
       'filter': formfilter,
       }
    c.update(csrf(request))
    
    return render_to_response('overviewProdukte.html', c)


def details (request, model, fabrikats_id):
    mymodel = get_model('lager', model)
    produkt = mymodel.objects.get(fabrikats_id=fabrikats_id)
    errors=""

    if model == 'Lautsprecher':
        form = LautsprecherForm
    if model== 'Faden':
        form = FadenForm
    
    if request.POST:
        formProdukt = form(request.POST, instance=produkt)
        if formProdukt.is_valid():
            formProdukt.save()
            return HttpResponseRedirect ('/lager/overview')
        else:
            errors = formProdukt.errors

    produkt = form(data=model_to_dict(produkt))
    
    c={'produkt':produkt,
       'model': model,
       'id': fabrikats_id,
       'errors': errors,
       }
    c.update(csrf(request))
    return render_to_response('detailsProdukt.html', c)

def inventur_overview (request):
    inventuren = Inventur.objects.all()
    
    c={
       'inventuren': inventuren
       }
    
    return render_to_response('overviewInventur.html', c)
'''
def generate_inventurliste(request):

    products = request.GET.getlist('products[]')
    produkte=[]
    for produkt in products:
        produkte.append(Produkt.objects.get_subclass(fabrikats_id=produkt))
    print produkte
    
    return show_inventurliste(request, products)
'''
def show_inventurliste (request, product_id=None):
    produkte=[]
    if product_id is not None:
        p = product_id.split('/')
        for produkt in p:
            produkte.append(Produkt.objects.get_subclass(fabrikats_id=p))
    else:
        produkte=Produkt.objects.all().select_subclasses()
            
    errors=""
    InventurFormset = formset_factory(InventurForm, min_num=len(produkte))
    
    if request.POST:
        inventur_formset = InventurFormset(request.POST, request.FILES)
        if inventur_formset.is_valid():
            inventur = Inventur()
            inventur.save()
            for form in inventur_formset:
                position = form.save()
                inventur.position.add(position)
                produkt = Produkt.objects.filter(fabrikat=form.cleaned_data['produkt']).select_subclasses()[0]
                produkt.EK = form.cleaned_data['EK']
                produkt.save()
                
            inventur.save()
            
            return HttpResponseRedirect('/lager/inventur/overview')
        else:
            errors= inventur_formset.errors
    else:
        inventur_formset = InventurFormset 

    initial={
             'form-TOTAL_FORMS': len(produkte),
              'form-INITIAL_FORMS': len(produkte),
              'form-MAX_NUM_FORMS': len(produkte),
             }
    counter=0;
    for produkt in produkte:
        initial['form-'+str(counter)+'-produkt']= produkt.fabrikat
        initial['form-'+str(counter)+'-EK']= produkt.EK
        initial['form-'+str(counter)+'-gesamtwert']= produkt.EK
        counter+=1
        
    inventur_formset = InventurFormset(data=initial)
    
    c={
       'inventurFormset': inventur_formset,
       'errors': errors,
       }

    c.update(csrf(request))
    return render_to_response('inventurliste.html', c)

def inventur_ausdrucken(request, inventur_id):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def inventur_auswerten(request, inventur_id):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    