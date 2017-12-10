from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from configuration.forms import ConfigurationsForm, ProdukttypForm,\
    KundengruppeForm, ProduktkategorieForm
from django.http.response import HttpResponseRedirect
from django.forms.formsets import formset_factory
from configuration.models import Configuration
from subprocess import Popen, PIPE
import os
import shutil

def configuration(request):
    ProdukttypFormset = formset_factory(ProdukttypForm)
    KundengruppeFormset = formset_factory(KundengruppeForm)
    ProduktkategorieFormset = formset_factory(ProduktkategorieForm)
    if request.POST:
        form = ConfigurationsForm(request.POST)
        formsetProdukt = ProdukttypFormset(request.POST, request.FILES)
        formsetKunde = KundengruppeFormset(request.POST, request.FILES)
        formsetKategorie = ProduktkategorieFormset(request.POST, request.FILES)
        if form.is_valid() and formsetProdukt.is_valid() and formsetKunde.is_valid() and formsetKategorie.is_valid():
            
            c = form.save(commit=False)
            c.bedarf = form.cleaned_data['bedarf']
            c.bestellung = form.cleaned_data['bestellung']
            c.bestellung_intern = form.cleaned_data['bestellung_intern']
            c.bestellung_extern = form.cleaned_data['bestellung_extern']
            c.scanner = form.cleaned_data['scanner']
            c.bezahlung = form.cleaned_data['bezahlung']
            c.angebot = form.cleaned_data['angebot']
            c.kaufabschluss = form.cleaned_data['kaufabschluss']
            c.zahlung = form.cleaned_data['zahlung']
            c.filtern = form.cleaned_data['filtern']
            c.inventur = form.cleaned_data['inventur']
            c.kunde_filtern = form.cleaned_data['kunde_filtern']
            form.save()
            produktkategorien = []
            for k in formsetKategorie: 
                    kategorie = k.save()
                    if len(kategorie.kategorie)>0:               
                        produktkategorien.append(kategorie)
                    else:
                        kategorie.delete()
            
            for p in formsetProdukt:
                produkt = p.save()
                if len(produkt.produkttyp_name)>0:
                    produkt.produkttyp_name = produkt.produkttyp_name.replace(" ", "_")
                    c.produkttypen.add(produkt)
                    if len(produktkategorien)>0:
                        produkt.kategorien.add(*produktkategorien)
                    produkt.save()
                else:
                    produkt.delete()
    
            for g in formsetKunde:
                gruppe = g.save()
                if len(gruppe.name)>0:
                    c.kundengruppen.add(gruppe)
                else:
                    gruppe.delete()
            c.save()
            generate(c.id)
            return HttpResponseRedirect('/')
        else:
            print formsetProdukt.errors
    else:
        form = ConfigurationsForm()
        formsetProdukt = ProdukttypFormset()
        formsetKunde = KundengruppeFormset()
        formsetKategorie = ProduktkategorieFormset()
    
    
    c={'form':form,
       'formsetProdukt': formsetProdukt,
       'formsetKunde': formsetKunde,
       'formsetKategorie': formsetKategorie,
      }
    c.update(csrf(request))
    return render_to_response('configurator.html', c)

def read_file(path):
    output_decoded=[]
    with open(path, 'r') as file:
        output= file.readlines()
        for line in output: 
            output_decoded.append(line.decode('utf8'))
        return output_decoded
def write_file(path, input):
    input_encoded=[]
    with open(path, 'w') as file:
        for line in input: 
            input_encoded.append(line.encode('utf8'))
        file.write("".join(input_encoded))

