from datetime import date
from django.db import models
from django.contrib import admin
from customers.models import Client


class Sale(models.Model):


    UPSELL='Upsell'
    NEW_CLIENT='New Client'
    CROSSSELL = 'Cross Sell'

    KIND_CHOICES = (
        (UPSELL, ('Upsell')),
        (NEW_CLIENT, ('New Client')),
        (CROSSSELL, ('Cross Sell'))
    )



    P = "P"
    FCD = "FCD"
    FC = "FC"

    S_CHOICES=(
        (P, ("P")),
        (FCD, ("FCD")),
        (FC, ("FC")),
    )



    SEO ='SEO'
    GADS = 'Google Ads'
    FADS = 'Facebook Ads'
    DW = 'Web Design'
    HO = 'Hosting'
    LIKD = 'LinkedIn'
    SSL = 'SSL certificate'
    WEB_PLAN = 'Web Plan'
    COMBO = 'COMBO'
    CM = 'Community Management'
    EMKTG = 'Email Marketing'
    OTHER = 'Other'

    SERVICE_CHOICES = (
        (SEO, ('SEO')),
        (GADS, ('Google Ads')),
        (FADS, ('Facebook Ads')),
        (LIKD, ('LinkedIn')),
        (CM, ('Community Management')),
        (WEB_PLAN, ('Web Plan')),
        (COMBO, ('COMBO')),
        (DW, ('Web Design')),
        (HO, ('Hosting')),
        (SSL, ('SSL certificate')),
        (OTHER, ('Other')),
    )

    def get_revenue(self):
        if self.service == 'SEO' or self.service == 'Google Ads' or self.service == 'Community Management' \
        or self.service == 'Facebook Ads' or self.service == 'Web Plan' or self.service == 'LinkedIn' \
        or self.service == 'COMBO':
            return ("RR")
        else:
            return ("OneOff")

    RR = 'RR'
    OneOff = 'OneOff'
    REVENUE_CHOICES=(
        (RR, ("RR")),
        (OneOff, ("OneOff")),
    )

    CANCELLED = "Cancelled"
    ACTIVE = "Active"

    CANCELLED_CHOICES = (
        (CANCELLED, ('Cancelled')),
        (ACTIVE, ('Active'))
    )


    client = models.ForeignKey(Client, related_name='sales', null=True, blank=True, on_delete=models.CASCADE, verbose_name="ACCOUNT")
    kind = models.CharField(max_length=50, choices=KIND_CHOICES, null=True, blank=True, verbose_name="KIND")
    date = models.DateField(default=date.today, verbose_name="DATE")
    total = models.IntegerField(blank=True, null=True, verbose_name="TOTAL")
    comments =models.CharField(max_length=500, null=True, blank=True, verbose_name="COMMENTS")
    revenue = models.CharField(max_length=20, null=True, blank=True, choices=REVENUE_CHOICES, help_text="Leave blank to automatically fill", verbose_name="REVENUE")
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="SERVICE")
    price = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12)
    note = models.CharField(max_length=400, null=True, blank=True, verbose_name="NOTES")
    cost = models.IntegerField(default=0, verbose_name="COST")
    status = models.CharField(max_length=5, choices=S_CHOICES, null=True, blank=True, verbose_name="STATUS $")
    cancelled = models.CharField(default='Active', max_length=50, choices=CANCELLED_CHOICES)
    objects = models.Manager()
    
    YES = 'YES'
    NO = 'NO'
    DEBATIBLE = 'DEBATIBLE'

    FAIL_CHOICES = (
        (YES, ('YES')),
        (NO, ('NO')),
        (DEBATIBLE, ('DEBATIBLE')),
        )
    
    comment_can = models.CharField(max_length=500, blank=True, null=True, verbose_name="COMMENT")
    date_can = models.DateField(null=True, blank=True, verbose_name="DATE")
    fail_can = models.CharField(max_length=50, choices=FAIL_CHOICES, blank=True, null=True, verbose_name="DO WE FAIL?")
        
    
    def save(self, *args, **kwargs):
        
        self.revenue = self.get_revenue()
        super(Sale, self).save(*args, **kwargs)


    @property
    def total(self):
        result = self.price - self.cost
        return '${}'.format(result)

    def __str__(self):
       return '{} - {}'.format(self.client, self.date)


    @admin.display
    def subtotal(self):
        return '${}'.format(self.price - self.cost)

    @property
    def price_service(self):
        return "$%s" % self.price if self.price else ""

    @property
    def cost_service(self):
        return "$%s" % self.cost if self.cost else "$0"

   



   
