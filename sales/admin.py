
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from sales.models import Sale, Service, Adj, Comm

from dashboard.resources import ServiceResource, SaleResource, AdjResource, CommResource




class CommAdmin(ImportExportModelAdmin):
    resource_class = CommResource
admin.site.register(Comm, CommAdmin)


class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource

admin.site.register(Service, ServiceAdmin)
    
    
class SaleAdmin(ImportExportModelAdmin):
    list_display = ['date', 'service', 'kind', 'client', 'change', 'note']
    search_fields = ['note',]
    resource_class = SaleResource
admin.site.register(Sale, SaleAdmin)


class AdjAdmin(ImportExportModelAdmin):
    resource_class = AdjResource
admin.site.register(Adj, AdjAdmin)