def generate(confi):
    c = Configuration.objects.get(id=confi)
    
    #Generiere Django Projekt
    project = 'Customized_ERP_'+str(c.id)
    #os.chdir('D:\workspace')
    Popen(["django-admin", "startproject", "%s" % project ], stdout=PIPE).communicate()
    
    #Kopiere statische Dateien und Templates aus Core-Projekt
    #shutil.copytree('coreproject/static', str(project)+'/static')
    shutil.copytree('coreproject/templates', str(project)+'/templates')
    shutil.copyfile('coreproject/coreproject/views.py', str(project)+'/'+str(project)+'/views.py')
    
    os.chdir(str(project))
    apps = []
    url_links=["    url(r'^$', '"+str(project)+".views.home', name='home'), \n"]
    menu = ["<meta charset='utf-8' />"]

    if c.lager:
        #Generiere Django App "lager"
        app_lager = 'lager'
        apps.append(app_lager)
        Popen(["python", "manage.py", "startapp", "%s" % app_lager ], stdout=PIPE).communicate()
        shutil.copytree('../coreproject/'+str(app_lager)+'/templates', str(app_lager)+'/templates')
        
        #Lager ins Menue hinzufuegen
        menu_lager = read_file('../coreproject/schablonen/menu_lager_basic.html')
        
        lager_views_import=[]   
        
        #URL zur Produkt-Detailansicht 
        url_links.append("    url(r'^lager/(?P<model>[-\w]+)/(?P<fabrikats_id>[-\w]+)/Details$', 'lager.views.details'), \n")
        
        #Bearbeite Kopfzeilen lager.models, lager.views und lager.forms
        lager_models=read_file("../coreproject/"+str(app_lager)+"/schablonen/models.txt")
        lager_forms = read_file("../coreproject/"+str(app_lager)+"/schablonen/forms.txt")
        mwst_klassen=''
        choicesKategorie=''
        lieferant = False
        for produkttyp in c.produkttypen.all():
            lager_forms.append('from lager.models import '+produkttyp.produkttyp_name+' \n')
            lager_views_import.append('from lager.forms import '+produkttyp.produkttyp_name+'Form \n')
            url_links.append("    url(r'^lager/create/"+produkttyp.produkttyp_name+"', 'lager.views.create_"+produkttyp.produkttyp_name+"'), \n")            
            if produkttyp.produktkategorie:
                choicesKategorie = '('
                for kat in produkttyp.kategorien.all():
                    choicesKategorie += '("'+str(kat.kategorie)+'", "'+str(kat.kategorie)+'"),'
                choicesKategorie +=')'
            if produkttyp.mwst_klasse:
                mwst_klassen = '((19,"19 Prozent"),(7,"7 Prozent"))'  

        if len(choicesKategorie)>2:
            lager_models.append('PRODUKTKATEGORIEN='+choicesKategorie+' \n')
            if c.filtern_kategorie:
                lager_forms.append('from lager.models import PRODUKTKATEGORIEN \n')
        if len(mwst_klassen)>0:
            lager_models.append('MWST_KLASSEN='+mwst_klassen+' \n')
            if c.filtern_mwst_klasse:
                lager_forms.append('from lager.models import MWST_KLASSEN \n')

    
        #Arrays der Anpassungen views.py
        createMethod_produkte=[]
        detailsMethod_produkte=[]
        
        #bearbeite Felder lager.forms, lager.model und Methoden bei lager.views
        for produkttyp in c.produkttypen.all():
            forms_exclude="exclude=['lagerbestand', "  
            lager_models.append('class '+str(produkttyp.produkttyp_name)+' (Produkt): \n')
            if produkttyp.artikelnummer:
                lager_models.append('    artikelnummer = models.IntegerField(max_length=50) \n')
            if produkttyp.produktkategorie:
                lager_models.append('    produktkategorie = models.CharField(max_length=50, choices=PRODUKTKATEGORIEN) \n')
            if produkttyp.hersteller: 
                lager_models.append('    hersteller = models.CharField(max_length=50) \n')
            if produkttyp.beschreibung: 
                lager_models.append('    produktbeschreibung = models.TextField() \n')
            if produkttyp.lieferant: 
                lieferant = True
                lager_models.append('    lieferant = models.ForeignKey("Lieferant") \n')
            if produkttyp.listenpreisVK: 
                lager_models.append('    listenpreisVK = models.DecimalField(max_digits=8, decimal_places=2) \n')
            if produkttyp.ausmasse: 
                lager_models.append('    ausmasse = models.CharField(max_length=50) \n')
            if produkttyp.farben: 
                lager_models.append('    farben = models.CharField(max_length=50) \n')
            if produkttyp.mwst_klasse: 
                lager_models.append('    mwst_klasse = models.IntegerField(max_length=50, choices=MWST_KLASSEN) \n')
            if produkttyp.durchschn_EK: 
                lager_models.append('    durchschn_EK= models.DecimalField(max_digits=10, decimal_places=2, default=0.00) \n')
                forms_exclude+= "'durchschn_EK', "
            if produkttyp.letzter_EK: 
                lager_models.append('    letzter_EK = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) \n')
                forms_exclude+= "'letzter_EK', "
            if produkttyp.bemerkung: 
                lager_models.append('    bemerkung = models.TextField(blank=True) \n')
            if produkttyp.ean_nummer:
                lager_models.append('    ean_nummer = models.IntegerField(max_length=50) \n')
            if c.bedarf:
                lager_models.append('    meldebestand = models.IntegerField(max_length=5) \n')
            lager_models.append('    def to_class_name(self): \n')
            lager_models.append('        return self.__class__.__name__ \n')
            
            lager_models.append('class Instanzen_'+str(produkttyp.produkttyp_name)+' (models.Model): \n')
            lager_models.append('    id = models.AutoField(primary_key=True) \n')
            lager_models.append('    seriennummer= models.IntegerField(unique=True) \n')
            lager_models.append('    fabrikat= models.ForeignKey("'+str(produkttyp.produkttyp_name)+'") \n')
            lager_models.append('    verkauft= models.BooleanField(default=False) \n')
            lager_models.append('    standort= models.CharField(max_length=50) \n')
            
            #lager.forms
            lager_forms.append('class '+str(produkttyp.produkttyp_name)+'Form (forms.ModelForm): \n')
            lager_forms.append('    class Meta: \n')
            lager_forms.append('        model= '+str(produkttyp.produkttyp_name)+' \n')
            lager_forms.append("        "+forms_exclude+"] \n")
                
            menu_lager.append('<a class="item" href="/lager/create/'+produkttyp.produkttyp_name+'">'+produkttyp.produkttyp_name+'</a> \n')
                
            #views.py create_PRODUKT
            createMethod = read_file("../coreproject/"+str(app_lager)+"/schablonen/create_Produkt.txt")
                    
            for line in createMethod:
                if "PRODUKT" in line:
                    createMethod_produkte.append(line.replace('PRODUKT', str(produkttyp.produkttyp_name)))
                else:
                    createMethod_produkte.append(line)
            
            #views.py details 
            detailsMethod = read_file("../coreproject/"+str(app_lager)+"/schablonen/details.txt")   
            
            for line in detailsMethod:
                if "PRODUKT" in line:
                    detailsMethod_produkte.append(line.replace('PRODUKT', str(produkttyp.produkttyp_name)))
                        
        lieferanten_methoden=""
        if c.bedarf or c.bestellung or lieferant:
            lager_forms.append('from lager.models import Lieferant \n')
            lager_forms.append('class LieferantForm (forms.ModelForm): \n')
            lager_forms.append('    class Meta: \n')
            lager_forms.append('        model=Lieferant \n')
            lager_forms.append("        exclude=['konto_id'] \n")
            lager_views_import.append('from lager.models import Lieferant \n')
            lager_views_import.append('from lager.forms import LieferantForm \n')
            lager_models.append('class Lieferant (models.Model): \n')
            lager_models.append('    lieferanten_id = models.AutoField(primary_key=True) \n')
            lager_models.append('    firmenname = models.CharField(max_length=50) \n')
            lager_models.append('    ansprechpartner = models.CharField(max_length=50) \n')
            if c.lieferant_strasse or c.lager_lieferant_strasse:
                lager_models.append('    strasse = models.CharField(max_length=50) \n')
            if c.lieferant_plz or c.lager_lieferant_plz:
                lager_models.append('    PLZ = models.CharField(max_length=5) \n')
            if c.lieferant_stadt or c.lager_lieferant_stadt:
                lager_models.append('    stadt = models.CharField(max_length=50) \n')
            if c.lieferant_mail or c.lager_lieferant_mail:
                lager_models.append('    email = models.EmailField(max_length=75) \n')
            if c.lieferant_tel or c.lager_lieferant_tel:
                lager_models.append('    telefon = models.CharField(max_length=50) \n')
            if c.lieferant_homepage or c.lager_lieferant_homepage:
                lager_models.append('    homepage = models.URLField(max_length=200) \n')
            if c.lieferant_ustid or c.lager_lieferant_ustid: 
                lager_models.append('    ust_id = models.CharField(max_length=50) \n')
            if c.lieferant_mindestbestellwert:
                lager_models.append('    mindestbestellwert = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) \n')
            if c.kunde_konto and c.lieferant_konto or c.lager_lieferant_konto:
                lager_models.append('    konto_id = models.ForeignKey("kunden.Konto") \n')
                lieferanten_methoden="lieferant_with_account.txt"
                url_links.append("    url(r'^lager/Lieferant/(?P<lieferanten_id>[-\w]+)/Details', 'lager.views.show_details_lieferant_with_account'), \n")
                url_links.append("    url(r'^lager/create/Lieferant', 'lager.views.create_Lieferant_with_account'), \n")
                url_links.append("    url(r'^lager/Lieferant/overview', 'lager.views.show_overview_lieferant'), \n")
                lager_views_import.append('from kunden.forms import KontoForm \n')
                    
            if c.kunde_konto==False and c.lieferant_konto or c.lager_lieferant_konto:
                url_links.append("    url(r'^lager/Lieferant/(?P<lieferanten_id>[-\w]+)/Details', 'lager.views.show_details_lieferant_with_account'), \n")
                url_links.append("    url(r'^lager/create/Lieferant', 'lager.views.create_Lieferant_with_account'), \n")
                url_links.append("    url(r'^lager/Lieferant/overview', 'lager.views.show_overview_lieferant'), \n")
                lieferanten_methoden="lieferant_with_account.txt"
                lager_views_import.append('from lager.forms import KontoForm \n')
                lager_models.append('    konto_id = models.ForeignKey("Konto") \n')
                lager_models.append('class Konto (models.Model): \n')
                lager_models.append('    konto_id = models.AutoField(primary_key=True) \n')
                lager_models.append('    IBAN = models.PositiveIntegerField(max_length=34) \n')
                lager_models.append('    kontoinhaber = models.CharField(max_length=50) \n')
                lager_models.append('    BLZ = models.PositiveIntegerField(max_length=30) \n')
            
            if c.kunde_konto==False and c.lieferant_konto==False and c.lager_lieferant_konto==False:
                lieferanten_methoden="lieferant_without_account.txt"
                url_links.append("    url(r'^lager/Lieferant/(?P<lieferanten_id>[-\w]+)/Details', 'lager.views.show_details_lieferant_without_account'), \n")
                url_links.append("    url(r'^lager/create/Lieferant', 'lager.views.create_Lieferant_without_account'), \n")
                url_links.append("    url(r'^lager/Lieferant/overview', 'lager.views.show_overview_lieferant'), \n")
            
            lager_models.append('    def __unicode__(self): \n')
            lager_models.append('        return unicode(self.firmenname) \n')
            
            menu_lieferant = read_file("../coreproject/schablonen/menu_lager_lieferant.html")
            for line in menu_lieferant:
                menu_lager.append(line)
        else:
            write_file(str(app_lager)+'/templates/sidebar_createProdukt.html', "")        
          
        #bearbeiten lager.forms.py FilterForm
        if c.filtern:
            overview_method="get_overview_filter.txt"
            url_links.append("    url(r'^lager/overview', 'lager.views.get_overview_filter'), \n")
            lager_forms.append('class FilterForm (forms.Form): \n')
            lager_views_import.append('from lager.forms import FilterForm \n')
            if c.filtern_fabrikat:
                lager_forms.append('    fabrikat = forms.CharField(max_length=50) \n')
            if c.filtern_seriennummer:
                lager_forms.append('    seriennummer = forms.IntegerField () \n')
            if c.filtern_kategorie:
                lager_forms.append('    kategorie = forms.ChoiceField(choices=PRODUKTKATEGORIEN) \n')
            if c.filtern_hersteller:
                lager_forms.append('    hersteller = forms.CharField(max_length=50) \n')
            if c.filtern_lieferant:
                lager_forms.append('    lieferant = forms.ModelChoiceField(queryset=Lieferant.objects.all()) \n')
            if c.filtern_mwst_klasse:
                lager_forms.append('    mwst_klasse = forms.ChoiceField(choices=MWST_KLASSEN) \n')
        else:
            overview_method="get_overview.txt"
            url_links.append("    url(r'^lager/overview', 'lager.views.get_overview'), \n")
            write_file(str(app_lager)+'/templates/filterProdukte.html', "")
        
        inventur_methoden=""
        if c.inventur:
            lager_views_import.append('from lager.forms import InventurForm \n')
            lager_views_import.append('from lager.models import Inventur \n')
            lager_forms.append('from lager.models import Inventurposition \n')
            lager_models.append('class Inventur (models.Model): \n')
            lager_models.append('    inventur_id = models.AutoField(primary_key=True) \n')
            lager_models.append('    datum = models.DateField(auto_now=False, auto_now_add=True) \n')
            lager_models.append('    position = models.ForeignKey("Inventurposition", blank=True) \n')
            
            lager_models.append('class Inventurposition (models.Model): \n')
            lager_models.append('    inventurposition_id = models.AutoField(primary_key=True) \n')
            lager_models.append('    produkt =  models.CharField(max_length=50) \n')
            lager_models.append('    lagerbestand_real = models.IntegerField(max_length=50) \n')
            lager_models.append('    gesamtwert = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) \n')
            
            lager_forms.append('class InventurForm (forms.ModelForm): \n')
            lager_forms.append('    EK = forms.DecimalField(max_digits=8, decimal_places=2, label="Einkaufspreis") \n')
            lager_forms.append('    class Meta: \n')
            lager_forms.append('        model=Inventurposition \n')
            lager_forms.append("        fields =['produkt', 'lagerbestand_real', 'EK', 'gesamtwert'] \n")
            lager_forms.append("        widgets={ \n")
            lager_forms.append("            'produkt': forms.TextInput(attrs={'readonly':'readonly'}), \n")
            lager_forms.append("            'gesamtwert': forms.TextInput(attrs={'readonly':'readonly'}), \n")
            lager_forms.append('        } \n')
            
            inventur_methoden=read_file("../coreproject/"+str(app_lager)+"/schablonen/inventur.txt")
            
            url_links.append("    url(r'^lager/inventurliste', 'lager.views.show_inventurliste'), \n")
            url_links.append("    url(r'^lager/inventur/(?P<inventur_id>[-\w]+)/auswerten', 'lager.views.inventur_auswerten'), \n")
            url_links.append("    url(r'^lager/inventur/(?P<inventur_id>[-\w]+)/drucken', 'lager.views.inventur_ausdrucken'), \n")
            url_links.append("    url(r'^lager/inventur/overview', 'lager.views.inventur_overview'), \n")
                        
            menu_inventur = read_file("../coreproject/schablonen/menu_lager_inventur.html")
            for line in menu_inventur:
                menu_lager.append(line)
        else:
            write_file(str(app_lager)+'/templates/sidebar_overviewProdukte.html', "")
        
        overview_method = read_file("../coreproject/"+str(app_lager)+"/schablonen/"+overview_method)
        if len(lieferanten_methoden)>0:
            lieferanten_methoden= read_file("../coreproject/"+str(app_lager)+"/schablonen/"+lieferanten_methoden)        
        
        #Schreibvorgang models.py
        write_file(str(app_lager)+"/models.py", lager_models)
        
        #Schreibvorgang forms.py
        write_file(str(app_lager)+"/forms.py", lager_forms)
        
        #view.py anpassen
        lager_views_schablone = read_file("../coreproject/"+str(app_lager)+"/schablonen/views.txt")
        lager_views=[]           
        for line in lager_views_schablone:
            if "IMPORTS" in line:
                for l in lager_views_import:
                    lager_views.append(l)
            if "CREATE METHODS" in line:
                for l in createMethod_produkte:
                    lager_views.append(l)
            if "OVERVIEW METHOD" in line:
                for l in overview_method:
                    lager_views.append(l)
            if "DETAIL PRODUKTE" in line:
                for l in detailsMethod_produkte:
                    lager_views.append(l)
            if "LIEFERANT METHODS" in line:
                for l in lieferanten_methoden:
                    lager_views.append(l)
            if "INVENTUR METHODS" in line:
                if len(inventur_methoden)>0:
                    for l in inventur_methoden:
                        lager_views.append(l)
            else:
                lager_views.append(line)
        #Schreibvorgang views.py
        write_file(str(app_lager)+"/views.py", lager_views)
        
        menu_lager.append('</div></div> \n')

    if c.kunden:
        #Generiere Django App "kunden"
        app_kunden = 'kunden'
        apps.append(app_kunden)
        Popen(["python", "manage.py", "startapp", "%s" % app_kunden ], stdout=PIPE).communicate()
        shutil.copytree('../coreproject/'+str(app_kunden)+'/templates', str(app_kunden)+'/templates')
        
        #Kunden ins Menue hinzufuegen
        menu_kunden = read_file('../coreproject/schablonen/menu_kunden_basic.html')
           
        #Variablen view Methode
        views_Kunde_new=[]
             
        #bearbeite kunden.models
        kunden_models=['from django.db import models \n']
        if c.kunde_gruppe:
            choicesGruppe = '('
            for gruppe in c.kundengruppen.all():
                if len(gruppe.name)>0:
                    choicesGruppe += '("'+str(gruppe.name)+'", "'+str(gruppe.name)+'"),'
            choicesGruppe +=')'
            if len(choicesGruppe)>2:
                kunden_models.append('KATEGORIEN ='+choicesGruppe+' \n')                      
        kunden_models.append('class Kunde (models.Model): \n')
        kunden_models.append('    kunden_id = models.AutoField (primary_key = True) \n')
        kunden_models.append('    nachname = models.CharField(max_length=50) \n')
        if c.kunde_vorname:
            kunden_models.append('    vorname = models.CharField(max_length=50) \n')
        if c.kunde_titel:
            kunden_models.append('    titel = models.CharField(max_length=50, blank=True) \n')
        if c.kunde_tel:
            kunden_models.append('    telefonnummer = models.CharField(max_length=50) \n')
        if c.kunde_organisation:
            kunden_models.append('    organisation = models.CharField(max_length=50, blank=True) \n')
        if c.kunde_strasse:
            kunden_models.append('    strasse = models.CharField(max_length=50) \n')
        if c.kunde_plz:
            kunden_models.append('    PLZ = models.CharField(max_length=50) \n')
        if c.kunde_stadt:
            kunden_models.append('    stadt = models.CharField(max_length=50) \n')
        if c.kunde_mail:
            kunden_models.append('    email = models.EmailField(max_length=75) \n')
        if c.kunde_gruppe:
            kunden_models.append('    kundengruppe = models.CharField(max_length=50, choices=KATEGORIEN) \n')
        if c.kunde_privat:
            kunden_models.append('    privatkunde = models.BooleanField(default=True) \n') 
        if c.kreditwuerdig:
            kunden_models.append('    kreditwuerdig = models.BooleanField(default=False) \n')
        if c.kunde_konto:
            kunden_models.append('    konto_id = models.ForeignKey("Konto") \n')
            
            kunden_models.append('class Konto (models.Model): \n')
            kunden_models.append('    konto_id = models.AutoField(primary_key=True) \n')
            kunden_models.append('    IBAN = models.IntegerField(max_length=34) \n')
            kunden_models.append('    kontoinhaber = models.CharField(max_length=50) \n')
            kunden_models.append('    BLZ = models.IntegerField(max_length=30) \n')
            
            views_Kunde_new.append('from kunden.forms import KontoForm \n')
            
            url_links.append("    url(r'^kunden/create', 'kunden.views.create_with_account'), \n")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Details', 'kunden.views.details_with_account'), \n")
        else:
            url_links.append("    url(r'^kunden/create', 'kunden.views.create_without_account'), \n")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Details', 'kunden.views.details_without_account'), \n")
            
        write_file(str(app_kunden)+"/models.py", kunden_models)
            
        #Bearbeite kunden.forms
        kunden_forms = ['from django import forms \n']
        if c.kunde_konto:
            kunden_forms.append('from kunden.models import Konto \n')
        if c.kunde_filtern:
            if c.kunde_gruppe:
                kunden_forms.append('from kunden.models import KATEGORIEN \n')
            if c.kunde_filtern_produktkategorie:
                kunden_forms.append('from lager.models import PRODUKTKATEGORIEN \n')
            if c.kunde_filtern_fabrikat:
                kunden_forms.append('from lager.models import Produkt \n')
            
            views_Kunde_new.append('from kunden.forms import FilterForm \n')
            url_links.append("    url(r'^kunden/overview', 'kunden.views.get_overview_filter'), \n")
        else:
            url_links.append("    url(r'^kunden/overview', 'kunden.views.get_overview'), \n")
            write_file(str(app_kunden+'/templates/filterKunde.html'), "")
            
        kunden_forms.append('from kunden.models import Kunde \n')
        kunden_forms.append('class KundenForm (forms.ModelForm): \n')
        kunden_forms.append('    class Meta: \n')
        kunden_forms.append('        model= Kunde \n')
        if c.kunde_konto and c.kreditwuerdig:
            kunden_forms.append('        exclude = ["konto_id", "kreditwuerdig"] \n')
        elif c.kunde_konto and c.kreditwuerdig==False:
            kunden_forms.append('        exclude = ["konto_id"] \n')
        elif c.kunde_konto == False and c.kreditwuerdig:
            kunden_forms.append('        exclude = ["kreditwuerdig"] \n')
        else:
            kunden_forms.append('        fields = "__all__" \n')
        if c.kunde_konto:
            kunden_forms.append('class KontoForm (forms.ModelForm): \n')
            kunden_forms.append('    class Meta: \n')
            kunden_forms.append('        model= Konto \n')
            kunden_forms.append('        fields = "__all__" \n')
        if c.kunde_filtern:
            kunden_forms.append('class FilterForm (forms.Form): \n\n')
            if c.kunde_filtern_nachname:
                kunden_forms.append('    nachname = forms.CharField(max_length=50) \n')
            if c.kunde_filtern_organisation:
                kunden_forms.append('    organisation = forms.CharField(max_length=50) \n')
            if c.kunde_filtern_plz:
                kunden_forms.append('    plz = forms.CharField(max_length=50) \n')
            if c.kunde_filtern_stadt: 
                kunden_forms.append('    stadt = forms.CharField(max_length=50) \n')
            if c.kunde_filtern_gruppe:
                kunden_forms.append('    kundengruppe = forms.ChoiceField(choices= KATEGORIEN) \n')
            if c.kunde_filtern_privat:
                kunden_forms.append('    privatkunde = forms.BooleanField() \n')
            if c.kunde_filtern_seriennummer:
                kunden_forms.append('    seriennummer = forms.IntegerField () \n')
            if c.kunde_filtern_fabrikat:
                kunden_forms.append('    fabrikat = forms.ModelChoiceField(queryset=Produkt.objects.all().select_subclasses()) \n')
            if c.kunde_filtern_produktkategorie:
                kunden_forms.append('    kategorie = forms.ChoiceField(choices=PRODUKTKATEGORIEN) \n')
            if c.kunde_filtern_preisspanne:
                kunden_forms.append('    kauf_von = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0, label="Kauf von") \n')
                kunden_forms.append('    kauf_bis = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0, label="bis") \n')
        
        write_file(str(app_kunden)+"/forms.py", kunden_forms)
            
        #views anpassen
        if c.kunde_konto:
            createKunde="create_with_account.txt"
            detailKunde="details_with_account.txt"
        else:
            createKunde="create_without_account.txt"
            detailKunde="details.txt"
        
        if c.kunde_filtern:
            overviewKunde="get_overview_filter.txt"
        else:
            overviewKunde="get_overview.txt"
            
        createMethod_Kunde = read_file('../coreproject/'+str(app_kunden)+'/schablonen/'+createKunde)
        detailMethod_Kunde= read_file('../coreproject/'+str(app_kunden)+'/schablonen/'+detailKunde)    
        overviewMethod_Kunde = read_file('../coreproject/'+str(app_kunden)+'/schablonen/'+overviewKunde)
        
        views_Kunde = read_file('../coreproject/'+str(app_kunden)+'/schablonen/views.txt')
        
        
        for line in views_Kunde:
            if "OVERVIEW" in line:
                for l in overviewMethod_Kunde:
                    views_Kunde_new.append(l)
            if "CREATE" in line:
                for l in createMethod_Kunde:
                    views_Kunde_new.append(l)
            if "DETAILS" in line:
                for l in detailMethod_Kunde:
                    views_Kunde_new.append(l)
            else:
                views_Kunde_new.append(line)
        
        write_file(str(app_kunden)+"/views.py", views_Kunde_new)
            
        #Methoden in Sidebar und urls integrieren
        sidebar_overviewKunde = ['<meta charset="utf-8" /> \n']
        if c.kunde_fusionieren:
            sidebar_overviewKunde.append('<a class="item" href="/kunden/merge">fusionieren</a> \n')
            url_links.append("    url(r'^kunden/merge', 'kunden.views.merge'), \n")
        if c.kunde_exportieren:
            sidebar_overviewKunde.append('<a class="item" href="/kunden/export">exportieren</a> \n')
            url_links.append("    url(r'^kunden/export', 'kunden.views.export'), \n")
        
        write_file(str(app_kunden)+"/templates/sidebar_overviewKunde.html", sidebar_overviewKunde)
        
        #Methoden Sidebar detailsKunde
        if c.kauf==False:
            write_file(str(app_kunden)+"/templates/sidebar_detailsKunde.html", "")
        
    
    if c.einkauf or c.lager:
        #Generiere Django App "einkauf"
        app_einkauf = 'einkauf'
        apps.append(app_einkauf)
        Popen(["python", "manage.py", "startapp", "%s" % app_einkauf ], stdout=PIPE).communicate()
        shutil.copytree('../coreproject/'+str(app_einkauf)+'/templates', str(app_einkauf)+'/templates')
        
        #Bearbeite einkauf.models
        einkauf_models =['from django.db import models \n']
        einkauf_models.append('from datetime import datetime \n')
        
        if c.bedarf:
            einkauf_models.append('class Bestellanforderung (models.Model): \n')
            einkauf_models.append('    banf_id = models.AutoField(primary_key=True) \n')
            einkauf_models.append('    fabrikat= models.CharField(max_length=50) \n')
            einkauf_models.append('    menge = models.IntegerField(max_length=5) \n')
            einkauf_models.append('    bestellt= models.BooleanField(default=False) \n')
            
        if c.bestellung:
            einkauf_models.append('class Bestellung (models.Model): \n')
            einkauf_models.append('    bestell_id = models.AutoField(primary_key=True) \n')
            einkauf_models.append('    bestellposition = models.ManyToManyField("Bestellposition") \n')
            einkauf_models.append('    summe = models.DecimalField(max_digits=10, decimal_places=2) \n')
            einkauf_models.append('    status_offen = models.BooleanField(default=True) \n')
            if c.bedarf:
                einkauf_models.append('    banf = models.ForeignKey("Bestellanforderung") \n')
            if c.bestellung_lieferort:
                einkauf_models.append('    lieferort = models.CharField(max_length=50) \n')
            if c.bestellung_lieferdatum:
                einkauf_models.append('    lieferdatum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) \n')
                
            einkauf_models.append('class Bestellposition (models.Model): \n')
            einkauf_models.append('    position_id = models.AutoField(primary_key=True) \n')
            einkauf_models.append('    fabrikat= models.CharField(max_length=50)  \n')
            einkauf_models.append('    menge = models.IntegerField(max_length=5) \n')
            einkauf_models.append('    erhalten = models.BooleanField(default=False) \n')
            einkauf_models.append('    def __unicode__(self): \n')
            einkauf_models.append("        return unicode(str(self.menge)+'X '+str(self.fabrikat)) \n")
            
        if c.bezahlung:
            einkauf_models.append('class ZahlungBestellung (models.Model): \n')
            einkauf_models.append('    zahlungs_id = models.AutoField(primary_key = True) \n')
            if c.kunde_konto:
                einkauf_models.append('    konto = models.ForeignKey("kunden.Konto") \n')
            else:
                einkauf_models.append('    konto = models.ForeignKey("lager.Konto") \n')
            einkauf_models.append('    bestellung = models.ForeignKey("Bestellung") \n')
            einkauf_models.append('    verwendungszweck = models.TextField() \n')
            einkauf_models.append('    datum = models.DateField(auto_now=False, auto_now_add=False) \n') 
        
        write_file(str(app_einkauf)+"/models.py", einkauf_models)
        
        #entscheide Sets: einkauf.views, menu, einkauf.forms und add urls
        if c.bedarf:
            menu_einkauf="menu_einkauf_banf.html"
            einkauf_methods = "banf.txt"
            einkauf_modelforms ="forms_banf.txt"
            url_links.append("    url(r'^einkauf/Bestellanforderung/overview', 'einkauf.views.show_banf_overview'), \n")
            url_links.append("    url(r'^einkauf/Bestellung/overview', 'einkauf.views.show_bestellung_overview'), \n")
            url_links.append("    url(r'^einkauf/create/Bestellung/(?P<lieferanten_id>[-\w]+)', 'einkauf.views.create_bestellung'), \n")
            url_links.append("    url(r'^einkauf/Bestellanforderung/(?P<banf_id>[-\w]+)/(?P<mitteilung_id>[-\w]+)', 'einkauf.views.show_banf_details'), \n")
            url_links.append("    url(r'^einkauf/Bestellanforderung/(?P<banf_id>[-\w]+)', 'einkauf.views.show_banf_details'), \n")
            url_links.append("    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/close', 'einkauf.views.close_bestellung'), \n")
            url_links.append("    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/Details', 'einkauf.views.show_details_bestellung'), \n")
        if c.bedarf==False and c.bestellung:
            menu_einkauf="menu_einkauf_bestellung.html"
            einkauf_methods="bestellung.txt"
            einkauf_modelforms="forms_bestellung.txt"
            url_links.append("    url(r'^einkauf/Bestellung/overview', 'einkauf.views.show_bestellung_overview'), \n")
            url_links.append("    url(r'^einkauf/create/Bestellung', 'einkauf.views.create_bestellung_without_banf'), \n")
            url_links.append("    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/close', 'einkauf.views.close_bestellung'), \n")
            url_links.append("    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/Details', 'einkauf.views.show_details_bestellung'), \n")
            url_links.append("    url(r'^Produkte', 'einkauf.views.get_produkte_zu_lieferant'), \n")
        if c.bedarf==False and c.bestellung==False and c.lager:
            einkauf_modelforms=""
            menu_einkauf="menu_einkauf_wareneingang.html"
            einkauf_methods="wareneingang.txt"
            url_links.append("    url(r'^einkauf/create/Wareneingang', 'einkauf.views.create_wareneingang'), \n")
            url_links.append("    url(r'^Produkte', 'einkauf.views.get_produkte_zu_lieferant'), \n") 
            
        menu_einkauf = read_file('../coreproject/schablonen/'+menu_einkauf)
        
        #bearbeitet einkauf.views
        einkauf_methods = read_file('../coreproject/'+str(app_einkauf)+'/schablonen/'+einkauf_methods)
        einkauf_views_new=[]
        if c.nichtVoraetigeProdukte:
            einkauf_methods_expanded=[]
            einkauf_views_new.append('from kauf.models import Kauf \n')
            einkauf_views_new.append('from mitteilungen.models import MitteilungKauf \n')
            einkauf_methods_nicht_vorraetig = read_file('../coreproject/'+str(app_einkauf)+'/schablonen/detailsBestellung_nicht_vorraetige_Produkte.txt')
            for line in einkauf_methods:
                if "NICHT VORRAETIGE PRODUKTE" in line:
                    for l in einkauf_methods_nicht_vorraetig:
                        einkauf_methods_expanded.append(l)
                        
                else: einkauf_methods_expanded.append(line)
            einkauf_methods = einkauf_methods_expanded
        
        
        einkauf_views = read_file('../coreproject/'+str(app_einkauf)+'/schablonen/views.txt')
        for line in einkauf_views:
            if "METHODS" in line:
                for l in einkauf_methods:
                    einkauf_views_new.append(l)
            else:
                einkauf_views_new.append(line)
        
        write_file(str(app_einkauf)+'/views.py', einkauf_views_new)
        
        #bearbeite einkauf.forms
        einkauf_forms = read_file('../coreproject/'+str(app_einkauf)+"/schablonen/forms.txt")
        if len(einkauf_modelforms)>0:
            einkauf_modelforms = read_file('../coreproject/'+str(app_einkauf)+"/schablonen/"+einkauf_modelforms)
            for line in einkauf_modelforms:
                einkauf_forms.append(line)
        write_file(str(app_einkauf)+'/forms.py', einkauf_forms)
            
        #bearbeite Optiom in Bestellung/Overview und /Details
        if c.bedarf or c.bestellung:
            bestellungOptions = read_file('../coreproject/'+str(app_einkauf)+"/schablonen/bestellungOptions.txt")
            sidebar_bestellung=['<meta charset="utf-8" /> \n']
            if c.scanner:
                sidebar_bestellung.append('<a class="item" href="/einkauf/Bestellung/{{id}}/scan">Produkte scannen</a> \n')
            if c.bestellung_extern:
                bestellungOptions.append('<div class="ui button"><a href="/einkauf/Bestellung/{{bestellung.bestell_id}}/download">Bestellung herunterladen</a></div> \n')
                sidebar_bestellung.append('<a class="item" href="/einkauf/Bestellung/{{id}}/download">Bestellung herunterladen</a> \n')
            if c.bestellung_auftragsbestaetigung or c.bestellung_lieferschein or c.bestellung_rechnung or c.bestellung_quittung: 
                bestellungOptions.append('<div class="ui button"><a href="/einkauf/Bestellung/{{bestellung.bestell_id}}/upload">Dokument hochladen</a></div> \n')
                sidebar_bestellung.append('<a class="item" href="/einkauf/Bestellung/{{id}}/upload">Dokument hochladen</a> \n')
            if c.bezahlung:
                bestellungOptions.append('<div class="ui button"><a href="/einkauf/Bestellung/{{bestellung.bestell_id}}/bezahlen">Rechnung bezahlen</a></div> \n')
                sidebar_bestellung.append('<a class="item" href="/einkauf/Bestellung/{{id}}/bezahlen">Rechnung bezahlen</a> \n')
            write_file(str(app_einkauf+'/templates/bestellungOptions.html'), bestellungOptions)
            write_file(str(app_einkauf+'/templates/sidebarBestellungDetails.html'), sidebar_bestellung)       
                
    if c.kauf:
        #Generiere Django App "kauf"
        app_kauf = 'kauf'
        apps.append(app_kauf)
        Popen(["python", "manage.py", "startapp", "%s" % app_kauf ], stdout=PIPE).communicate()
        shutil.copytree('../coreproject/'+str(app_kauf)+'/templates', str(app_kauf)+'/templates')
            
        #bearbeite kauf.models
        kauf_models = ['from django.db import models \n']
        kauf_models.append('from datetime import datetime \n')
        
        kauf_models.append('class Kauf (models.Model): \n')
        kauf_models.append('    kauf_id = models.AutoField (primary_key=True) \n')
        kauf_models.append('    kunde = models.ForeignKey("kunden.Kunde") \n')
        kauf_models.append('    warenposition = models.ManyToManyField("Warenposition") \n')
        kauf_models.append('    summe = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) \n')
        kauf_models.append('    abgeschlossen = models.BooleanField(default=False) \n')
        if c.kauf_mwst:
            kauf_models.append('    mehrwertsteuer = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) \n')
        if c.kauf_prozentrabatt or c.kauf_betragsrabatt:
            kauf_models.append('    rabatt = models.DecimalField(max_digits=10, decimal_places=2, default=0) \n')
            rabattarten="("
            if c.kauf_prozentrabatt:
                rabattarten += '("prozentrabatt", "%"),'
            if c.kauf_betragsrabatt:
                rabattarten += '("betragsrabatt", "EUR"),'
            rabattarten+= ")"
            kauf_models.append('    rabattarten = models.CharField(max_length=50, choices='+rabattarten+') \n')
        if c.kauf_rabattgrund:
            kauf_models.append('    rabattgrund = models.TextField(blank=True) \n')
        if c.kauf_standort:
            kauf_models.append('    standort = models.CharField(max_length=50) \n')
        if c.kauf_datum:
            kauf_models.append('    datum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) \n')
        
        if c.angebot:
            kauf_models.append('class Angebot (models.Model): \n')
            kauf_models.append('    angebot_id = models.AutoField (primary_key=True) \n')
            kauf_models.append('    kunde = models.ForeignKey("kunden.Kunde") \n')
            kauf_models.append('    warenposition = models.ManyToManyField("Warenposition") \n')
            kauf_models.append('    summe = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) \n')
            if c.angebot_mwst:
                kauf_models.append('    mehrwertsteuer = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) \n')
            if c.angebot_prozentrabatt or c.angebot_betragsrabatt:
                kauf_models.append('    rabatt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) \n')
                rabattarten="("
                if c.angebot_prozentrabatt:
                    rabattarten += '("prozentrabatt", "%"),'
                if c.angebot_betragsrabatt:
                    rabattarten += '("betragsrabatt", "EUR"),'
                rabattarten+= ")"
                kauf_models.append('    rabattarten = models.CharField(max_length=50, choices='+rabattarten+') \n')
            if c.angebot_rabattgrund:
                kauf_models.append('    rabattgrund = models.TextField() \n')
            if c.angebot_standort:
                kauf_models.append('    standort = models.CharField(max_length=50) \n')
            if c.angebot_datum:
                kauf_models.append('    datum = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()) \n')
        
        kauf_models.append('class Warenposition (models.Model): \n')
        kauf_models.append('    position_id = models.AutoField(primary_key=True) \n')
        kauf_models.append('    fabrikat= models.CharField(max_length=50) \n')
        kauf_models.append('    menge = models.IntegerField(max_length=5) \n')
        kauf_models.append('    available = models.BooleanField(default=True) \n')
        kauf_models.append('    def __unicode__(self): \n')
        kauf_models.append("        return unicode(str(self.menge)+'X '+str(self.fabrikat)) \n")
        
        if c.zahlung:
            kauf_models.append('class ZahlungKauf (models.Model): \n')
            kauf_models.append('    zahlungs_id = models.AutoField(primary_key = True) \n')
            kauf_models.append('    konto = models.ForeignKey ("kunden.Konto") \n')
            kauf_models.append('    kauf = models.ForeignKey("Kauf") \n')
            kauf_models.append('    verwendungszweck = models.TextField() \n')
            kauf_models.append('    datum = models.DateField(auto_now=False, auto_now_add=True) \n')
            zahlarten="("
            if c.zahlart_raten:
                zahlarten+= '("Raten", "Ratenzahlung"),'
            if c.zahlart_kreditkarte:
                zahlarten += '("Kreditkarte", "Kreditkarte"),'
            zahlarten+= ")"
            kauf_models.append('    zahlart = models.CharField(max_length=20, choices='+zahlarten+') \n')
            
        write_file(str(app_kauf)+"/models.py", kauf_models)
        
        #bearbeite kauf.forms und kauf.views und add urls
        kauf_forms = read_file("../coreproject/"+str(app_kauf)+"/schablonen/forms.txt")
        kauf_views = read_file("../coreproject/"+str(app_kauf)+"/schablonen/views.txt")
        kauf_views_offer=""
        kauf_views_history=""
        if c.angebot:
            kauf_forms.append("from kauf.models import Angebot \n")
            kauf_forms.append("class AngebotForm (forms.ModelForm): \n")
            kauf_forms.append("    class Meta: \n")
            kauf_forms.append("        model=Angebot \n")
            kauf_forms.append("        exclude=['warenposition', 'kunde'] \n")
            kauf_forms.append("        widgets={ \n")
            kauf_forms.append("            'summe': forms.TextInput(attrs={'readonly':'readonly', 'value': 0}), \n")
            kauf_forms.append("            'mehrwertsteuer': forms.TextInput(attrs={'readonly':'readonly', 'value':0}), \n")
            kauf_forms.append("        } \n")
            
            kauf_views_offer= read_file("../coreproject/"+str(app_kauf)+"/schablonen/create_offer.txt")
            kauf_views_history = read_file("../coreproject/"+str(app_kauf)+"/schablonen/show_orderhistory_with_offer.txt")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Angebot', 'kauf.views.create_offer'), \n")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/kaufhistorie', 'kauf.views.show_orderhistory_with_offer'), \n")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Angebot/(?P<angebot_id>[-\w]+)/download', 'kauf.views.download_offer'), \n")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Angebot/(?P<angebot_id>[-\w]+)', 'kauf.views.show_angebot_details'), \n")
        else:
            kauf_views_history = read_file("../coreproject/"+str(app_kauf)+"/schablonen/show_orderhistory_without_offer.txt")
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/kaufhistorie', 'kauf.views.show_orderhistory_without_offer'), \n")
        
        write_file(str(app_kauf)+"/forms.py", kauf_forms)
        
        kauf_views_neu=[]
        kauf_views_extended=[]
        vorraetig = False
        banf=False
        if c.nichtVoraetigeProdukte:
            vorraetig=True
            kauf_views_neu.append("from mitteilungen.views import message_read \n")
        if c.bedarf:
            kauf_views_neu.append("from einkauf.views import check_for_banf \n")
            banf=True    
            
            
        for line in kauf_views:
            if vorraetig and banf:
                if "MITTEILUNG" in line:
                    kauf_views_extended.append("    if mitteilung_id>0: \n")
                    kauf_views_extended.append("        message_read(request, mitteilung_id) \n")
                if "CHECK FOR BANF" in line:
                    kauf_views_extended.append("            for produkt in produkte: \n")
                    kauf_views_extended.append("                check_for_banf(produkt.fabrikats_id, kauf_id) \n")
                else:
                    kauf_views_extended.append(line)
            elif vorraetig and banf==False:
                if "MITTEILUNG" in line:
                    kauf_views_extended.append("    if mitteilung_id>0: \n")
                    kauf_views_extended.append("        message_read(request, mitteilung_id) \n")  
                else:
                    kauf_views_extended.append(line)
            elif banf and vorraetig==False:
                if "CHECK FOR BANF" in line:
                    kauf_views_extended.append("            for produkt in produkte: \n")
                    kauf_views_extended.append("                check_for_banf(produkt.fabrikats_id, kauf_id) \n")
                else:
                    kauf_views_extended.append(line)
            else:
                kauf_views_extended.append(line)
            
        
        for line in kauf_views_extended:
            if "ORDERHISTORY" in line:
                for l in kauf_views_history:
                    kauf_views_neu.append(l)
            if "CREATE OFFER" in line:
                if len(kauf_views_offer)>0:
                    for l in kauf_views_offer:
                        kauf_views_neu.append(l)
            else:
                kauf_views_neu.append(line)
        write_file(str(app_kauf)+"/views.py", kauf_views_neu)
        
        #Sidebar Kunde Details, Kaufhistorie und urls
        sidebar_detailsKunde=['<meta charset="utf-8" /> \n']
        sidebar_historie=['<meta charset="utf-8" /> \n']
        sidebar_detailsKunde.append('<a class="item" href="/kunden/{{id}}/kaufhistorie">Kaufhistorie</a> \n')
        sidebar_detailsKunde.append('<a class="item" href="/kunden/{{id}}/create/Kauf"><i class="add icon"></i> Kauf</a> \n')
        if c.angebot:
            sidebar_historie.append('<a class="item" href="/kunden/{{kunde.kunden_id}}/create/Angebot"><i class="add icon"></i> Angebot</a> \n')
            sidebar_detailsKunde.append('<a class="item" href="/kunden/{{id}}/create/Angebot"><i class="add icon"></i> Angebot</a> \n')
        if c.kreditwuerdig:
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/check_credit', 'kauf.views.check_credit'), \n")
            sidebar_historie.append('<a class="item" href="/kunden/{{id}}/check_credit">check creditworthiness</a> \n')
            sidebar_detailsKunde.append('<a class="item" href="/kunden/{{id}}/check_credit">check creditworthiness</a> \n')
        if c.angebotUmwandeln==False:
            write_file(str(app_kauf)+'/templates/options_kaufhistorie_angebote.html', "")
        else:
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf/(?P<angebot_id>[-\w]+)', 'kauf.views.create_purchase_from_offer'), \n")
        
        write_file(str(app_kunden)+'/templates/sidebar_detailsKunde.html', sidebar_detailsKunde)
        write_file(str(app_kauf)+'/templates/sidebar_kaufhistorie.html', sidebar_historie)
        
        #Sidebar Kauf
        sidebar_kauf=['<meta charset="utf-8" />']
        if c.scanner_kauf:
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf/scannen', 'kauf.views.scan_products'), \n")
            sidebar_kauf.append('<a class="item" href="/kunden/{{id}}/create/Kauf/scannen">Produkte scannen</a> \n')
        if c.zahlung:
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf/zahlung', 'kauf.views.check_payment'), \n")
            sidebar_kauf.append('<a class="item" href="/kunden/{{id}}/create/Kauf/zahlung">Zahlung verfolgen</a> \n')
        
        write_file(str(app_kauf)+'/templates/sidebar_createKauf.html', sidebar_kauf)
        
        #urls
        url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf', 'kauf.views.create_purchase'), \n")
        url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Kauf/(?P<kauf_id>[-\w]+)/download', 'kauf.views.download_purchase'), \n")
        if c.nichtVoraetigeProdukte:
            url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Kauf/(?P<kauf_id>[-\w]+)/(?P<mitteilung_id>[-\w]+)', 'kauf.views.show_kauf_details'), \n")
        url_links.append("    url(r'^kunden/(?P<kunden_id>[-\w]+)/Kauf/(?P<kauf_id>[-\w]+)', 'kauf.views.show_kauf_details'), \n")
        url_links.append("    url(r'^Preis', 'kauf.views.get_Preis'), \n")
        
    if c.bedarf or c.nichtVoraetigeProdukte or c.zahlung:
        #Generiere Django App "mitteilungen"
        app_mitteilungen = 'mitteilungen'
        apps.append(app_mitteilungen)
        Popen(["python", "manage.py", "startapp", "%s" % app_mitteilungen ], stdout=PIPE).communicate()
        shutil.copytree('../coreproject/'+str(app_mitteilungen)+'/templates', str(app_mitteilungen)+'/templates')
        shutil.copyfile('../coreproject/'+str(app_mitteilungen)+'/views.py', str(app_mitteilungen)+'/views.py')
        
        mitteilungen_models = read_file('../coreproject/'+str(app_mitteilungen)+'/schablonen/models.txt')
        
        if c.nichtVoraetigeProdukte or c.zahlung:
            mitteilungen_models.append('class MitteilungKauf (Mitteilung): \n')
            mitteilungen_models.append('    kauf = models.ForeignKey("kauf.Kauf") \n')
        if c.bedarf:
            mitteilungen_models.append('class MitteilungBanf (Mitteilung): \n')
            mitteilungen_models.append('    bestellanforderung = models.ForeignKey("einkauf.Bestellanforderung") \n')
        write_file(str(app_mitteilungen)+'/models.py', mitteilungen_models)
        
        url_links.append("    url(r'^Mitteilungsboard/(?P<mitteilung_id>[-\w]+)/gelesen', 'mitteilungen.views.message_read'), \n")
        url_links.append("    url(r'^Mitteilungsboard', 'mitteilungen.views.show_messages'), \n")
        url_links.append("    url(r'^Messages', 'mitteilungen.views.calc_messages'), \n")
        
        menu_mitteilungen = '<a class="item" href="/Mitteilungsboard">Mitteilungsboard<div id="messages_number" class="ui green label"></div></a> \n'
        
    #Anpassen menu.html
    if c.kunden:
        for line in menu_kunden:
            menu.append(line)
    if c.lager:
        for line in menu_lager:
            menu.append(line)
    if c.einkauf:
        for line in menu_einkauf:
            menu.append(line)
    if c.bedarf or c.nichtVoraetigeProdukte or c.zahlung:
        menu.append(menu_mitteilungen)
    write_file("templates/menu.html", menu)
    
            
    #Anpassungen setting.py
    os.chdir(str(project))
    settings = read_file("settings.py") 
    
    new_settings=[]
    
    for line in settings:
        if "INSTALLED_APPS" in line:
            new_settings.append(line)
            for app in apps:
                new_settings.append("    '"+str(app)+"', \n")
        else:
            new_settings.append(line)
    
    new_settings.append("STAICFILES_DIRS =( \n")
    new_settings.append("    'C:/customizedErp/static', )\n")
    
    new_settings.append("TEMPLATE_DIRS = ( \n")
    new_settings.append("    os.path.join(BASE_DIR, 'templates'), )\n")
        
    write_file("settings.py", new_settings) 
    
    #Anpassungen urls.py    
    urls = read_file("urls.py")
    
    new_urls=[]
    
    for line in urls:
        if "urlpatterns = patterns" in line:
            new_urls.append(line)
            for link in url_links:
                new_urls.append(str(link))
        else:
            new_urls.append(line)
            
    write_file("urls.py", new_urls)
    
    os.chdir('..')
    os.chdir('..') 