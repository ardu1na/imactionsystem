from datetime import date
from django.db import models
from django.db.models import F
from django.contrib import admin
from customers.models import Client
from decimal import Decimal


class LastBlue (models.Model):
    compra = models.DecimalField(max_digits=15, decimal_places=2
                                 )
    date_updated = models.DateTimeField(auto_now=True)
    
    @property
    def get_blue(self):
        return self.compra


#last_blue = LastBlue.objects.get(pk=1)
blue = 1 #last_blue.compra



class Service(models.Model):
            
        SEO ='SEO'
        GADS = 'Google Ads'
        FADS = 'Facebook Ads'
        LIKD = 'LinkedIn'
        WEB_PLAN = 'Web Plan'
        COMBO = 'Combo'
        CM = 'Community Management'
        EMKTG = 'Email Marketing'
        OTHER_RR = 'Others RR'
        SERVICE_CHOICES = (
            (SEO, ('SEO')),
            (GADS, ('Google Ads')),
            (FADS, ('Facebook Ads')),
            (LIKD, ('LinkedIn')),
            (CM, ('Community Management')),
            (WEB_PLAN, ('Web Plan')),
            (COMBO, ('Combo')),
            (OTHER_RR, ('Others RR')),

        )
        service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
        client = models.ForeignKey(Client, related_name="services", on_delete=models.CASCADE, null=True)
        
        total = models.DecimalField(default=0, decimal_places=2, max_digits=20)
        last_adj = models.DecimalField(default=0, decimal_places=2, max_digits=6)
        adj_at = models.DateField(null=True, blank=True)
        
        def __str__(self):
            
            return f"{self.service} - {self.client}"
        
        @property        
        def update_total(self):
            if self.total == 0:
                total=0
                for sale in self.sales.all():
                    total += sale.change
                self.total=total
                    
                print("*******************  REGISTRO   **********************")
            print("*****************************  FIN    *****************************")
            
            
        
            

            
            
        
        """def save(self, *args, **kwargs):
            self.total = self.update_total()
           
            
            super(Service, self).save(*args, **kwargs)"""
        
            
            
        class Meta:
            unique_together = (('service', 'client'),) 


