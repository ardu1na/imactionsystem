from django.forms import ModelForm, \
TextInput, EmailInput, Select, BooleanField

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
                }),

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
                }),

            'tel' : TextInput(attrs={
                'class':"form-control",
                'id':"tel",
                'placeholder' : "Phone Number"
                }),
        }


class EditEmployeeForm(ModelForm):
    
    class Meta:
        model = Employee
        
        exclude = ['id',]
        
        widgets = {
            
            'active' :     Select(attrs={
                'class':"form-select",
                'id':"active",
                'placeholder' : "Active?",
                }),


            'date_join' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date"}),     
            
            
            'date_gone' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date Gone"}),     



            'rol' : Select(attrs={
                'class':"form-select",
                'id':"rol",
                'placeholder' : "Rol",
                }),
            

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
                }),

            'tel' : TextInput(attrs={
                'class':"form-control",
                'id':"tel",
                'placeholder' : "Phone Number"
                }),
            }        
        
        
class EditWageForm(ModelForm):
    
    class Meta:
        model = Employee
        
        exclude = ['id', 'rol', 'name', 'address', 'email', 'tel', 'date_join', 'active','date_gone']
        
        widgets = {           

            'white' : TextInput(attrs={
                'class':"form-control",
                'id':"white",
                'placeholder' : "WHITE"
                }
            ),          

            'nigga' : TextInput(attrs={
                'role':"textbox",

                'class':"form-control",
                'id':"nigga",
                'placeholder' : "NIGGA"
                }
            ),        
            
            'mp' : TextInput(attrs={
                'class':"form-control",
                'id':"mp",
                'placeholder' : "MP"
                }
            ),                      

            'tc' : TextInput(attrs={
                'class':"form-control",
                'id':"tc",
                'placeholder' : "TC"
                }
            ),          
            
            'atm_cash' : TextInput(attrs={
                'class':"form-control",
                'id':"atm_cash",
                'placeholder' : "ATM CASH"
                }
            ),}