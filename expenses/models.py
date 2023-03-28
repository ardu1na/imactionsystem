from datetime import date
from decimal import Decimal

from django.db import models

from sales.models import LastBlue

last_blue = LastBlue.objects.get(pk=1)
blue = (last_blue.venta+last_blue.compra)/2




class Employee(models.Model):
    SEO = 'SEO'
    GADS = 'GADS'
    FADS = 'FADS'
    DESIGN = 'Design'
    ADMIN = 'Admin'
    SALES = 'Sales'
    OTHERS = 'Others'
    CEO = 'CEO'
    ROL_CHOICES = (
        (SEO, ('SEO')),
        (GADS, ('GADS')),
        (FADS, ('FADS')),
        (DESIGN, ('Design')),
        (ADMIN, ('Admin')),
        (SALES, ('Sales')),
        (OTHERS, ('Others')),
        (CEO, ('CEO')),)

    

    ACTIVE = 'Yes'
    GONE = 'No'
    ACT_CHOICES = (
        (ACTIVE, ('Yes')),
        (GONE, ('No')),)
    
    
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, blank=False, null=True,  verbose_name="ROL", default=None)
    
    name = models.CharField(max_length=150, verbose_name="NAME")
    
    address = models.CharField(max_length=250, verbose_name="ADDRESS", blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="EMAIL")
    tel = models.CharField(max_length=40, blank=True, null=True, verbose_name="PHONE")
    
    date_join = models.DateField(default=date.today, verbose_name="JOIN")
    active = models.CharField(max_length=15, choices=ACT_CHOICES, blank= False, verbose_name="ACTIVE?", default="Yes")
    date_gone = models.DateField(null=True, blank=True, verbose_name="GONE")
    
    salary = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="SALARY")
    
    nigga = models.DecimalField(default= 0, max_digits=50, decimal_places=25, null=True, blank=True, verbose_name="NIGGA %")
    
    mp = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="MP")
    tc = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="TC")
    cash = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="CASH $")

    atm_cash = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="ATM CASH")
    cash_usd = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="CASH USD")
    paypal = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="PAYPAL")
    
    
    @property
    def get_white (self):
        white = self.salary - (self.salary*(self.nigga/100))
        return white
    
    @property
    def get_nigga (self):
        nigga = (self.salary*(self.nigga/100))
        return nigga
    
    @property
    def get_social (self):
        social = self.get_white/2
        return social
    
    @property
    def get_total (self):
        total = self.get_white + self.get_social + self.get_nigga
        return total
    
    
    @property
    def get_paypal (self):
        p_c = self.paypal*Decimal(blue)
        return p_c
    
    
    
    @property
    def get_cash_usd (self):
        c = self.cash_usd*Decimal(blue)
        return c
    
    
    @property
    def get_total_ceo (self):
        total = self.salary + self.mp + self.atm_cash + self.cash + self.tc + self.get_paypal + self.get_cash_usd
        return total
    
    @property
    def get_aguinaldo_mensual (self):
        if self.rol == "CEO":
            month = self.salary/12
        else:
            month = self.get_total/12
        return month
    
    
    
   
    
    def __str__ (self):
        return self.name
    
    
    


class Expense(models.Model):
    
    DEBIT = 'Debit'
    BANK_TRANSFER = 'Bank transfer'
    VARIOUS = 'Various'
    CASH = 'Cash'
    BALANCE = "Balance"
    TC = "TC"

    WOP_CHOICES = (
    (DEBIT, ('Debit')),
    (BANK_TRANSFER, ('Bank transfer')),
    (VARIOUS, ('Various')),
    (CASH, ('Cash')),
    (BALANCE, ('Balance')),
    (TC, ('TC')),
    )

    EMPRESA = 'Empresa'
    LEAD_GEN = 'Lead Gen'
    OFFICE = 'Office'
    OTHER = 'Other'
    TAX = 'Tax'

    EXP_CHOICES = (
        (EMPRESA, ('Empresa')),
        (LEAD_GEN, ('Lead Gen')),
        (OFFICE, ('Office')),
        (OTHER, ('Other')),
        (TAX, ('Tax')),
        )
    
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=80, default=None, choices=EXP_CHOICES, blank=False, verbose_name="CATEGORY")
    concept = models.CharField(max_length=150, verbose_name="CONCEPT", blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=15, blank= True, null= True, verbose_name="VALUE")
    wop = models.CharField(max_length=80, default=None, blank= False, choices=WOP_CHOICES, verbose_name="WOP")

    def __str__ (self):
        return '{}/{}: ${}'.format(self.category, self.concept, self.value)

