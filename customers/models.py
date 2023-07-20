from datetime import date
from django.db import models
from dashboard.models import ConfTier


class Client(models.Model):
    
    @property
    def get_service(self, service):
        try:
            service = self.services.get(service=service)
        except:
            service = None
        return service
    
    
    
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


    CASH='Cash'
    CBU='CBU'
    MP_IM='MP Imactions'
    MP_P='MP Personal'
    BANK_TRANSFER='Bank Transfer'
    PAYPAL='PayPal'

    WOP_CHOICES=(
        (CASH, ('Cash')),
        (CBU, ('CBU')),
        (MP_IM, ('MP Imactions')),
        (MP_P, ('MP Personal')),
        (BANK_TRANSFER, ('Bank Transfer')),
        (PAYPAL, ('PayPal')),

    )

    name = models.CharField(max_length=150, unique=True)
    business_name = models.CharField(max_length=150, blank=True, null=True)
    cuit = models.CharField(max_length=80, blank=True, null=True, verbose_name="CUIT")
    source = models.CharField(max_length=50, choices=CANAL_CHOICES, null=True, blank=False, default=None)
    date = models.DateField(editable=True, default=date.today)
    website = models.URLField(blank=True, null=True)
    
    wop = models.CharField(max_length=150, choices=WOP_CHOICES, null=True, blank=False, verbose_name='WOP', default=None)
    
    
    # new contact data
    c1_name = models.CharField(max_length=150, blank=True, null=True)
    c1_email = models.EmailField(blank=True, null=True)
    c1_email2 = models.EmailField(blank=True, null=True)
    c1_tel = models.CharField(max_length=150, blank=True, null=True)
    c1_tel2 = models.CharField(max_length=150, blank=True, null=True)
    
    c2_name = models.CharField(max_length=150, blank=True, null=True)
    c2_email = models.EmailField(blank=True, null=True)
    c2_email2 = models.EmailField(blank=True, null=True)
    c2_tel = models.CharField(max_length=150, blank=True, null=True)
    c2_tel2 = models.CharField(max_length=150, blank=True, null=True)
    admin_name = models.CharField(max_length=150, blank=True, null=True)
    admin_email = models.EmailField(blank=True, null=True)
    admin_email2 = models.EmailField(blank=True, null=True)
    admin_tel = models.CharField(max_length=150, blank=True, null=True)
    admin_tel2 = models.CharField(max_length=150, blank=True, null=True)
    
    landing_page = models.URLField(blank=True, null=True)



    cancelled = models.CharField(default='Active', max_length=51, choices=CANCELLED_CHOICES, blank=True)
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
    fail_can = models.CharField(max_length=50, choices=FAIL_CHOICES, blank=False, default= None, null=True, verbose_name="DO WE FAIL?")
    
    def __str__(self):
       return str(self.name)


    # get the TIER in base of range of RR sales
    # the params comes from ConfTier Model defined above
    @property
    def tier(self):
        
        if self.total_rr <= ConfTier.objects.get(pk=1).tier_iv:
            return "IV"
        elif self.total_rr <= ConfTier.objects.get(pk=1).tier_iii:
            return "III"
        elif self.total_rr <= ConfTier.objects.get(pk=1).tier_ii:
            return "II"
        elif self.total_rr > ConfTier.objects.get(pk=1).tier_i:
            return "I"
        else:
            return "V"
   
   
    def save(self, *args, **kwargs):
        if self.cancelled == "Cancelled":
            for service in self.services.all():
                service.state = False
                service.save()   
        
        super(Client, self).save(*args, **kwargs)
            
            
            

    @property
    def get_date(self):
        formatdate = self.date.strftime('%d/%m/%Y')
        return formatdate
    
    @property
    def get_date_can(self):
        formatdate = self.date_can.strftime('%d/%m/%Y')
        return formatdate       
  
    @property
    def get_rr_client(self):
        rr_client = False
        if self.services:
            rr_client = True
        return rr_client

    @property
    def total_rr(self):
        total = 0
        for service in self.services.filter(state=True):
                total += service.total
        return total


    @property
    def rr(self): 
        total = 0
        if self.cancelled =="Active":
            for sale in self.services.filter(state=True):
                        total += sale.total
        return '${:,.2f}'.format(total)

    



    ##########
    ### in the func below we get
    ### all sales objects of each rr service
    ### it should be MORE DRY i know
    
    @property
    def other_rr_sales(self, *args, **kwargs):
        other = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="Others RR").exclude(note="auto revenue sale"):
                other.append(sale)
        if len(other) > 0:
            return other
        else:
            return None
    
    @property
    def seo_sales(self, *args, **kwargs):
        seo = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="SEO").exclude(note="auto revenue sale"):
                seo.append(sale)
        if len(seo) > 0:
            return seo
        else:
            return None
        
    @property
    def gads_sales(self, *args, **kwargs):
        gads = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="Google Ads").exclude(note="auto revenue sale"):
                gads.append(sale)
        if len(gads) > 0:
            return gads
        else:
            return None
        
        
    @property
    def combo_sales(self, *args, **kwargs):
        combo = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="Combo").exclude(note="auto revenue sale"):
                combo.append(sale)
        if len(combo) > 0:
            return combo
        else:
            return None
        
    @property
    def fads_sales(self, *args, **kwargs):
        fads = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="Facebook Ads").exclude(note="auto revenue sale"):
                fads.append(sale)
        if len(fads) > 0:
            return fads
        else:
            return None
        
        
        
    @property
    def lin_sales(self, *args, **kwargs):
        lin = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="LinkedIn").exclude(note="auto revenue sale"):
                lin.append(sale)
        if len(lin) > 0:
            return lin
        else:
            return None
        
    @property 
    def cm_sales(self, *args, **kwargs):
        cm = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="Community Management").exclude(note="auto revenue sale"):
                cm.append(sale)
        if len(cm) > 0:
            return cm
        else:
            return None
        
    @property
    def wp_sales(self, *args, **kwargs):
        wp = []
        if self.cancelled == "Active":
            for sale in self.sales.filter(revenue="RR", cancelled="Active", service="Web Plan").exclude(note="auto revenue sale"):
                wp.append(sale)
        if len(wp) > 0:
            return wp
        else:
            return None
    
    ##########


    
        
        
        
    @property
    def get_other(self, *args, **kwargs):
        other_total=0
        if self.cancelled == "Active":
            for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
                if sale.service == "Others RR":
                    if sale.cancelled == "Active":
                        other_total += sale.get_change
        return '${:,.2f}'.format(other_total)
    
    @property
    def get_seo(self, *args, **kwargs):
        seo_total=0
        if self.cancelled == "Active":
            for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
                if sale.service == "SEO":
                    if sale.cancelled == "Active":
                        seo_total += sale.get_change
        return '${:,.2f}'.format(seo_total)
    @property
    def get_gads(self, *args, **kwargs):
        gads_total=0
        for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
            if self.cancelled == "Active":
                if sale.service == "Google Ads":
                   if sale.cancelled == "Active":
                        gads_total += sale.get_change
        return '${:,.2f}'.format(gads_total)
    @property
    def get_combo(self, *args, **kwargs):
        combo_total=0
        for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
            if self.cancelled == "Active":
                if sale.service == "Combo":
                    if sale.cancelled == "Active":
                        combo_total += sale.get_change
        return '${:,.2f}'.format(combo_total)
    @property
    def get_fads(self, *args, **kwargs):
        fads_total=0
        for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
            if self.cancelled == "Active":
                if sale.service == "Facebook Ads":
                    if sale.cancelled == "Active":
                        fads_total += sale.get_change
        return '${:,.2f}'.format(fads_total)
    @property
    def get_lnkd(self, *args, **kwargs):
        lnkd_total=0
        for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
            if self.cancelled == "Active":
                if sale.service == "LinkedIn":
                    if sale.cancelled == "Active":
                        lnkd_total += sale.get_change
        return '${:,.2f}'.format(lnkd_total)
    @property
    def get_cm(self, *args, **kwargs):
        cm_total=0
        for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
            if self.cancelled == "Active":
                if sale.service == "Community Management":
                    if sale.cancelled == "Active":
                        cm_total += sale.get_change
        return '${:,.2f}'.format(cm_total)
    @property
    def get_wp(self, *args, **kwargs):
        wp_total=0
        for sale in self.sales.filter(date__month=date.today().month, date__year=date.today().year):
            if self.cancelled == "Active":
                if sale.service == "Web Plan":
                    if sale.cancelled == "Active":
                        wp_total += sale.get_change
        return '${:,.2f}'.format(wp_total)
    
    
    @property        
    def seo(self):
        for service in self.services.filter(state=True):
            if service.service == "SEO":
                return service
                
        
    @property        
    def gads(self):
        for service in self.services.filter(state=True):
            if service.service == "Google Ads":
                return service
        
    @property        
    def fads(self):
        for service in self.services.filter(state=True):
            if service.service == "Facebook Ads":
                return service
    
    @property        
    def linkd(self):
        for service in self.services.filter(state=True):
            if service.service == "LinkedIn":
                return service
        
    @property        
    def wp(self):
        for service in self.services.filter(state=True):
            if service.service == "Web Plan":
                return service
            
    @property        
    def combo(self):
        for service in self.services.filter(state=True):
            if service.service == "Combo":
                return service

    @property    
    def cm(self):
        for service in self.services.filter(state=True):
            if service.service == "Community Management":
                return service    
        
    @property        
    def emkg(self):
        for service in self.services.filter(state=True):
            if service.service == "Email Marketing":
                return service    
        
        
    @property        
    def otherr(self):
        for service in self.services.filter(state=True):
            if service.service == "Others RR":
                return service 
                
                

    


    
    
    
        
        
        
        
        
        
        
### This manager is for the admin panel, clients list view.
# # in order to just show active clients
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
        
        
        
        


