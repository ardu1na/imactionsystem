from datetime import date

from django.db import models


class Expense(models.Model):

    EMPRESA = 'Empresa'
    LEAD_GEN = 'Lead Gen'
    OFFICE = 'Office'
    OTHER = 'Other'
    TAX = 'Tax'
    WAGES = "Wages"

    EXP_CHOICES = (
        (EMPRESA, ('Empresa')),
        (LEAD_GEN, ('Lead Gen')),
        (OFFICE, ('Office')),
        (OTHER, ('Other')),
        (TAX, ('Tax')),
        (WAGES, ('Wages')),
        )


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
    
    category = models.CharField(max_length=80, default="Other", choices=EXP_CHOICES, verbose_name="CATEGORY")
    concept = models.CharField(max_length=150, verbose_name="CONCEPT")
    value = models.DecimalField(decimal_places=2, max_digits=15, blank= True, null= True, verbose_name="VALUE")
    wop = models.CharField(max_length=80, default="Various", choices=WOP_CHOICES, verbose_name="WOP")
    date = models.DateField(default=date.today)

    def __str__ (self):
        return '{}: ${}'.format(self.category, self.value)





class Employee(models.Model):
    name = models.CharField(max_length=150, verbose_name="NAME")
    address = models.CharField(max_length=250, verbose_name="ADDRESS", blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="EMAIL")
    tel = models.CharField(max_length=40, blank=True, null=True, verbose_name="PHONE")
    date_join = models.DateField(default=date.today)
    active = models.BooleanField(default=True)
    
    def __str__ (self):
        return self.name

    

    
    
    
    
    

class Salary(models.Model):
   
    expense = models.OneToOneField(
        Expense, on_delete=models.CASCADE,
        blank=True, null=True)

    employee = models.ForeignKey(
        Employee, related_name="salaries",
        on_delete=models.CASCADE,
        verbose_name="EMPLOYEE")
    
    white = models.DecimalField(
        decimal_places=2, max_digits=15,
        null=True, blank=True,
        verbose_name="WHITE",
        default=0)
    
    nigga = models.DecimalField(
        decimal_places=2, max_digits=15,
        null=True, blank=True,
        verbose_name="NIGGA",
        default=0)
    
    aguinaldo_mensual = models.DecimalField(
        decimal_places=2, max_digits=15,
        null=True,
        blank=True,
        verbose_name="AGUINALDO MENSUAL")
    
    
    
    def get_social(self):
        return self.white/2
    
    def get_aguinaldo_mensual(self):
        aguinaldo = self.white + self.nigga + self.get_social
        return aguinaldo/12
    
    
    def save(self, *args, **kwargs):
        self.aguinaldo_mensual = self.get_aguinaldo_mensual
        super(Salary, self).save(*args, **kwargs)
        

    def __str__ (self):
        return '{} {}'.format(self.employee, self.expense.date)