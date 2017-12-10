# -*- coding: utf-8 -*-
from django.db import models

class Configuration (models.Model):
    id = models.AutoField(primary_key=True)
    
    einkauf = models.BooleanField(default=False)
    bedarf = models.BooleanField(default=False)
    bestellung= models.BooleanField(default=False)
    lieferant_adresse = models.BooleanField(default=False)
    lieferant_strasse = models.BooleanField(default=False)
    lieferant_plz = models.BooleanField(default=False)
    lieferant_stadt = models.BooleanField(default=False)
    lieferant_mail = models.BooleanField(default=False)
    lieferant_tel = models.BooleanField(default=False)
    lieferant_homepage = models.BooleanField(default=False)
    lieferant_ustid = models.BooleanField(default=False)
    lieferant_mindestbestellwert = models.BooleanField(default=False)
    lieferant_konto = models.BooleanField(default=False)
    bestellung_intern= models.BooleanField(default=False)
    bestellung_extern= models.BooleanField(default=False)
    bestellung_lieferort = models.BooleanField(default=False)
    bestellung_lieferdatum = models.BooleanField(default=False)
    bestellung_auftragsbestaetigung = models.BooleanField(default=False)
    bestellung_lieferschein = models.BooleanField(default=False)
    bestellung_rechnung = models.BooleanField(default=False)
    bestellung_quittung = models.BooleanField(default=False)
    scanner = models.BooleanField(default=False)
    bezahlung = models.BooleanField(default=False)
    
    kauf = models.BooleanField(default=False)
    angebot = models.BooleanField(default=False)
    kaufabschluss = models.BooleanField (default=False)
    angebot_mwst = models.BooleanField(default=False)
    angebot_standort = models.BooleanField(default=False)
    angebot_datum = models.BooleanField(default=False)
    angebot_rabatt = models.BooleanField(default=False)
    angebot_rabattgrund = models.BooleanField(default=False)
    angebot_prozentrabatt = models.BooleanField(default=False)
    angebot_betragsrabatt = models.BooleanField(default=False)
    kauf_mwst = models.BooleanField(default=False)
    kauf_standort = models.BooleanField(default=False)
    kauf_datum = models.BooleanField(default=False)
    kauf_rabatt = models.BooleanField(default=False)
    kauf_rabattgrund = models.BooleanField(default=False)
    kauf_prozentrabatt = models.BooleanField(default=False)
    kauf_betragsrabatt = models.BooleanField(default=False)
    kreditwuerdig = models.BooleanField(default=False)
    angebotUmwandeln = models.BooleanField(default=False)
    nichtVoraetigeProdukte = models.BooleanField(default=False)
    scanner_kauf = models.BooleanField(default=False)
    zahlung = models.BooleanField(default=False)
    zahlart_raten = models.BooleanField(default=False)
    zahlart_kreditkarte = models.BooleanField(default=False)
    
    lager = models.BooleanField(default=False)
    produkttypen = models.ManyToManyField('Produkttyp', blank=True)
    lager_lieferant_adresse = models.BooleanField(default=False)
    lager_lieferant_strasse = models.BooleanField(default=False)
    lager_lieferant_plz = models.BooleanField(default=False)
    lager_lieferant_stadt = models.BooleanField(default=False)
    lager_lieferant_mail = models.BooleanField(default=False)
    lager_lieferant_tel = models.BooleanField(default=False)
    lager_lieferant_homepage = models.BooleanField(default=False)
    lager_lieferant_ustid = models.BooleanField(default=False)
    lager_lieferant_konto = models.BooleanField(default=False)
    filtern = models.BooleanField(default=False)
    filtern_fabrikat = models.BooleanField(default=False)
    filtern_seriennummer = models.BooleanField(default=False)
    filtern_kategorie = models.BooleanField(default=False)
    filtern_hersteller = models.BooleanField(default=False)
    filtern_lieferant = models.BooleanField(default=False)
    filtern_mwst_klasse = models.BooleanField(default=False)
    inventur = models.BooleanField(default=False)
    inventur_kategorie = models.BooleanField(default=False)
    inventur_durchschn_EK = models.BooleanField(default=False)
    inventur_letzter_EK = models.BooleanField(default=False)
    inventur_bemerkung = models.BooleanField(default=False)
    
    kunden = models.BooleanField(default=False)
    kunde_vorname = models.BooleanField(default=False)
    kunde_titel = models.BooleanField(default=False)
    kunde_tel = models.BooleanField(default=False)
    kunde_organisation = models.BooleanField(default=False)
    kunde_adresse = models.BooleanField(default=False)
    kunde_strasse = models.BooleanField(default=False)
    kunde_plz = models.BooleanField(default=False)
    kunde_stadt = models.BooleanField(default=False)
    kunde_mail = models.BooleanField(default=False)
    kunde_gruppe = models.BooleanField(default=False)
    kunde_privat = models.BooleanField(default=False)
    kunde_konto = models.BooleanField(default=False)
    kundengruppen = models.ManyToManyField('Kundengruppe', blank=True)
    kunde_filtern = models.BooleanField(default=False)
    kunde_filtern_nachname = models.BooleanField(default=False)
    kunde_filtern_organisation = models.BooleanField(default=False)
    kunde_filtern_plz = models.BooleanField(default=False)
    kunde_filtern_stadt = models.BooleanField(default=False)
    kunde_filtern_gruppe = models.BooleanField(default=False)
    kunde_filtern_privat = models.BooleanField(default=False)
    kunde_filtern_seriennummer = models.BooleanField(default=False)
    kunde_filtern_fabrikat = models.BooleanField(default=False)
    kunde_filtern_produktkategorie = models.BooleanField(default=False)
    kunde_filtern_preisspanne = models.BooleanField(default=False)
    kunde_fusionieren = models.BooleanField(default=False)
    kunde_exportieren = models.BooleanField(default=False)
    
    #Pluralbezeichnung
    class Meta:
        verbose_name_plural = "Konfigurationen"
     
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.id)

class Produkttyp (models.Model):
    produkttyp_id = models.AutoField(primary_key=True)
    produkttyp_name = models.CharField(max_length=50, blank=True)
    artikelnummer = models.BooleanField(default=False)
    produktkategorie = models.BooleanField(default=False)
    kategorien = models.ManyToManyField('Produktkategorie', blank=True)
    hersteller = models.BooleanField(default=False)
    beschreibung = models.BooleanField(default=False)
    lieferant = models.BooleanField(default=False)
    listenpreisVK = models.BooleanField(default=False)
    ausmasse = models.BooleanField(default=False)
    farben = models.BooleanField(default=False)
    mwst_klasse = models.BooleanField(default=False)
    durchschn_EK = models.BooleanField(default=False)
    letzter_EK = models.BooleanField(default=False)
    bemerkung = models.BooleanField(default=False)
    ean_nummer = models.BooleanField(default=False)

    
    #Pluralbezeichnung
    class Meta:
        verbose_name_plural = "Produkttypen"
     
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.produkttyp_name)
    
class Produktkategorie (models.Model):
    kategorie_id = models.AutoField(primary_key=True)
    kategorie= models.CharField(max_length=50)
    
    #Pluralbezeichnung
    class Meta:
        verbose_name_plural = "Produktkategorien"
     
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.kategorie)

class Kundengruppe (models.Model):
    kundengruppe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    #Pluralbezeichnung
    class Meta:
        verbose_name_plural = "Kundengruppen"
     
    #Objektbezeichnung    
    def __unicode__(self):
        return unicode(self.name)