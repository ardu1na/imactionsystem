from datetime import date, timedelta
from decimal import Decimal

from django.db import models
from django.contrib import admin

from customers.models import Client
from expenses.models import Employee
from dashboard.models import LastBlue, Comms

# get commision value from configurations db
try:
    comms = Comms.objects.get(id=1)
except:
    comms = Comms.objects.create(              
                )
# get 'dolar blue / pesos' exchange to display info
try:
    last_blue =  LastBlue.objects.get(pk=1)
    blue = last_blue.venta
except:
    blue = 0

from django.db import models

# Constants for service choices and fail choices
SERVICE_CHOICES = (
    ('SEO', 'SEO'),
    ('Google Ads', 'Google Ads'),
    ('Facebook Ads', 'Facebook Ads'),
    ('LinkedIn', 'LinkedIn'),
    ('Community Management', 'Community Management'),
    ('Web Plan', 'Web Plan'),
    ('Combo', 'Combo'),
    ('Others RR', 'Others RR'),
)

FAIL_CHOICES = (
    ('YES', 'YES'),
    ('NO', 'NO'),
    ('DEBATIBLE', 'DEBATIBLE'),
)

class Service(models.Model):
    """
    Service is a rr subscription of a service by a client.
    It has several sales (get by instance.sales).
    To see if it has adjustments asociated : instance.adj
    
    """

    # Fields related to the service
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    client = models.ForeignKey(Client, related_name="services", on_delete=models.CASCADE, null=True)
    total = models.DecimalField(default=0, decimal_places=2, max_digits=20) ## Total field: This field might not reflect the actual value of the service since sales in USD can vary due to exchange rates. ITS IS ONLY FOR DISPLAY PORPUSES


    # Timestamps for creation and last update
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.service}"

    class Meta:
        # Ensure that the combination of service and client is unique
        unique_together = (('service', 'client'),)
        # Use created_at for the latest record retrieval
        get_latest_by = ('created_at',)

    # Fields related to service state and cancellation
    state = models.BooleanField(default=True)
    comment_can = models.CharField(max_length=500, blank=True, null=True, verbose_name="COMMENT")
    date_can = models.DateField(null=True, blank=True, verbose_name="DATE cancellation")
    fail_can = models.CharField(max_length=50, choices=FAIL_CHOICES, blank=True, null=True, verbose_name="DO WE FAIL?")

              
