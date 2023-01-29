
from django.contrib import admin
from django.contrib.admin.models import LogEntry
#from django.db.models import Sum

from unfold.admin import ModelAdmin
from cancellations.models import Cancellation
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
    list_display = ('account',  'service', 'note', 'get_total', 'kind','status', 'date', 'comments')
    radio_fields = {'kind':admin.VERTICAL,}
    list_filter = ('kind', 'revenue', 'status')
    date_hierarchy = 'date'
    search_fields = ('account__customer', 'note', 'service')
    empty_value_display = ''
    #autocomplete_fields = ('account',)
    show_change_link = True
    list_display_links = ('account',  'service', 'kind','status', 'date', 'comments')

    fieldsets = (
        ('ACCOUNT', {
            'fields': ('account','kind',)
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
    client_link.short_description = 'Account'"""   
    


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


class CancellationAdmin(ModelAdmin):
    list_display =  ('date_can', 'get_type', 'get_client', 'get_service', 'get_price', 'fail_can', 'comment_can')
    search_fields = ("comment_can",)
    list_filter = ('fail_can',)
    date_hierarchy = 'date_can'
    list_display_links = ('date_can', 'comment_can', 'fail_can','get_type', 'get_client', 'get_service')



    readonly_fields = ('get_type', 'get_client', 'get_service',)
    
    fieldsets = (
        (None, {
            'fields': ('date_can', 'get_type',)
        }),
        
        (None, {
            'fields': ('get_client', 'get_service')
        }),

        (None, {
            'fields': ('comment_can', 'fail_can')
        }),
        
        
    )



    def has_add_permission(self, request):
        return False


    @admin.display(description='ACC/SERV')
    def get_type(self, obj):
        
        try:
            if obj.client.cancelled == "Cancelled":
                return "ACCOUNT"
        except:
            return "SERVICE"

    @admin.display(description='ACCOUNT')
    def get_client(self, obj):
        
        try:
            if obj.client.cancelled == "Cancelled":
                return obj.client.customer
        except:
            return obj.sale.account


    @admin.display(description='SERVICE')
    def get_service(self, obj):
        
        try:
            if obj.client.cancelled == "Cancelled":
                sales = obj.client.sales.all()
                return ", " .join(sale.service for sale in sales[:5])
        except:
            return obj.sale.service


    @admin.display(description=' $$ ')
    def get_price(self, obj):
        
        try:
            if obj.client.cancelled == "Cancelled":
                sales = obj.client.sales.all()
                total = 0
                for sale in sales:
                    total += sale.price 
                return '${:,}'.format(total)
        except:
            return '${:,}'.format(obj.sale.price)
                        
    

admin.site.register(Cancellation, CancellationAdmin)


