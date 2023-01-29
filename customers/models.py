from datetime import date
from django.db import models
from django.contrib import admin
from cancellations.models import Cancellation, CancellationManager
from django.db.models import Q


"""class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(sales__kind='RR')"""



class Client(Cancellation):
    #objects = ClientManager()
    GOOGLE_ADS='Google Ads'
    FACEBOOK_ADS='Facebook Ads'
    SEO='SEO'
    LINKEDIN='LinkedIn'
    CALL='Call'
    EMAIL_MARKETING='Email Marketing'
    REFERRAL ='Referral'
    RESELLER = "Reseller"

    CANAL_CHOICES=(
        (GOOGLE_ADS, ('Google Ads')),
        (FACEBOOK_ADS, ('Facebook Ads')),
        (SEO, ('SEO')),
        (LINKEDIN, ('LinkedIn')),
        (CALL, ('Call')),
        (EMAIL_MARKETING, ('Email Marketing')),
        (REFERRAL, ('Referral')),
        (RESELLER, ('Reseller'))
    )

    CANCELLED = "Cancelled"
    ACTIVE = "Active"

    CANCELLED_CHOICES = (
        (CANCELLED, ('Cancelled')),
        (ACTIVE, ('Active'))
    )


    id_client = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=30)
    business_name = models.CharField(max_length=30, blank=True, null=True)
    source = models.CharField(max_length=50, choices=CANAL_CHOICES, null=True, blank=True)
    date = models.DateField(editable=True, default=date.today)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email_2 = models.EmailField(blank=True, null=True)
    email_admin = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    phone_2 = models.CharField(max_length=25, blank=True, null=True)
    landing_page = models.URLField(blank=True, null=True)
    cancelled = models.CharField(default='Active', max_length=50, choices=CANCELLED_CHOICES)
    #rr_tabla = models.CharField(max_length=20, null=True, blank= True)

    objects = models.Manager()
    customan = CancellationManager()


    def __str__(self):
       return str(self.customer)

    def get_cancelled(self):
        if self.comment_can:
            return 'Cancelled'
        if self.comment_can == None or self.comment_can == "":
            return "Active"

    """def get_rr_tabla(self):
        sales = self.sales.all()
        for sale in sales:
            if sale.revenue == "RR":
                return "RR"
            break"""



    def save(self, *args, **kwargs):
        self.cancelled = self.get_cancelled()
        #self.rr_tabla = self.get_rr_tabla()
        super(Client, self).save(*args, **kwargs)


    @property
    def total_rr(self):
        total = 0
        for sale in self.sales.all():
            if sale.revenue == "RR":
                total += sale.price
        return total

    @property
    @admin.display(description="RR")
    def rr(self):
        total = 0
        if self.cancelled =="Active":
            for sale in self.sales.all():
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total += sale.price
        return '${}'.format(total)

    

    @property
    def get_seo(self, *args, **kwargs):
        seo_total=0
        if self.cancelled == "Active":
            for sale in self.sales.all():
                if sale.service == "SEO":
                    if sale.cancelled == "Active":
                        seo_total += sale.price
        return '${:,}'.format(seo_total)

    @property
    def get_gads(self, *args, **kwargs):
        gads_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Google Ads":
                   if sale.cancelled == "Active":
                        gads_total += sale.price
        return '${:,}'.format(gads_total)

    @property
    def get_combo(self, *args, **kwargs):
        combo_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "COMBO":
                    if sale.cancelled == "Active":
                        combo_total += sale.price
        return '${:,}'.format(combo_total)



    @property
    def get_fads(self, *args, **kwargs):
        fads_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Facebook Ads":
                    if sale.cancelled == "Active":
                        fads_total += sale.price
        return '${:,}'.format(fads_total)



    @property
    def get_lnkd(self, *args, **kwargs):
        lnkd_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "LinkedIn":
                    if sale.cancelled == "Active":
                        lnkd_total += sale.price
        return '${:,}'.format(lnkd_total)



    @property
    def get_cm(self, *args, **kwargs):
        cm_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Community Management":
                    if sale.cancelled == "Active":
                        cm_total += sale.price
        return '${:,}'.format(cm_total)


    @property
    def get_wp(self, *args, **kwargs):
        wp_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Web Plan":
                    if sale.cancelled == "Active":
                        wp_total += sale.price
        return '${:,}'.format(wp_total)

    @property
    def get_combo(self, *args, **kwargs):
        combo_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "COMBO":
                    if sale.cancelled == "Active":
                        combo_total += sale.price
        return '${:,}'.format(combo_total)



    
    @property
    def tier(self):
        if self.total_rr <= 30000:
            return "V"
        elif self.total_rr > 30000 and self.total_rr <= 65000:
            return "IV"
        elif self.total_rr > 65000 and self.total_rr <= 110000:
            return "III"
        elif self.total_rr > 110000 and self.total_rr <= 200000:
            return "II"
        elif self.total_rr > 200000:
            return "I"


class AbstractClientManager(models.Manager):
    def get_queryset(self):
      # sale.revenue="RR"
        return super(AbstractClientManager, self).get_queryset().filter(cancelled="Active")


class AbstractClient(Client):
    objects = AbstractClientManager()
    class Meta:
        proxy = True
        verbose_name = "CLIENT"
        verbose_name_plural = "CLIENTS"


class BankData(models.Model):
    MercadoPago = 'MercadoPago'
    Debit_CBU = 'Debit'
    Wire_transfer = 'Wire transfer'
    Cash = 'Cash'

    PAYMENT_CHOICES = (
        (MercadoPago,  ('MercadoPago')),
        (Debit_CBU, ('Debit')),
        (Wire_transfer, ('Wire transfer')),
        (Cash, ('Cash')),
        )

    payment = models.CharField(max_length=50,choices=PAYMENT_CHOICES, blank=False, null=False)
    cbu = models.CharField(null=True, blank=True, max_length=100)
    alias = models.CharField(max_length=200, blank=True, null=True, default="")
    CUIT = models.CharField(max_length=50, blank=True, null=True, default="")
    detail = models.CharField(max_length=500, default="", blank=True, null=True)
    account = models.ForeignKey(Client, related_name= 'accounts', on_delete=models.CASCADE, blank=False, null=False)
    

    def __str__(self):
        return 'Bank account {} of {}'.format(self.payment, self.account)

    class Meta:
        verbose_name_plural = "bank data"

