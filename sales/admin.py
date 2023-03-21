
from django.contrib import admin

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from dashboard.resources import SaleResource
from sales.models import Sale, LastBlue



@admin.register(LastBlue)


class SaleAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = SaleResource
admin.site.register(Sale, SaleAdmin)


