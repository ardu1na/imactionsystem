from datetime import date, timedelta
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

last_blue = 0
try:
    last_blue =  LastBlue.objects.get(pk=1)
    blue = last_blue.compra

except:
    blue = 0



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
            
    

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        
        return f"{self.client} - {self.service}"
    
                
    class Meta:
        unique_together = (('service', 'client'),) 
        get_latest_by = ('created_at')
            
            
    YES = 'YES'
    NO = 'NO'
    DEBATIBLE = 'DEBATIBLE'

    FAIL_CHOICES = (
        (YES, ('YES')),
        (NO, ('NO')),
        (DEBATIBLE, ('DEBATIBLE')),
        ) 
    
    state = models.BooleanField(default=True)   
    comment_can = models.CharField(max_length=500, blank=True, null=True, verbose_name="COMMENT")
    date_can = models.DateField(null=True, blank=True, verbose_name="DATE")
    fail_can = models.CharField(max_length=50, choices=FAIL_CHOICES, blank=False,default=None, null=True, verbose_name="DO WE FAIL?")
            
      
        
class Adj(models.Model):
    A = "Account"
    S = "Service"
    ADJ_CHOICES = (
        (A, ('Account')),
        (S, ('Service')),
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    
    type = models.CharField(max_length=40, default=None, verbose_name="Account/Service", choices=ADJ_CHOICES, blank=False, null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="adj", null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="adj", null=True, blank=True)
       
    adj_percent = models.DecimalField(decimal_places=2, max_digits=16)

    old_value = models.DecimalField(default=0, max_digits=40, decimal_places=2)
    new_value = models.DecimalField(default=0, max_digits=40, decimal_places=2)
    dif = models.DecimalField(default=0, max_digits=40, decimal_places=2)
                
            
    
    def __str__ (self):
        if self.type == "Service":
            client = self.service.client.name
        else:
            client = self.client.name
        return f'{self.type}: {client} - {self.notice_date}'
        
    class Meta:
        ordering = ['-notice_date']

    notice_date = models.DateField(null=True,blank=True)
    adj_done = models.BooleanField(default=False)

    email_date = models.DateField(null=True, blank=True)
    remind_sent = models.BooleanField(default=False)
    

   
    def save(self, *args, **kwargs):
        if self.notice_date:
            fifteen_days_before = self.notice_date - timedelta(days=15)
            self.email_date =   fifteen_days_before
        
        super(Adj, self).save(*args, **kwargs)
                    


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
    


    """CANCELLED = "Cancelled"
    ACTIVE = "Active"
    CANCELLED_CHOICES = (
        (CANCELLED, ('Cancelled')),
        (ACTIVE, ('Active')))"""
    
    ARS = "ARS"
    USD = "USD"
    COIN_CHOICES = (
        (ARS, ('ARS')),
        (USD, ('USD')))

    client = models.ForeignKey(Client, related_name='sales', null=True, blank=True, on_delete=models.CASCADE, verbose_name="ACCOUNT")
   
    
    kind = models.CharField(max_length=50, choices=KIND_CHOICES, null=True, blank=False, default=None, verbose_name="KIND")
    
    date = models.DateField(default=date.today, verbose_name="DATE")
    
    total = models.IntegerField(blank=True, null=True, verbose_name="TOTAL")
    
    comments =models.CharField(max_length=500, null=True, blank=True, verbose_name="COMMENTS")
    
    
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="SERVICE", blank=False, default=None)
    
    price = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=50, default="ARS", choices=COIN_CHOICES, null=True, blank=False, verbose_name="CURRENCY")
    note = models.CharField(max_length=400, null=True, blank=True, verbose_name="NOTES")
    cost = models.IntegerField(default=0, verbose_name="COST")
    status = models.CharField(max_length=5, choices=S_CHOICES, null=True, blank=False, default=None, verbose_name="STATUS $")
    # cancelled = models.CharField(default='Active', max_length=50, choices=CANCELLED_CHOICES, blank=False)
    change = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12, null=True, blank=True)
    
    @property
    def get_change(self):
        change = 0
        if self.currency == "USD":
            change = self.price*Decimal(blue)
            return change
        else:
            return self.price
        
    
    
        
    def delete(self, *args, **kwargs):
        
        servicio = self.suscription
        servicio.total -= self.change
        servicio.save()
        super().delete(*args, **kwargs)    
        
    
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
    revenue = models.CharField(max_length=20, null=True, blank=False, default=None, choices=REVENUE_CHOICES, help_text="Leave blank to automatically fill", verbose_name="REVENUE")

    def save(self, *args, **kwargs):
        self.change = self.get_change
        self.revenue = self.get_revenue()
        if self.pk:

            if self.note != "auto revenue sale" and self.revenue == "RR":     
                self.get_service_or_update()
            super(Sale, self).save(*args, **kwargs)   
        else:
            if self.note != "auto revenue sale" and self.revenue == "RR":
                     
                self.get_service_or_update()
            super(Sale, self).save(*args, **kwargs)

            
      
    
    ################### 
    def get_service_or_update (self, *args, **kwargs):  
        print()
        print("CHEKCING IF SERVICE WITH SAME SERVICE AND CLIENT DO EXISTS.......")
        print(".........")                  
        try:
            service = Service.objects.get(
                client=self.client, service=self.service) 
            print(" IT EXISTS, checking if sale is already asociated.........")                  
               
            if not self.suscription:                
                print(" sale is not asociated... setting relation and adding sale value into service")                  

                #service.sales.add(self, bulk= False)
                service.total += Decimal(self.change)
                print()
                print("################### saving service ################################")
                print(".........")  
                service.save()     
                print(".....service saved....")  
                print("################### setting rel service --- sale  ################################")

                self.suscription=service
                print(f"################### rel {self.suscription}: service --- sale  ################################")

            print("sale is allready asociated into service, nothing to do")
                                         
            
        except Service.DoesNotExist:       
            print(" IT DONT EXISTS")                  
            
            values = {
                "client": self.client,
                "service": self.service,
                "total": self.change,
                }            
            print("setting client service and total as sale values.........")  
            service = Service(**values)
            print()
            print("################### saving service with new values ################################")
            service.save()  
            print(".....SERVICE SAVED....")      
            print("adding sale relationship.........")  

            self.suscription=service
            
            
                
    
    
    
                        
                    

            
        
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
    
    
        
        