class Adj(models.Model):
    """
    Model representing an adjustment made for an Account or a Service.
    """

    # Choices for type field (Account or Service)
    A = "Account"
    S = "Service"
    ADJ_CHOICES = (
        (A, ('Account')),
        (S, ('Service')),
    )

    # Fields related to timestamps
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # Type of the adjustment (Account or Service)
    type = models.CharField(max_length=40, default=None, verbose_name="Account/Service", choices=ADJ_CHOICES, blank=False, null=False)

    # Foreign keys for associated Service and Client
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="adj", null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="adj", null=True, blank=True)

    # Fields representing adjustment details
    adj_percent = models.DecimalField(decimal_places=2, max_digits=16)
    old_value = models.DecimalField(default=0, max_digits=40, decimal_places=2)
    new_value = models.DecimalField(default=0, max_digits=40, decimal_places=2)
    dif = models.DecimalField(default=0, max_digits=40, decimal_places=2)

    def __str__(self):
        """
        Returns a string representation of the adjustment.
        If the type is 'Service', it displays the client's name and notice date.
        If the type is 'Account', it displays the client's name and notice date.
        """
        if self.type == "Service":
            client = self.service.client.name
        else:
            client = self.client.name
        return f'{self.type}: {client} - {self.notice_date}'

    class Meta:
        # Ordering adjustments by notice date in descending order
        ordering = ['-notice_date']

    # Date when the adjustment notice was received
    notice_date = models.DateField(null=True, blank=True)

    # Boolean flag indicating whether the adjustment has been completed
    adj_done = models.BooleanField(default=False)

    # Date when the reminder email is scheduled to be sent (15 days before the notice date)
    email_date = models.DateField(null=True, blank=True)

    # Boolean flag indicating whether the reminder email has been sent
    remind_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Custom save method to update the email_date when the notice_date is set.
        It sets the email_date to fifteen days before the notice_date.
        """
        if self.notice_date:
            fifteen_days_before = self.notice_date - timedelta(days=15)
            self.email_date = fifteen_days_before

        super(Adj, self).save(*args, **kwargs)


class Sale(models.Model):
    # obtener el porcentaje de comisión acorde al tipo de venta
    @property
    def get_comm_per(self):
        
        if self.change >= comms.rr_1:
            ## obtener el porcentaje de comisiones por venta para los empleados vendedores
            if self.revenue == "OneOff":
                return comms.one_off
            else:    
                if self.kind == "Upsell":
                    return comms.up_sell
                else:
                    # el porcentaje de comisión de las ventas rr q no son upsell varian según parámetros configurados x el usuario
                    # se obtienen de dashboard.comms pk=1
                    if self.change >= comms.rr_1 and self.change < comms.rr_2:
                        return comms.com_rr_1
                    elif self.change >= comms.rr_2 and self.change < comms.rr_3:
                        return comms.com_rr_2
                    elif self.change >= comms.rr_3 and self.change < comms.rr_4:
                        return comms.com_rr_3
                    elif self.change >= comms.rr_4 and self.change < comms.rr_5:
                        return comms.com_rr_4
                    elif self.change >= comms.rr_5:
                        return comms.com_rr_5
            
    @property
    def get_comm(self):
        # obtener el valor de la comisión según el precio de la venta y el prcjje
        try:
            comm = (self.get_comm_per * self.change)/100
            return comm
        # si la venta es menor a comms.rr_1 retornar 0 comisión
        except:
            return 0
        
    

    UPSELL='Upsell'
    NEW_CLIENT='New Client'
    CROSSSELL = 'Cross Sell'
    NEW = ' - '
    KIND_CHOICES = (
        (UPSELL, ('Upsell')),
        (NEW_CLIENT, ('New Client')),
        (CROSSSELL, ('Cross Sell')),
        (NEW, (' - ')))

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
       
    ARS = "ARS"
    USD = "USD"
    COIN_CHOICES = (
        (ARS, ('ARS')),
        (USD, ('USD')))

    client = models.ForeignKey(Client, related_name='sales', null=True, blank=True, on_delete=models.CASCADE, verbose_name="ACCOUNT")
    
    sales_rep = models.ForeignKey(
                    Employee,
                    related_name='sales',
                    null=True, blank=True,
                    on_delete=models.SET_NULL, verbose_name="SALES REP")
    
    
    kind = models.CharField(max_length=50, choices=KIND_CHOICES, null=True, blank=False, default=None, verbose_name="KIND")
    
    date = models.DateField(default=date.today, verbose_name="DATE")
    
    total = models.IntegerField(blank=True, null=True, verbose_name="TOTAL")
    
    comments =models.CharField(max_length=500, null=True, blank=True, verbose_name="COMMENTS")
    
    
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="SERVICE", blank=False, default=None)
    
    
    note = models.CharField(max_length=400, null=True, blank=True, verbose_name="NOTES")
    cost = models.IntegerField(default=0, verbose_name="COST")
    status = models.CharField(max_length=5, choices=S_CHOICES, null=True, blank=False, default=None, verbose_name="STATUS $")
    change = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12, null=True, blank=True)
    price = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=50, default="ARS", choices=COIN_CHOICES, null=True, blank=False, verbose_name="CURRENCY")
    @property
    def get_change(self):
        change = 0
        if self.currency == "USD":
            change = self.price*Decimal(blue)
            return change
        else:
            return self.price
        
        
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


        if self.suscription is None and self.revenue == "RR":
                    
            self.get_service_or_update()
            

        super(Sale, self).save(*args, **kwargs)

        
    
        
            
      
    
    ################### 
    def get_service_or_update (self, *args, **kwargs):  
                
        try:
            service = Service.objects.get(
                client=self.client, service=self.service) 
               
            if not self.suscription:                
                service.total += Decimal(self.change)
                service.save()     
                self.suscription=service                              
            
        except Service.DoesNotExist:                  
            
            values = {
                "client": self.client,
                "service": self.service,
                "total": self.change,
                }            
            service = Service(**values)
            service.save()  
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
    
    
        
        