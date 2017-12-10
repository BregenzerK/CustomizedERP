from django.contrib import admin
from einkauf.models import Bestellung, Bestellanforderung, Bestellposition

# Register your models here.
class BestellungenAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bestellung, BestellungenAdmin)

class BestellanforderungAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bestellanforderung, BestellanforderungAdmin)

class PositionAdmin (admin.ModelAdmin):
    pass

admin.site.register(Bestellposition, PositionAdmin)