from import_export import resources, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from sales.models import Sale, Adj, Service
from customers.models import Client, BackUps, ConfTier, AutoRevenue
from expenses.models import Expense, Employee, Holiday, Salary
from dashboard.models import Comms, LastBlue, Configurations   


        
class CommsResource(resources.ModelResource): 
    
    class Meta:
        model = Comms

        
class LastBlueResource(resources.ModelResource): 
    
    class Meta:
        model = LastBlue

        
class ConfigurationsResource(resources.ModelResource): 
    
    class Meta:
        model = Configurations
        
        
class BackUpsResource(resources.ModelResource): 
    
    class Meta:
        model = BackUps
        


        
class ConfTierResource(resources.ModelResource): 
    
    class Meta:
        model = ConfTier
        


        
class AutoRevenueResource(resources.ModelResource): 
    
    class Meta:
        model = AutoRevenue
        




class SalaryResource(resources.ModelResource):
    
    employee = Field(
        column_name='employee',
        attribute='employee',
        widget=ForeignKeyWidget(model=Employee, field='name'))
    
    
    class Meta:
        model = Salary
        


class HolidayResource(resources.ModelResource):
    
    employee = Field(
        column_name='employee',
        attribute='employee',
        widget=ForeignKeyWidget(model=Employee, field='name'))
    
    
    class Meta:
        model = Holiday
        
            
"""
class SaleResource(resources.ModelResource):
    
    client = Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(model=Client, field='name'))
    
    
    class Meta:
        model = Sale"""
"""
        
class SaleResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
    
    suscription = fields.Field(
        column_name='suscription',
        attribute='suscription',
        widget=ForeignKeyWidget(Service, 'service')
    )
    
    class Meta:
        model = Sale
"""



class ExportSales(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
    
    sales_rep = fields.Field(
        column_name='sales_rep',
        attribute='sales_rep',
        widget=ForeignKeyWidget(Employee, 'name')
    )
    
    class Meta:
        model = Sale
        exclude = ('suscription', 'change', 'id', 'pk', 'total')




class SaleResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
    
    sales_rep = fields.Field(
        column_name='sales_rep',
        attribute='sales_rep',
        widget=ForeignKeyWidget(Employee, 'name')
    )
    
    class Meta:
        model = Sale
        exclude = ('suscription',)



class ServiceResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
    
    class Meta:
        model = Service




class ExportRR(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
   
    class Meta:
        model = Service



class AdjResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
    
    service = fields.Field(
        column_name='service',
        attribute='service',
        widget=ForeignKeyWidget(Service, 'service')
    )
    
    class Meta:
        model = Adj





        
class ClientResource(resources.ModelResource): 
    
    class Meta:
        model = Client
        

        
        
            
class EmployeeResource(resources.ModelResource): 
    
    class Meta:
        model = Employee      
        

            
class ExportCeo(resources.ModelResource): 
    last_salary = fields.Field(attribute='get_salary', column_name='SALARY')
    
    mp = fields.Field(attribute='get_mp', column_name='MP')
    tc = fields.Field(attribute='get_tc', column_name='TC')
    atm = fields.Field(attribute='get_atm', column_name='ATM')
    cash = fields.Field(attribute='get_cash', column_name='CASH')
    usd = fields.Field(attribute='get_cash_usd', column_name='CASH USD')
    paypal = fields.Field(attribute='get_paypal', column_name='PAYPAL')

    monthly_bonus = fields.Field(attribute='get_aguinaldo_mensual', column_name='MONTHLY BONUS')
    
    total =fields.Field(attribute='get_total_ceo', column_name='TOTAL')
    
    
    class Meta:
        model = Employee
        fields = ('name', 'rol', 'dob', 'address', 'email', 'tel', 'date_join', 'active', 'date_gone', 'last_salary', 'mp','tc','atm','cash','usd','paypal','monthly_bonus', 'total')
        
        

    def get_queryset(self):
        # Get the original queryset
        queryset = super().get_queryset()

        # Filter out employees with role="CEO"
        queryset = queryset.filter(rol="CEO")

        return queryset

        
            
class ExportStaff(resources.ModelResource): 
    last_salary = fields.Field(attribute='get_salary', column_name='SALARY')
    white = fields.Field(attribute='get_white', column_name='WHITE')
    tax = fields.Field(attribute='get_social', column_name='TAX')
    nigga = fields.Field(attribute='get_nigga', column_name='NIGGA')
    
    monthly_bonus = fields.Field(attribute='get_aguinaldo_mensual', column_name='MONTHLY BONUS')
    
    total =fields.Field(attribute='get_total', column_name='TOTAL')
    
    
    class Meta:
        model = Employee
        fields = ('name', 'rol', 'dob', 'address', 'email', 'tel', 'date_join', 'active', 'date_gone', 'last_salary', 'white','tax','nigga','monthly_bonus', 'total')
        
        

    def get_queryset(self):
        # Get the original queryset
        queryset = super().get_queryset()

        # Filter out employees with role="CEO"
        queryset = queryset.exclude(rol="CEO")

        return queryset

    
      
        
        
        
class ExpenseResource(resources.ModelResource): 
    
    class Meta:
        model = Expense