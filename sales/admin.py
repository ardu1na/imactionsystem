
from django.contrib import admin



from sales.models import Sale, LastBlue, Service, Adj


class SaleAdmin(admin.ModelAdmin):
    list_display = ['service', 'client', 'change', 'note']
    search_fields = ['note',]
admin.site.register(Sale, SaleAdmin)

class SaleInline(admin.StackedInline):
    model = Sale
    extra = 0


class ServiceAdmin(admin.ModelAdmin):
    inlines = [SaleInline,]
    extra= 0
admin.site.register(Service, ServiceAdmin)
    
    

admin.site.register(LastBlue)
class AdjAdmin(admin.ModelAdmin):
    pass
admin.site.register(Adj, AdjAdmin)
