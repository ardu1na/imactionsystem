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
<<<<<<< HEAD
        exclude = ('suscription',)






class ServiceResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
    )
    
    class Meta:
        model = Service






=======
"""

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
        
        
        
class ExpenseResource(resources.ModelResource): 
    
    class Meta:
        model = Expense
