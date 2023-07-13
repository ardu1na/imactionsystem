from datetime import date
from decimal import Decimal

from django.db import models

from dashboard.models import LastBlue



last_blue = 0
try:
    last_blue =  LastBlue.objects.get(pk=1)
    blue = last_blue.venta

except:
    blue = 0






class Salary (models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="EMPLOYEE", related_name="salaries")
    
    period = models.DateField(default=date.today)
    
    salary = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="SALARY")
    
    nigga = models.DecimalField(default= 0, max_digits=50, decimal_places=25, null=True, blank=True, verbose_name="NIGGA %")
    
    mp = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="MP")
    tc = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="TC")
    cash = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="CASH $")

    atm_cash = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="ATM CASH")
    cash_usd = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="CASH USD")
    paypal = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="PAYPAL")
    
    raice = models.DecimalField(default= 0, max_digits=50, decimal_places=2, null=True, blank=True, verbose_name="RAICE")
    
    
    def __str__ (self):
        return '{} salary'.format(self.employee) 
    
    
    class Meta:
        get_latest_by = ['-period']
        ordering = ['-period']

        
        
        
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
    
    dob = models.DateField(null=True, blank=True)
    
    address = models.CharField(max_length=250, verbose_name="ADDRESS", blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="EMAIL")
    tel = models.CharField(max_length=40, blank=True, null=True, verbose_name="PHONE")
    
    date_join = models.DateField(default=date.today, verbose_name="JOIN")
    active = models.CharField(max_length=15, choices=ACT_CHOICES, blank= False, verbose_name="ACTIVE?", default="Yes")
    date_gone = models.DateField(null=True, blank=True, verbose_name="GONE")
    
    
    def get_salary (self):
        if self.rol == "CEO":
            wages  = Salary.objects.filter(employee=self.pk).first()
        else: 
            wages  = Salary.objects.filter(employee=self.pk).latest() 

        s = wages.salary 
        return s
    
    def get_nigga_per(self):
        ni = Salary.objects.filter(employee=self.pk).latest() 

        s = ni.nigga 
        return s    
    
    def get_white (self):
        wages  = Salary.objects.filter(employee=self.pk).latest() 

        white = wages.salary - (wages.salary*(wages.nigga/100))
        return white
    
    def get_nigga (self):
        wages  = Salary.objects.filter(employee=self.pk).latest() 

        n = (wages.salary*(wages.nigga/100))
        return n
    
    def get_social (self):
        social = self.get_white()/2
        return social
    
    
    
    
    def get_paypal (self):
        wages  = Salary.objects.filter(employee=self.pk).first() 

        p_c = wages.paypal*Decimal(blue)
        return p_c
    
    def get_mp(self):
        wages  = Salary.objects.filter(employee=self.pk).first() 
        i = wages.mp
        return i 
    
    def get_atm(self):
        wages  = Salary.objects.filter(employee=self.pk).first() 
        i = wages.atm_cash
        return i 
    
    def get_tc(self):
        wages  = Salary.objects.filter(employee=self.pk).first() 
        i = wages.tc
        return i 
    
    
    def get_cash(self):
        wages  = Salary.objects.filter(employee=self.pk).first() 
        i = wages.cash
        return i 
    
    def get_cash_usd (self):
        wages  = Salary.objects.filter(employee=self.pk).first() 

        c = wages.cash_usd*Decimal(blue)
        return c
    
    
    def get_total (self):
        total = self.get_white() + self.get_social() + self.get_nigga()
        return total
    
    def get_total_ceo (self):
        wages  = Salary.objects.filter(employee=self.pk).first() 

        total = wages.salary + wages.mp + wages.atm_cash + wages.cash + wages.tc + self.get_paypal() + self.get_cash_usd()
        return total
    
    def get_aguinaldo_mensual (self):
        

        if self.rol == "CEO":
            wages  = Salary.objects.filter(employee=self.pk).first() 
            month = wages.salary/12
        else:
            wages  = Salary.objects.filter(employee=self.pk).latest() 
            month = self.get_total()/12
        return month
    
   
    
    def __str__ (self):
        return self.name
    
    
    
    
    
    
class Holiday (models.Model):
    JAN = 'January'
    FEB = 'February'
    MAR = 'March'
    APR = 'April'
    MAY = 'May'
    JUN = 'June'
    JUL = 'July'
    AUG = 'August'
    SEP = 'September'
    OCT = 'October'
    NOV = 'November'
    DEC = 'December'
    MONTH_CHOICES = (
        (JAN, ('January')),
        (FEB, ('February')),
        (MAR, ('March')),
        (APR, ('April')),
        (MAY, ('May')),
        (JUN, ('June')),
        (JUL, ('July')),
        (AUG, ('August')),
        (SEP, ('September')),
        (OCT, ('October')),
        (NOV, ('November')),
        (DEC, ('December')),       
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="EMPLOYEE", related_name="holidays")
    year = models.IntegerField(verbose_name="YEAR", null=True, blank= True)
    
    month = models.CharField(choices=MONTH_CHOICES, max_length=150, null=True, blank= False, default=None, verbose_name="MONTH")
    
    days = models.SmallIntegerField(verbose_name="WORKING DAYS", null=True, blank= True)
    date_start = models.DateField(null=True, blank= True)
    date_end = models.DateField(null=True, blank= True)
    
    def __str__ (self):
        return '{} {} {} holidays'.format(self.employee, self.month, self.year)       


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
    
    
    ARS = "ARS"
    USD = "USD"
    COIN_CHOICES = (
        (ARS, ('ARS')),
        (USD, ('USD')))
    
    currency = models.CharField(max_length=50, default="ARS", choices=COIN_CHOICES, null=True, blank=False, verbose_name="CURRENCY")

    change = models.DecimalField(default=0, verbose_name="PRICE", decimal_places=2, max_digits=12, null=True, blank=True)

    @property
    def get_change(self):
        change = 0
        if self.currency == "USD":
            change = self.value*Decimal(blue)
            return change
        else:
            return self.value
        
    wop = models.CharField(max_length=80, default=None, blank= False, choices=WOP_CHOICES, verbose_name="WOP")

    def __str__ (self):
        return '{} / {}: ${}'.format(self.category, self.concept, self.value)


    class Meta:
        ordering = ['-date']
        
    
    
    def save(self, *args, **kwargs):                                    

        self.change = self.get_change         

        super(Expense, self).save(*args, **kwargs)