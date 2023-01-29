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
    
    def __str__ (self):
        return self.name

    

    

class Salary(models.Model):
    NIGGA = 'Nigga'
    WHITE = 'White'

    WAGES_CHOICES = (
        (NIGGA, ('Nigga')),
        (WHITE, ('White')),
        )

    employee = models.ForeignKey(Employee, related_name="salarys", on_delete=models.CASCADE, verbose_name="EMPLOYEE")
    kind = models.CharField(choices= WAGES_CHOICES, default='White', max_length=50, verbose_name="KIND")
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE, blank=True, null=True)

    def __str__ (self):
        return str(self.expense.value)