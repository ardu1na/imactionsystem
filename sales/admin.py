
from django.contrib import admin
from django.contrib.admin.models import LogEntry

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from dashboard.resources import SaleResource
from sales.models import Sale, LastBlue



@admin.register(LastBlue)


class SaleAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = SaleResource
admin.site.register(Sale, SaleAdmin)


