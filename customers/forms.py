from django.forms import ModelForm, \
TextInput, URLInput, EmailInput, Select, Textarea
from customers.models import Client,  ConfTier



class TierConf(ModelForm):
    class Meta:
        model = ConfTier
        exclude = ['id',]
        
        widgets = {
            'tier_i' : TextInput(attrs={'class':"form-control",
            'id':"tier_i",
            'placeholder':"Tier I"}),
            
            'tier_ii' : TextInput(attrs={'class':"form-control",
            'id':"tier_ii",
            'placeholder':"Tier II"}),
            
            'tier_iii' : TextInput(attrs={'class':"form-control",
            'id':"tier_iii",
            'placeholder':"Tier III"}),
            
            'tier_iv' : TextInput(attrs={'class':"form-control",
            'id':"tier_iv",
            'placeholder':"Tier IV"}),
            
            'tier_v' : TextInput(attrs={'class':"form-control",
            'id':"tier_v",
            'placeholder':"Tier V"}),
        }



class ClientForm(ModelForm): 
    
   
    class Meta:
        model = Client
        
        exclude = ['id', 'cancelled', 'comment_can', 'date_can', 'fail_can']
        
        widgets = {

            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date"}),

            'name' : TextInput(attrs={'class':"form-control",
            'id':"name",
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

            'wop' : Select(attrs={
                'class':"form-select",
            'id':"wop",
            'placeholder':"WOP",}),

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
        
        exclude = ['id',]
        
        widgets = {

            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),


            'name' : TextInput(attrs={'class':"form-control",
            'id':"name",
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

            'wop' : Select(attrs={
                'class':"form-select",
            'id':"wop",
            'placeholder':"WOP",}),

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
            
            'date_can' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Cancellation date",}),
            
            
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


