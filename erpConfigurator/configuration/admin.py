from django.contrib import admin
from models import Configuration, Produkttyp, Kundengruppe
from configuration.models import Produktkategorie

# Register your models here.
class ConfigurationAdmin (admin.ModelAdmin):
    pass

class ProdukttypAdmin (admin.ModelAdmin):
    pass

class KundengruppenAdmin (admin.ModelAdmin):
    pass

class ProduktkategorieAdmin (admin.ModelAdmin):
    pass

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Produkttyp, ProdukttypAdmin)
admin.site.register(Kundengruppe, KundengruppenAdmin)
admin.site.register(Produktkategorie, ProduktkategorieAdmin)