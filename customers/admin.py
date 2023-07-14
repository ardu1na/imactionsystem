from django.contrib import admin
from sales.models import Sale
from customers.models import  ConfTier, BackUps, Client, AutoRevenue

from import_export.admin import ImportExportModelAdmin

from dashboard.resources import ClientResource, BackUpsResource, ConfTierResource,  AutoRevenueResource

admin.site.site_header = 'IMACTIONS'
admin.site.index_title = 'Home'
admin.site.site_title = 'IMACTIONS'



class BackUpsAdmin(ImportExportModelAdmin):
    resource_class = BackUpsResource    
admin.site.register(BackUps, BackUpsAdmin)



class AutoRevenueAdmin(ImportExportModelAdmin):
    resource_class = AutoRevenueResource    
admin.site.register(AutoRevenue, AutoRevenueAdmin)


class ConfTierAdmin(ImportExportModelAdmin):
    resource_class = ConfTierResource    
admin.site.register(ConfTier, ConfTierAdmin)

class SaleInstanceInline(admin.TabularInline):
    model = Sale
    extra = 0
    show_change_link = True
    fk_name = 'client'

    fieldsets = (
        ('SALE', {
            'fields': ('service',)
        }),

        (None, {
            'fields': ( 'date',)
        }),
        (None, {
            'fields': ('price' ,)
        }),
    )
    class Meta:
        verbose_name_plural = "SALES"
        verbose_name= "SALE"


class ClientAdmin(ImportExportModelAdmin):
    resource_class = ClientResource    
admin.site.register(Client, ClientAdmin)

