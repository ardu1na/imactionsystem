from datetime import date
from django.db import models
from django.contrib import admin



class BackUps(models.Model):
    date = models.DateField(auto_now=True)
    
     
       
# SETTINGS
# # let the user change variables of model method definitions
class ConfTier(models.Model):
    tier_v = models.IntegerField(default=30000)
    tier_iv = models.IntegerField(default=65000)
    tier_iii = models.IntegerField(default=110000)
    tier_ii = models.IntegerField(default=200000)
    tier_i = models.IntegerField(default=200000)




class Client(models.Model):
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

    name = models.CharField(max_length=150)
    business_name = models.CharField(max_length=150, blank=True, null=True)
    source = models.CharField(max_length=50, choices=CANAL_CHOICES, null=True, blank=True)
    date = models.DateField(editable=True, default=date.today)
    website = models.URLField(blank=True, null=True)
    
    wop = models.CharField(max_length=150, choices=WOP_CHOICES, null=True, blank=True, verbose_name='WOP')
    
    
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



    cancelled = models.CharField(default='Active', max_length=51, choices=CANCELLED_CHOICES)
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
    
    def __str__(self):
       return str(self.name)


    # get the TIER in base of range of RR sales
    # the params comes from ConfTier Model defined above
    @property
    def tier(self):
        if self.total_rr <= ConfTier.objects.get(pk=1).tier_v:
            return "V"
        elif self.total_rr <= ConfTier.objects.get(pk=1).tier_iv:
            return "IV"
        elif self.total_rr <= ConfTier.objects.get(pk=1).tier_iii:
            return "III"
        elif self.total_rr <= ConfTier.objects.get(pk=1).tier_ii:
            return "II"
        elif self.total_rr > ConfTier.objects.get(pk=1).tier_i:
            return "I"
   

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
        if self.sales:
            for sale in self.sales.all():
                if sale.revenue == "RR" and sale.cancelled == "Active":
                    rr_client = True
        return rr_client

    @property
    def total_rr(self):
        total = 0
        for sale in self.sales.all():
            if sale.revenue == "RR" and sale.cancelled == "Active":
                total += sale.get_change
        return total

    @property
    @admin.display(description="RR")
    def rr(self):
        total = 0
        if self.cancelled =="Active":
            for sale in self.sales.all():
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total += sale.get_change
        return '${:.2f}'.format(total)

    



    ##########
    ### in the func below we get
    ### the total sales of each rr service
    ### it should be MORE DRY i know
    
    @property
    def get_other(self, *args, **kwargs):
        other_total=0
        if self.cancelled == "Active":
            for sale in self.sales.all():
                if sale.service == "Other RR":
                    if sale.cancelled == "Active":
                        other_total += sale.get_change
        return '${:.2f}'.format(other_total)
    
    @property
    def get_seo(self, *args, **kwargs):
        seo_total=0
        if self.cancelled == "Active":
            for sale in self.sales.all():
                if sale.service == "SEO":
                    if sale.cancelled == "Active":
                        seo_total += sale.get_change
        return '${:.2f}'.format(seo_total)
    @property
    def get_gads(self, *args, **kwargs):
        gads_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Google Ads":
                   if sale.cancelled == "Active":
                        gads_total += sale.get_change
        return '${:.2f}'.format(gads_total)
    @property
    def get_combo(self, *args, **kwargs):
        combo_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "COMBO":
                    if sale.cancelled == "Active":
                        combo_total += sale.get_change
        return '${:.2f}'.format(combo_total)
    @property
    def get_fads(self, *args, **kwargs):
        fads_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Facebook Ads":
                    if sale.cancelled == "Active":
                        fads_total += sale.get_change
        return '${:.2f}'.format(fads_total)
    @property
    def get_lnkd(self, *args, **kwargs):
        lnkd_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "LinkedIn":
                    if sale.cancelled == "Active":
                        lnkd_total += sale.get_change
        return '${:.2f}'.format(lnkd_total)
    @property
    def get_cm(self, *args, **kwargs):
        cm_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Community Management":
                    if sale.cancelled == "Active":
                        cm_total += sale.get_change
        return '${:.2f}'.format(cm_total)
    @property
    def get_wp(self, *args, **kwargs):
        wp_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "Web Plan":
                    if sale.cancelled == "Active":
                        wp_total += sale.get_change
        return '${:.2f}'.format(wp_total)
    @property
    def get_combo(self, *args, **kwargs):
        combo_total=0
        for sale in self.sales.all():
            if self.cancelled == "Active":
                if sale.service == "COMBO":
                    if sale.cancelled == "Active":
                        combo_total += sale.get_change
        return '${:.2f}'.format(combo_total)
    ##########


    
        
        
        
        


        
        
        
        
        
        
        
        
        
        
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
        
        
        
        


