from django.contrib import admin

from import_export.admin import ImportExportModelAdmin


from dashboard.models import Comms, LastBlue, Configurations


from dashboard.resources import CommsResource, LastBlueResource, ConfigurationsResource


class CommsAdmin(ImportExportModelAdmin):
    resource_class = CommsResource    
admin.site.register(Comms, CommsAdmin)



class LastBlueAdmin(ImportExportModelAdmin):
    resource_class = LastBlueResource    
admin.site.register(LastBlue, LastBlueAdmin)



class ConfigurationsAdmin(ImportExportModelAdmin):
    resource_class = ConfigurationsResource    
admin.site.register(Configurations, ConfigurationsAdmin)
