from django.forms import ModelForm, \
TextInput, Select, ModelChoiceField, Textarea

from sales.models import Sale, Client


class SaleForm(ModelForm):
    
    account = ModelChoiceField(queryset=Client.objects.all(), widget=Select(attrs={'class':"form-select",
            'id':"account",
            'placeholder':"Account",}))

    
    class Meta:
        model = Sale
        
        exclude = ['id_sale', 'cancelled', 'date', 'comment_can', 'date_can', 'fail_can', 'revenue']
        
        
        
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
    
    id_account = TextInput(attrs={'class':'form-control', 'hidden':'true'})

    
    class Meta:
        model = Sale
        
        exclude = ['id_sale', 'cancelled', 'date', 'comment_can', 'date_can', 'fail_can', 'revenue']
        
        
        
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
        
        exclude = ['id_sale', 'date', 'date_can', 'revenue']
        
        
        
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
