
from django.contrib import admin

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from dashboard.resources import SaleResource
from sales.models import Sale, LastBlue, Service

class SaleInline(admin.StackedInline):
    model = Sale


class ServiceAdmin(ModelAdmin):
    inlines = [SaleInline,]
    extra= 0
admin.site.register(Service, ServiceAdmin)
    
    

class SaleAdmin(ModelAdmin, ImportExportModelAdmin):
    
    resource_class = SaleResource
   
admin.site.register(Sale, SaleAdmin)

admin.site.register(LastBlue)
