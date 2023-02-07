from datetime import date

from django.db import models


class Employee(models.Model):
    STAFF = 'Staff'
    CEO = 'CEO'
    ROL_CHOICES = (
        (STAFF, ('Staff')),
        (CEO, ('CEO')),)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, verbose_name="ROL", default="Staff")
    
    name = models.CharField(max_length=150, verbose_name="NAME")
    
    address = models.CharField(max_length=250, verbose_name="ADDRESS", blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="EMAIL")
    tel = models.CharField(max_length=40, blank=True, null=True, verbose_name="PHONE")
    
    date_join = models.DateField(default=date.today, verbose_name="JOIN")
    active = models.BooleanField(default=True, verbose_name="ACTIVE?")
    date_gone = models.DateField(null=True, blank=True, verbose_name="GONE")
    
    white = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="SALARY")
    nigga = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="NIGGA")
    
    mp = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="MP")
    tc = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="TC")
    atm_cash = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="ATM CASH")
    
    

    def __str__ (self):
        return self.name
    
    @property
    def get_social(self):
        return self.white/2
    
    @property
    def get_aguinaldo(self):
        aguinaldo = self.white + self.nigga + self.get_social
        return aguinaldo
    
    @property
    def get_aguinaldo_mensual(self):
        aguinaldo = self.white + self.nigga + self.get_social
        return aguinaldo/12
    
    


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
    WAGES = "Wages"
    NIGGA = "Nigga"

    EXP_CHOICES = (
        (EMPRESA, ('Empresa')),
        (LEAD_GEN, ('Lead Gen')),
        (OFFICE, ('Office')),
        (OTHER, ('Other')),
        (TAX, ('Tax')),
        (WAGES, ('Wages')),
        (NIGGA, ('Nigga'))
        )
    
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=80, default="Other", choices=EXP_CHOICES, verbose_name="CATEGORY")
    concept = models.CharField(max_length=150, verbose_name="CONCEPT", blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=15, blank= True, null= True, verbose_name="VALUE")
    wop = models.CharField(max_length=80, default="Various", choices=WOP_CHOICES, verbose_name="WOP")

    def __str__ (self):
        return '{}/{}: ${}'.format(self.category, self.concept, self.value)

