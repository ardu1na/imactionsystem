
from django.contrib import admin
from django.contrib.admin.models import LogEntry
#from django.db.models import Sum

from unfold.admin import ModelAdmin
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



    

class SaleAdmin(ModelAdmin):
    list_display = ('client',  'service', 'note', 'get_total', 'kind','status', 'date', 'comments')
    radio_fields = {'kind':admin.VERTICAL,}
    list_filter = ('kind', 'revenue', 'status')
    date_hierarchy = 'date'
    search_fields = ('client__name', 'note', 'service')
    empty_value_display = ''
    #autocomplete_fields = ('client',)
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



    """

    def client_link(self, book):
        url = reverse("admin:customers_client_change", args=[customers.client.id])
        link = '<a href="%s">%s</a>' % (url, customers.client.id)
        return mark_safe(link)
    client_link.short_description = 'client'"""   
    


    """def get_queryset(self, request):
        queryset = Sale.objects.filter(date__month=date.today().month)
        return queryset
    """

    """def dos_total(self, *args, **kwargs):
        #functions to calculate whatever you want...
        total = Sale.objects.filter(date__month=date.today().month).aggregate(tot=Sum('price'))['tot']
        return total

    def changelist_view(self, request, extra_context=None):
        my_context = {
            'total': self.dos_total(),
        }
        return super(SaleAdmin, self).changelist_view(request,
            extra_context=my_context)
            
            
            
         

    def dos_total(cl, *args, **kwargs):
        dos_total=0
        for item in items_for_result:
            dos_total += item.price
        return cl.dos_total(*args, **kwargs)"""



admin.site.register(Sale, SaleAdmin)

