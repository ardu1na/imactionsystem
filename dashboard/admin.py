from django.contrib import admin

from import_export.admin import ImportExportModelAdmin


from dashboard.models import Comms, LastBlue, Configurations,   ConfTier


from dashboard.resources import CommsResource,  ConfigurationsResource,  ConfTierResource

admin.site.register(LastBlue)

class ConfTierAdmin(ImportExportModelAdmin):
    resource_class = ConfTierResource    
admin.site.register(ConfTier, ConfTierAdmin)

class CommsAdmin(ImportExportModelAdmin):
    resource_class = CommsResource    
admin.site.register(Comms, CommsAdmin)


class ConfigurationsAdmin(ImportExportModelAdmin):
    resource_class = ConfigurationsResource    
admin.site.register(Configurations, ConfigurationsAdmin)