class Sale(models.Model):

    UPSELL='Upsell'
    NEW_CLIENT='New Client'
    CROSSSELL = 'Cross Sell'
    KIND_CHOICES = (
        (UPSELL, ('Upsell')),
        (NEW_CLIENT, ('New Client')),
        (CROSSSELL, ('Cross Sell')))

    P = "P"
    FCD = "FCD"
    FC = "FC"
    S_CHOICES=(
        (P, ("P")),
        (FCD, ("FCD")),
        (FC, ("FC")),)

    SEO ='SEO'
    GADS = 'Google Ads'
    FADS = 'Facebook Ads'
    DW = 'Web Design'
    HO = 'Hosting'
    LIKD = 'LinkedIn'
    SSL = 'SSL certificate'
    WEB_PLAN = 'Web Plan'
    COMBO = 'Combo'
    CM = 'Community Management'
    EMKTG = 'Email Marketing'
    OTHER = 'Others'
    OTHER_RR = 'Others RR'
    SERVICE_CHOICES = (
        (SEO, ('SEO')),
        (GADS, ('Google Ads')),
        (FADS, ('Facebook Ads')),
        (LIKD, ('LinkedIn')),
        (CM, ('Community Management')),
        (WEB_PLAN, ('Web Plan')),
        (COMBO, ('Combo')),
        (DW, ('Web Design')),
        (HO, ('Hosting')),
        (SSL, ('SSL certificate')),
        (OTHER, ('Others')),
        (OTHER_RR, ('Others RR')),

    )

    def get_revenue(self):
        if self.service == 'SEO' or self.service == 'Google Ads' or self.service == 'Community Management' \
        or self.service == 'Facebook Ads' or self.service == 'Web Plan' or self.service == 'LinkedIn' \
        or self.service == 'Combo' or self.service == 'Others RR':
            return ("RR")
        else:
            return ("OneOff")

    RR = 'RR'
    OneOff = 'OneOff'
    REVENUE_CHOICES=(
        (RR, ("RR")),
        (OneOff, ("OneOff")),)

    CANCELLED = "Cancelled"
    ACTIVE = "Active"
    CANCELLED_CHOICES = (
        (CANCELLED, ('Cancelled')),
        (ACTIVE, ('Active')))
    
    ARS = "ARS"
    USD = "USD"
    COIN_CHOICES = (
        (ARS, ('ARS')),
        (USD, ('USD')))

    client = models.ForeignKey(Client, related_name='sales', null=True, blank=True, on_delete=models.CASCADE, verbose_name="ACCOUNT")

    raice = models.DecimalField(verbose_name="ADJUSTMENT", decimal_places=2, max_digits=12, null=True, blank=True)
    raice_date = models.DateField(blank=True, null=True, default=date.today, verbose_name="DATE UPDATED")    
    
    kind = models.CharField(max_length=50, choices=KIND_CHOICES, null=True, blank=False, default=None, verbose_name="KIND")
    
    date = models.DateField(default=date.today, verbose_name="DATE")
    
    total = models.IntegerField(blank=True, null=True, verbose_name="TOTAL")
    
    comments =models.CharField(max_length=500, null=True, blank=True, verbose_name="COMMENTS")
    
    revenue = models.CharField(max_length=20, null=True, blank=False, default=None, choices=REVENUE_CHOICES, help_text="Leave blank to automatically fill", verbose_name="REVENUE")
    
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="SERVICE", blank=False, default=None)
    
    price = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=50, default="ARS", choices=COIN_CHOICES, null=True, blank=False, verbose_name="CURRENCY")
    note = models.CharField(max_length=400, null=True, blank=True, verbose_name="NOTES")
    cost = models.IntegerField(default=0, verbose_name="COST")
    status = models.CharField(max_length=5, choices=S_CHOICES, null=True, blank=False, default=None, verbose_name="STATUS $")
    cancelled = models.CharField(default='Active', max_length=50, choices=CANCELLED_CHOICES, blank=False)
    change = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12, null=True, blank=True)
    
    @property
    def get_change(self):
        change = 0
        if self.currency == "USD":
            change = self.price*Decimal(blue)
            return change
        else:
            return self.price
        
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
    fail_can = models.CharField(max_length=50, choices=FAIL_CHOICES, blank=False,default=None, null=True, verbose_name="DO WE FAIL?")
        
    
    def update_db_sales (self, *args, **kwargs):
        if self.cancelled == "Active":
            if self.note != "auto revenue sale":
                if self.revenue == "RR":                    
                    service, created = Service.objects.update_or_create(
                        service=self.service,
                        client=self.client,                        
                    )                    
                    self.suscription = service
                    
    def save(self, *args, **kwargs):
        self.change = self.get_change
        self.revenue = self.get_revenue()
        self.update_db_sales()
        if self.pk:
            pass
        else: 
            self.suscription.total += self.change
            self.suscription.save()
        super(Sale, self).save(*args, **kwargs)



    @property
    def get_previous(self, *args, **kwargs):
        previous_sales = Sale.objects.filter(service=self.service, client=self.client).order_by('-raice_date')
        if previous_sales:
            return previous_sales[0]
        else:
            return None
        
        
                    
                        
                    

            
        
    @property
    def total(self):
        result = self.price - self.cost
        return '${:,}'.format(result)

    def __str__(self):
       return '{} - {} '.format(self.client, self.service)


    @admin.display
    def subtotal(self):
        return '${:,}'.format(self.price - self.cost)

    @property
    def price_service(self):
        return "$%s" % self.price if self.price else ""

    @property
    def cost_service(self):
        return "$%s" % self.cost if self.cost else "$0"

   
    @property
    def get_date(self):
        formatdate = self.date.strftime('%d/%m/%Y')
        return formatdate
    
    @property
    def get_date_can(self):
        formatdate = self.date_can.strftime('%d/%m/%Y')
        return formatdate


   

    class Meta:
        ordering = ['-date']
        
    suscription = models.ForeignKey(Service, related_name="sales", on_delete=models.CASCADE, null=True, blank=True)
    
    
        
        