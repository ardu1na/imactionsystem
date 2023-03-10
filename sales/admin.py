
from django.contrib import admin
from django.contrib.admin.models import LogEntry

from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from dashboard.resources import SaleResource
from sales.models import Sale





@admin.register(LogEntry)
class LogEntryAdmin(ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False



    

class SaleAdmin(ModelAdmin, ImportExportModelAdmin):
    
    resource_class = SaleResource
    list_display = ('client',  'service', 'note', 'get_total', 'kind','status', 'date', 'comments')
    radio_fields = {'kind':admin.VERTICAL,}
    list_filter = ('kind', 'revenue', 'status')
    date_hierarchy = 'date'
    search_fields = ('client__name', 'note', 'service')
    empty_value_display = ''
    show_change_link = True
    list_display_links = ('client',  'service', 'kind','status', 'date', 'comments')

    fieldsets = (
        ('client', {
            'fields': ('client','kind',)
        }),
        ('SERVICE', {
            'fields': ('revenue', 'service', 'price' )
        }),
        (None, {
            'fields': ('note', 'date', )
        }),
        (None, {
            'fields': ('cost', )
        }),
        (None, {
            'fields': ('status', 'comments')
        }),
        ('CANCELLATION', {
            'classes' : ('collapse',),
            'fields': ('date_can', 'comment_can', 'fail_can')
        }),
    )

    @admin.display(description='total')
    def get_total(self, obj):
        return '${:,}'.format(obj.price)


admin.site.register(Sale, SaleAdmin)