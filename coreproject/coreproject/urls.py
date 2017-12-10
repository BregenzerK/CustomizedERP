from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'coreproject.views.home', name='home'),
    
    url(r'^kunden/create', 'kunden.views.create_with_account' ),
    url(r'^kunden/overview', 'kunden.views.get_overview_filter'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/Details', 'kunden.views.details_with_account'),
    url(r'^kunden/export', 'kunden.views.export'),
    url(r'^kunden/merge', 'kunden.views.merge'),
    
    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Angebot', 'kauf.views.create_offer'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf/(?P<angebot_id>[-\w]+)', 'kauf.views.create_purchase_from_offer'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf', 'kauf.views.create_purchase'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf/scannen', 'kauf.views.scan_products'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/create/Kauf/zahlung', 'kauf.views.check_payment'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/kaufhistorie', 'kauf.views.show_orderhistory_with_offer'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/Kauf/(?P<kauf_id>[-\w]+)/download', 'kauf.views.download_purchase'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/Angebot/(?P<angebot_id>[-\w]+)/download', 'kauf.views.download_offer'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/Kauf/(?P<kauf_id>[-\w]+)/(?P<mitteilung_id>[-\w]+)', 'kauf.views.show_kauf_details'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/Kauf/(?P<kauf_id>[-\w]+)', 'kauf.views.show_kauf_details'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/Angebot/(?P<angebot_id>[-\w]+)', 'kauf.views.show_angebot_details'),
    url(r'^Preis', 'kauf.views.get_Preis'),
    url(r'^kunden/(?P<kunden_id>[-\w]+)/check_credit', 'kauf.views.check_credit'),
    
    url(r'^lager/create/Lautsprecher', 'lager.views.create_Lautsprecher'),
    url(r'^lager/create/Faden', 'lager.views.create_Faden'),
    url(r'^lager/overview', 'lager.views.get_overview_filter'),
    url(r'^lager/Lieferant/(?P<lieferanten_id>[-\w]+)/Details', 'lager.views.show_details_lieferant_with_account'),
    url(r'^lager/(?P<model>[-\w]+)/(?P<fabrikats_id>[-\w]+)/Details$', 'lager.views.details'),
    #url(r'^lager/generateInventurliste', 'lager.views.generate_inventurliste'),
    url(r'^lager/inventurliste', 'lager.views.show_inventurliste'),
    url(r'^lager/inventurliste/(?P<product_id>.+)', 'lager.views.show_inventurliste'),
    url(r'^lager/inventur/(?P<inventur_id>[-\w]+)/auswerten', 'lager.views.inventur_auswerten'),
    url(r'^lager/inventur/(?P<inventur_id>[-\w]+)/drucken', 'lager.views.inventur_ausdrucken'),
    url(r'^lager/inventur/overview', 'lager.views.inventur_overview'),
    url(r'^lager/create/Lieferant', 'lager.views.create_Lieferant_with_account'),
    url(r'^lager/Lieferant/overview', 'lager.views.show_overview_lieferant'),
    
    url(r'^einkauf/Bestellanforderung/overview', 'einkauf.views.show_banf_overview'),
    url(r'^einkauf/Bestellung/overview', 'einkauf.views.show_bestellung_overview'),
    url(r'^einkauf/create/Bestellung/(?P<lieferanten_id>[-\w]+)', 'einkauf.views.create_bestellung'),
    url(r'^einkauf/create/Bestellung', 'einkauf.views.create_bestellung_without_banf'),
    url(r'^einkauf/create/Wareneingang', 'einkauf.views.create_wareneingang'),
    url(r'^einkauf/Bestellanforderung/(?P<banf_id>[-\w]+)/(?P<mitteilung_id>[-\w]+)', 'einkauf.views.show_banf_details'),
    url(r'^einkauf/Bestellanforderung/(?P<banf_id>[-\w]+)', 'einkauf.views.show_banf_details'),
    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/upload', 'einkauf.views.upload_document'),
    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/bezahlen', 'einkauf.views.pay_bestellung'),
    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/close', 'einkauf.views.close_bestellung'),
    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/download', 'einkauf.views.download_bestellung'),
    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/scan', 'einkauf.views.scan_products'),
    url(r'^einkauf/Bestellung/(?P<bestell_id>[-\w]+)/Details', 'einkauf.views.show_details_bestellung'),
    url(r'^Produkte', 'einkauf.views.get_produkte_zu_lieferant'),
        
    url(r'^Mitteilungsboard/(?P<mitteilung_id>[-\w]+)/gelesen', 'mitteilungen.views.message_read'),
    url(r'^Mitteilungsboard', 'mitteilungen.views.show_messages'),
    url(r'^Messages', 'mitteilungen.views.calc_messages'),


    url(r'^admin/', include(admin.site.urls)),
)
