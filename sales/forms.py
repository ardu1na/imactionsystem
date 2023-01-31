from django.forms import ModelForm, \
TextInput, Select, ModelChoiceField, Textarea

from sales.models import Sale
from customers.models import Client


class SaleForm(ModelForm):
    
    client = ModelChoiceField(queryset=Client.objects.all(), widget=Select(attrs={'class':"form-select",
            'id':"client",
            'placeholder':"client",}))

    
    class Meta:
        model = Sale
        
        exclude = ['sale_id', 'cancelled', 'date', 'comment_can', 'date_can', 'fail_can', 'revenue']
        
        
        
        widgets = {


            'kind' : Select(attrs={'class':"form-select",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"form-select",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Note"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"form-select",
                'id':"status",
                'placeholder' : "Status"
                }
            ),

        }



class ClientSaleForm(ModelForm):
    
    
    
    
    class Meta:
        model = Sale
        
        exclude = ['id', 'cancelled', 'date', 'comment_can', 'date_can', 'fail_can', 'revenue', 'client']
        
        
        
        widgets = {
            
            
            

            'kind' : Select(attrs={'class':"form-select",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"form-select",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Note"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"form-select",
                'id':"status",
                'placeholder' : "Status"
                }
            ),

        }


class EditSaleForm(ModelForm):
    
        
    class Meta:
        model = Sale
        
        exclude = ['id', 'date', 'date_can', 'revenue', 'client']
        
        
        
        widgets = {


            'kind' : Select(attrs={'class':"form-select",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"form-select",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Note"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"form-select",
                'id':"status",
                'placeholder' : "Status"
                }
            ),
            
            'cancelled' : Select(attrs={
                'class':"form-select",
            'id':"cancelled",
            'placeholder':"Cancelled?",}),
            
            
            'fail_can' : Select(attrs={
                'class':"form-select",
            'id':"fail_can",
            'placeholder':"Do we fail?",}),
            
            'comment_can' : Textarea(attrs={
                'class':"form-control",
                'id':"comment_can",
                'placeholder' : "Comment"
                }
            ),

        }
