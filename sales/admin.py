
from django.contrib import admin

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from dashboard.resources import SaleResource
from sales.models import Sale, LastBlue, Service, Adj



class SaleInline(admin.StackedInline):
    model = Sale
    extra = 0


class ServiceAdmin(ModelAdmin):
    inlines = [SaleInline,]
    extra= 0
admin.site.register(Service, ServiceAdmin)
    
    

class SaleAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['service', 'client', 'change', 'note']
    search_fields = ['note',]
    resource_class = SaleResource
   
admin.site.register(Sale, SaleAdmin)

admin.site.register(LastBlue)
class AdjAdmin(ModelAdmin):
    pass
admin.site.register(Adj, AdjAdmin)
