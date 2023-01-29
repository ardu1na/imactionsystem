from django.contrib import admin
from unfold.admin import ModelAdmin
from sales.models import Sale
from customers.models import  BankData, AbstractClient

admin.site.site_header = 'IMACTIONS'
admin.site.index_title = 'Home'
admin.site.site_title = 'IMACTIONS'


class SaleInstanceInline(admin.TabularInline):
    model = Sale
    extra = 0
    show_change_link = True
    fk_name = 'account'

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


class BankDataInstanceInline(admin.StackedInline):
    model = BankData
    extra = 0
    class Meta:
        verbose_name_plural = "BANK DATA"
        verbose_name= "BANK DATA"

class ClientAdmin(ModelAdmin): 
    inlines = [SaleInstanceInline, BankDataInstanceInline]
    list_display = ('tier', "customer", 'get_seo', "get_gads", "get_fads", "get_lnkd", "get_cm", "get_wp", 'get_combo', 'rr')
    search_fields = ("customer", "business_name")
    date_hierarchy = 'date'
    list_per_page = 500
    list_display_links = ('customer', 'business_name', 'website')

    """def get_queryset(self, request):
        
        return super(ClientAdmin, self).get_queryset(request).filter(cancelled="Active")
"""

    fieldsets = (
        ('CLIENT', {
            'fields': ('customer', 'date')
        }),
        (None, {
            'fields': ( 'business_name', 'source', 'website')
        }),
        ('CONTACT DATA', {
            
            'fields': ('phone_number', 'email', )
        }),
        ('EXTRA INFO', {
            'classes' : ('collapse',),
            'fields': ( 'landing_page', 'phone_2', 'email_2', 'email_admin',)
        }),
        ('CANCELLATION', {
            'classes' : ('collapse',),
            'fields': ('date_can', 'comment_can', 'fail_can')
        }),
    )


    @admin.display(description='SEO')
    def get_seo(self, obj):
        seo_total=0
        if obj.cancelled == "Active":
            for sale in obj.sales.all():
                if sale.service == "SEO":
                    if sale.cancelled == "Active":
                        seo_total += sale.price
        return '${:,}'.format(seo_total)

    @admin.display(description='GADS')
    def get_gads(self, obj):
        gads_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "Google Ads":
                   if sale.cancelled == "Active":
                        gads_total += sale.price
        return '${:,}'.format(gads_total)

    @admin.display(description='COMBO')
    def get_combo(self, obj):
        combo_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "COMBO":
                    if sale.cancelled == "Active":
                        combo_total += sale.price
        return '${:,}'.format(combo_total)



    @admin.display(description='FADS')
    def get_fads(self, obj):
        fads_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "Facebook Ads":
                    if sale.cancelled == "Active":
                        fads_total += sale.price
        return '${:,}'.format(fads_total)



    @admin.display(description='LinkedIn')
    def get_lnkd(self, obj):
        lnkd_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "LinkedIn":
                    if sale.cancelled == "Active":
                        lnkd_total += sale.price
        return '${:,}'.format(lnkd_total)



    @admin.display(description='CM')
    def get_cm(self, obj):
        cm_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "Community Management":
                    if sale.cancelled == "Active":
                        cm_total += sale.price
        return '${:,}'.format(cm_total)


    @admin.display(description='WP')
    def get_wp(self, obj):
        wp_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "Web Plan":
                    if sale.cancelled == "Active":
                        wp_total += sale.price
        return '${:,}'.format(wp_total)

    @admin.display(description='COMBO')
    def get_combo(self, obj):
        combo_total=0
        for sale in obj.sales.all():
            if obj.cancelled == "Active":
                if sale.service == "COMBO":
                    if sale.cancelled == "Active":
                        combo_total += sale.price
        return '${:,}'.format(combo_total)


          



admin.site.register(AbstractClient, ClientAdmin)