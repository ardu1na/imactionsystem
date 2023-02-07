from django.forms import ModelForm, \
TextInput, URLInput, EmailInput, Select, Textarea

from expenses.models import Employee


class EmployeeForm(ModelForm): 
    
   
    class Meta:
        model = Employee
        
        exclude = ['id', 'active', 'date_gone', 'white', 'nigga', 'mp', 'tc', 'atm_cash']
        
        widgets = {

            'date_join' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date"}),
            
            
            'rol' : Select(attrs={
                'class':"form-select",
                'id':"rol",
                'placeholder' : "Rol",
                }
            ),


            'name' : TextInput(attrs={'class':"form-control",
            'id':"name",
            'placeholder':"Name",}),

            'address' : TextInput(attrs={'class':"form-control",
            'id':"address",
            'placeholder':"Address",}),


            'email' : EmailInput(attrs={
                'class':"form-control",
                'id':"email",
                'placeholder' : "Email"
                }
            ),

            'tel' : TextInput(attrs={
                'class':"form-control",
                'id':"tel",
                'placeholder' : "Phone Number"
                }
            ),
        }



"""


class EditEmployeeForm(ModelForm):
    
    class Meta:
        model = Employee
        
        exclude = ['id',]
        
        widgets = {

            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),


            'name' : TextInput(attrs={'class':"form-control",
            'id':"name",
            'placeholder':"Employee",}),

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




class BankDataForm(ModelForm):
    
    
    
    
    class Meta:
        model = BankData
        
        exclude = ['id', 'account',]
        
        
        
        widgets = {
            
            
            

            'payment' : Select(attrs={'class':"form-select",
            'id':"payment",
            'placeholder':"Payment",}),

            'cbu' : TextInput(attrs={'class':"form-control",
            'id':"cbu",
            'placeholder':"CBU",}),

            'alias' : TextInput(attrs={
                'class':"form-control",
                'id':"alias",
                'placeholder' : "Alias",
                }
            ),


            'cuit' : TextInput(attrs={
                'class':"form-control",
                'id':"cuit",
                'placeholder' : "CUIT"
                }
            ),

            'detail' : TextInput(attrs={
                'class':"form-control",
                'id':"detail",
                'placeholder' : "Detail"
                }
            ),

        }"""