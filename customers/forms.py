from django.forms import ModelForm, \
TextInput, URLInput, EmailInput, Select

from customers.models import Client


class ClientForm(ModelForm):
    
    class Meta:
        model = Client
        
        exclude = ['id_client', 'cancelled', 'date', 'comment_can', 'date_can', 'fail_can']
        
        widgets = {

            'customer' : TextInput(attrs={'class':"form-control",
            'id':"customer",
            'placeholder':"Client",}),

            'website' : URLInput(attrs={'class':"form-control",
            'id':"website",
            'placeholder':"Website",}),

            'business_name' : TextInput(attrs={'class':"form-control",
            'id':"business_name",
            'placeholder':"Business name",}),

            'source' : Select(attrs={
                'class':"form-select",
                'id':"source",
                'placeholder' : "Source",
                'empty_label':"Select the source",
                }
            ),


            'email' : EmailInput(attrs={
                'class':"form-control",
                'id':"email",
                'placeholder' : "Email"
                }
            ),

            'phone_number' : TextInput(attrs={
                'class':"form-control",
                'id':"phone_number",
                'placeholder' : "Phone Number"
                }
            ),

            'phone_2' : TextInput(attrs={
                'class':"form-control",
                'id':"phone_2",
                'placeholder' : "Other Phone Number"
                }
            ),

            'email_2' : EmailInput(attrs={
                'class':"form-control",
                'id':"email_2",
                'placeholder' : "Other Email"
                }
            ),

            'email_admin' : EmailInput(attrs={
                'class':"form-control",
                'id':"email_admin",
                'placeholder' : "Email Admin"
                }
            ),

            'landing_page' : URLInput(attrs={'class':"form-control",
            'id':"landing_page",
            'placeholder':"Landing Page",}),


        }






class EditClientForm(ModelForm):
    
    class Meta:
        model = Client
        
        exclude = ['id_client','date', 'date_can',]
        
        widgets = {

            'customer' : TextInput(attrs={'class':"form-control",
            'id':"customer",
            'placeholder':"Client",}),

            'website' : URLInput(attrs={'class':"form-control",
            'id':"website",
            'placeholder':"Website",}),

            'business_name' : TextInput(attrs={'class':"form-control",
            'id':"business_name",
            'placeholder':"Business name",}),

            'source' : Select(attrs={
                'class':"form-select",
                'id':"source",
                'placeholder' : "Source",
                'empty_label':"Select the source",
                }
            ),


            'email' : EmailInput(attrs={
                'class':"form-control",
                'id':"email",
                'placeholder' : "Email"
                }
            ),

            'phone_number' : TextInput(attrs={
                'class':"form-control",
                'id':"phone_number",
                'placeholder' : "Phone Number"
                }
            ),

            'phone_2' : TextInput(attrs={
                'class':"form-control",
                'id':"phone_2",
                'placeholder' : "Other Phone Number"
                }
            ),

            'email_2' : EmailInput(attrs={
                'class':"form-control",
                'id':"email_2",
                'placeholder' : "Other Email"
                }
            ),

            'email_admin' : EmailInput(attrs={
                'class':"form-control",
                'id':"email_admin",
                'placeholder' : "Email Admin"
                }
            ),

            'landing_page' : URLInput(attrs={'class':"form-control",
            'id':"landing_page",
            'placeholder':"Landing Page",}),
            
            
            'cancelled' : Select(attrs={
                'class':"form-select",
            'id':"cancelled",
            'placeholder':"Cancelled?",}),
            
            
            'fail_can' : Select(attrs={
                'class':"form-select",
            'id':"fail_can",
            'placeholder':"Do we fail?",}),
            
            'comment_can' : TextInput(attrs={
                'class':"form-control",
                'id':"comment_can",
                'placeholder' : "Comment"
                }
            ),


        }
