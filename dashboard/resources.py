from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from sales.models import Sale
from customers.models import Client, BankData
from expenses.models import Expense, Employee
   
    

class SaleResource(resources.ModelResource):
    
    client = Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(model=Client, field='name'))
    
    
    class Meta:
        model = Sale
        
        
class ClientResource(resources.ModelResource): 
    
    class Meta:
        model = Client
        
class BankResource(resources.ModelResource): 
    account = Field(
        column_name='account',
        attribute='account',
        widget=ForeignKeyWidget(model=Client, field='name'))
    
    class Meta:
        model = BankData     
        
        
        
class EmployeeResource(resources.ModelResource): 
    
    class Meta:
        model = Employee      
        
        
        
class ExpenseResource(resources.ModelResource): 
    
    class Meta:
        model = Expense