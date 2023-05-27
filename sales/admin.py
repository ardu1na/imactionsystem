
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin
from sales.models import Sale, LastBlue, Service, Adj

from dashboard.resources import *

class SaleAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['service', 'client', 'change', 'note']
    search_fields = ['note',]
    resource_class = SaleResource

admin.site.register(Sale, SaleAdmin)

class SaleInline(admin.StackedInline):
    model = Sale
    extra = 0


class ServiceAdmin(admin.ModelAdmin):
    inlines = [SaleInline,]
    extra= 0
    resource_class = ServiceResource

admin.site.register(Service, ServiceAdmin)
    
    

admin.site.register(LastBlue)

class AdjAdmin(admin.ModelAdmin):
    resource_class = AdjResource
admin.site.register(Adj, AdjAdmin)
