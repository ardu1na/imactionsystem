from django.db import models
from datetime import date


class AutoRevenue(models.Model):
    date = models.DateField(default=date.today, editable=True)
    sales = models.BooleanField(default=False, null=True, blank=True)
    expenses = models.BooleanField(default=False, null=True, blank=True)
    wages = models.BooleanField(default=False, null=True, blank=True)
    
     
       
# SETTINGS
# # let the user change variables of model method definitions
class ConfTier(models.Model):
    tier_v = models.IntegerField(default=30000)
    tier_iv = models.IntegerField(default=65000)
    tier_iii = models.IntegerField(default=110000)
    tier_ii = models.IntegerField(default=200000)
    tier_i = models.IntegerField(default=200000)




class BackUps(models.Model):
    date = models.DateField(default=date.today)
    

class LastBlue (models.Model):
    venta = models.DecimalField(
                max_digits=15, decimal_places=2
                                 )
    date_updated = models.DateTimeField(auto_now=True)
    
    @property
    def get_blue(self):
        return self.venta
    
    
    
    
    
    
class Comms (models.Model):
    
    com_rr_1 = models.DecimalField(
                max_digits=15, decimal_places=2,
                default=1
                                 )
    rr_1 = models.IntegerField(
                default=1)

    com_rr_2 = models.DecimalField(
                max_digits=15, decimal_places=2,
                default=1
                                 )
    rr_2 = models.IntegerField(
                default=1)
    
    
    com_rr_3 = models.DecimalField(
                default=1,
                max_digits=15, decimal_places=2
                                 )
    rr_3 = models.IntegerField(
                default=1)
    com_rr_4 = models.DecimalField(
                max_digits=15, decimal_places=2,
                default=1
                                 )
    rr_4 = models.IntegerField(
                default=1)
    com_rr_5 = models.DecimalField(
                max_digits=15, decimal_places=2,
                default=1
                                 )
    rr_5 = models.IntegerField(
                default=1)
    
    up_sell = models.DecimalField(
                max_digits=15, decimal_places=2,
                default=1
                                 )
    one_off = models.DecimalField(
                max_digits=15, decimal_places=2,
                default=1
                                 )
    
    def __str__ (self):
        return "COMMS config"
    
    

class Configurations(models.Model):
    INPUT_TYPE_CHOICES = (
        ('','Select InputType'),
        ('text','text'),
        ('textarea','textarea'),
        ('file','file'),
        ('checkbox','checkbox'),
        ('radio','radio'),
        ('button','button'),
        ('select','select'),
    )
    name = models.CharField(max_length=255,null=True)
    value = models.CharField(max_length=255, null=True,blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    input_type = models.CharField(max_length=255,choices=INPUT_TYPE_CHOICES, default=INPUT_TYPE_CHOICES[0][0])
    editable = models.BooleanField(default=True)
    order=models.IntegerField(null=True,blank=True)
    params =  models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True) #Automatically set the field to now when the object is first created.
    updated_at = models.DateTimeField(auto_now=True) #Automatically set the field to now every time the object is saved.
    class Meta:
        verbose_name = "configuration"
        verbose_name_plural = "configurations"
    def __str__(self):
        return f'{self.name}'
    



    


