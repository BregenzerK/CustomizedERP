from django.contrib import admin
from lager.models import Lautsprecher, Faden, Lieferant, Inventurposition, Inventur,\
    Produkt
#from lager.forms import InventurForm

# Register your models here.
class LautsprecherAdmin (admin.ModelAdmin):
    pass

class FadenAdmin (admin.ModelAdmin):
    pass

class LieferantAdmin (admin.ModelAdmin):
    pass

class InventurpositionAdmin (admin.ModelAdmin):
    #form = InventurForm
    pass

class InventurAdmin (admin.ModelAdmin):
    pass

class ProduktAdmin(admin.ModelAdmin):
    pass

admin.site.register(Produkt, ProduktAdmin)
admin.site.register(Inventur, InventurAdmin)
admin.site.register(Inventurposition, InventurpositionAdmin)
admin.site.register(Lieferant, LieferantAdmin)
admin.site.register(Faden, FadenAdmin)
admin.site.register(Lautsprecher, LautsprecherAdmin)