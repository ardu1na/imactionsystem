from django.forms import ModelForm, \
TextInput, Select, ModelChoiceField, Textarea
from django import forms

from sales.models import Sale, Service, Adj 
from customers.models import Client


class AdjustmentForm(ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Service
        fields = ['last_adj', 'adj_at']
        
        
        widgets = {
            
            'adj_at' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Adjustment Date",}),

            'last_adj' : TextInput(attrs={'class':"form-control",
            'id':"last_adj",
            'placeholder':"Adjustment %",}),}
        
        

class AdjustAccount(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())         
    last_adj = forms.CharField(widget=TextInput(attrs={'class':"form-control",'id':"last_adj",'placeholder':"Adjustment %",}))
    adj_at = forms.CharField(widget=TextInput(attrs={'class':"datetimepicker form-control",
        'id':"PublishDateTimeTextbox",
        'type':"date",
        'placeholder':"Adjustment Date",}))
    
    
class AdjForm(ModelForm):
    client = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control wide mb-3',
            'placeholder': 'type client name...',
            'id': 'client',
            'autocomplete': 'on',
            'list': 'clients',
        })
    )
    service = ModelChoiceField(
        queryset=Service.objects.filter(state=True),
        widget=Select(
            attrs={
                'class': "default-select form-control wide mb-3",
                'id': "service",
                'placeholder': "service",
            }
        ),
        empty_label=' - ',
        required=False  
    )
    
    class Meta:
        model = Adj
        fields = ['notice_date', 'adj_percent', 'date_alert', 'type' ]
        
        widgets = {
            
            'notice_date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Notice Date",}),

            'date_alert' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Internal RemainderDate",}),
 
            'adj_percent' : TextInput(attrs={'class':"form-control",
            'id':"adj_percent",
            'placeholder':"Adjustment %",}),

            'type' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"type",
                'placeholder' : "type",
                'empty_label': "Account/Service"
                }
            ),
        }
        

class SaleForm(ModelForm):
    
    client = ModelChoiceField(queryset=Client.objects.all(), widget=Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"client",
            'placeholder':"client",}), empty_label = ' - ')

    

    class Meta:
        model = Sale
        
        exclude = ['sale_id', 'cancelled', 'comment_can', 'date_can', 'fail_can', 'revenue', 'change']
        
        
        widgets = {
            
            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),

            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
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
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status"
                }
            ),

        }



class ClientSaleForm(ModelForm):
    
    
    
    
    class Meta:
        model = Sale
        
        exclude = ['id', 'cancelled', 'comment_can', 'date_can', 'fail_can', 'revenue', 'client', 'change']
        
        
        
        widgets = {
            
            
            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),

            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
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
            
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),
            

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status"
                }
            ),

        }


class EditSaleForm(ModelForm):
    
        
    class Meta:
        model = Sale
        
        exclude = ['id', 'revenue', 'client', 'change']
        
        
        
        widgets = {

            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),
            
            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
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
            
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status"
                }
            ),
            
            'cancelled' : Select(attrs={
                'class':"default-select form-control wide mb-3",
            'id':"cancelled",
            'placeholder':"Cancelled?",}),
            
            'date_can' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Cancellation date",}),
            
            'fail_can' : Select(attrs={
                'class':"default-select form-control wide mb-3",
            'id':"fail_can",
            'placeholder':"Do we fail?",}),
            
            'comment_can' : Textarea(attrs={
                'class':"form-control",
                'id':"comment_can",
                'placeholder' : "Comment"
                }
            ),

        }
