from django.contrib import admin
from kauf.models import Angebot, Warenposition, Kauf

# Register your models here.
class AngebotAdmin (admin.ModelAdmin):
    pass

admin.site.register(Angebot, AngebotAdmin)

class WarenpositionAdmin (admin.ModelAdmin):
    pass

admin.site.register(Warenposition, WarenpositionAdmin)

class KaufAdmin (admin.ModelAdmin):
    pass

admin.site.register(Kauf, KaufAdmin)
