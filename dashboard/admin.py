from django.contrib import admin

from import_export.admin import ImportExportModelAdmin


from dashboard.models import Comms, LastBlue, Configurations,  BackUps, ConfTier, AutoRevenue


from dashboard.resources import CommsResource, LastBlueResource, ConfigurationsResource,  BackUpsResource, ConfTierResource,  AutoRevenueResource

class AutoRevenueAdmin(ImportExportModelAdmin):
    resource_class = AutoRevenueResource    
admin.site.register(AutoRevenue, AutoRevenueAdmin)


class ConfTierAdmin(ImportExportModelAdmin):
    resource_class = ConfTierResource    
admin.site.register(ConfTier, ConfTierAdmin)

class CommsAdmin(ImportExportModelAdmin):
    resource_class = CommsResource    
admin.site.register(Comms, CommsAdmin)


class BackUpsAdmin(ImportExportModelAdmin):
    resource_class = BackUpsResource    
admin.site.register(BackUps, BackUpsAdmin)



class LastBlueAdmin(ImportExportModelAdmin):
    resource_class = LastBlueResource    
admin.site.register(LastBlue, LastBlueAdmin)



class ConfigurationsAdmin(ImportExportModelAdmin):
    resource_class = ConfigurationsResource    
admin.site.register(Configurations, ConfigurationsAdmin)
