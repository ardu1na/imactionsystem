from import_export import resources, fields, widgets
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from sales.models import Sale, Adj, Service
from customers.models import Client
from expenses.models import Expense, Employee, Holiday, Salary
   

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

class SaleResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'name')
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