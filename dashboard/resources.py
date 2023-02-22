from import_export import resources
from sales.models import Sale
from customers.models import Client
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

   
    

class SaleResource(resources.ModelResource):
    
    client = Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(model=Client, field='name'))
    
    
    class Meta:
        model = Sale