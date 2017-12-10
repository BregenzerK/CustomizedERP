from django.contrib import admin
from kunden.models import Kunde, Konto

# Register your models here.
class KundenAdmin (admin.ModelAdmin):
    pass

class KontoAdmin (admin.ModelAdmin):
    pass

admin.site.register(Kunde, KundenAdmin)
admin.site.register(Konto, KontoAdmin)