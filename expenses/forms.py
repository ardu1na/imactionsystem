from django import forms

from django.forms import ModelForm, \
TextInput, EmailInput, Select
from django.forms import formset_factory


from expenses.models import Employee, Expense, Holiday, Salary

class HolidayEmployeeForm(ModelForm):
    class Meta:
        model = Holiday
        exclude = ['id', 'employee']

        widgets = {
            
            
            'year': TextInput(attrs=
                              {'class':"form-control",
                                'id':"year",
                                'placeholder':"YEAR",}),
            
            'month': Select(attrs={
                        'class':"default-select form-control wide mb-3",
                        'id':"month",
                        'placeholder' : "MONTH",
                        }),
            
            'days': TextInput(attrs=        
                              {'class':"form-control",
                                'id':"days",
                                'placeholder':"DAYS",}),
            
            'date_start' : TextInput(attrs=
                                {'class':"datetimepicker form-control",
                                'id':"PublishDateTimeTextbox",
                                'type':"date",
                                'placeholder':"Date Start",}),
            
            
            'date_end' : TextInput(attrs=
                            {'class':"datetimepicker form-control",
                            'id':"PublishDateTimeTextbox",
                            'type':"date",
                            'placeholder':"Date End",}),
                        }




class ExpenseForm(ModelForm):  
    class Meta:
        model = Expense
        
        exclude = ['id',]
        
        
        
        
        widgets = {
            
            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),

            'category' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"category",
            'placeholder':"Category",}),

            'concept' : TextInput(attrs={'class':"form-control",
            'id':"concept",
            'placeholder':"Concept",}),

            'wop' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"wop",
                'placeholder' : "WOP",
                }),
            
            'value' : TextInput(attrs={
                'class':"form-control",
                'id':"value",
                'placeholder' : "Value"
                }),

        }



class EmployeeForm(ModelForm): 
    
       class Meta:
        model = Employee
        exclude = ['id', 'active', 'date_gone']
        
        widgets = {
            
            'date_join' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date"}),            
            
            'rol' : Select(attrs={
                'class':"default-select form-control wide mb-3",
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

class EmployeeSalaryForm(ModelForm): 
    
       class Meta:
        model = Salary
        fields = ['salary', 'nigga']
        
        widgets = {
            
            
            
            'salary' : TextInput(attrs={
                'class':"form-control",
                'id':"salary",
                'placeholder' : "salary"
                }
            ),          

            'nigga' : TextInput(attrs={
                'role':"textbox",

                'class':"form-control",
                'id':"nigga",
                'placeholder' : "NIGGA %"
                }
            ),        
            
           
        }
        
        


class CeoForm(ModelForm): 
    
       class Meta:
        model = Employee
        exclude = ['id', 'active', 'date_gone']
        
        widgets = {
            
            'date_join' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date"}),            
            
            'rol' : Select(attrs={
                'class':"default-select form-control wide mb-3",
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


class CeoSalaryForm(ModelForm): 
    
       class Meta:
        model = Salary
        fields = ['salary', 'atm_cash', 'cash', 'mp', 'paypal', 'cash_usd', 'tc']
        
        widgets = {
            
            
            
            'salary' : TextInput(attrs={
                'class':"form-control",
                'id':"salary",
                'placeholder' : "salary"
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
            
            'cash' : TextInput(attrs={
                'class':"form-control",
                'id':"cash",
                'placeholder' : "CASH"
                }
        
            ),
            
            'atm_cash' : TextInput(attrs={
                'class':"form-control",
                'id':"atm_cash",
                'placeholder' : "ATM"
                }
            ),
            
            'cash_usd' : TextInput(attrs={
                'class':"form-control",
                'id':"cash_usd",
                'placeholder' : "CASH USD"
                }
            ),
            
            'paypal' : TextInput(attrs={
                'class':"form-control",
                'id':"paypal",
                'placeholder' : "PAYPAL"
                }
            ),
            
           
        }
    
    
    
    
    
class EditEmployeeForm(ModelForm):
    
    class Meta:
        model = Employee
        
        fields = ['active', 'date_join', 'date_gone', 'rol', 'name', 'address', 'email', 'tel']
        
        widgets = {
            
            'active' :     Select(attrs={
                'class':"default-select form-control wide mb-3",
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
                'class':"default-select form-control wide mb-3",
                'id':"rol",
                'placeholder' : "AREA",
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
        model = Salary
        
        fields = ['salary', 'nigga', 'period']
        
        widgets = {           

            
            'salary' : TextInput(attrs={
                'class':"form-control",
                'id':"salary",
                'placeholder' : "SALARY"
                }
            ),          

            'nigga' : TextInput(attrs={
                'role':"textbox",

                'class':"form-control",
                'id':"nigga",
                'placeholder' : "NIGGA %"
                }
            ),        
            
             'period' : TextInput(attrs=
                                {'class':"datetimepicker form-control",
                                'id':"PublishDateTimeTextbox",
                                'type':"date",
                                'placeholder':"Date Start",}),
            
            
            
            }
        
        
        
class EditWageCeo(ModelForm):
    
    class Meta:
        model = Salary
        
        exclude = ['id', 'rol', 'name', 'address', 'email', 'tel', 'date_join', 'active','date_gone', 'nigga']
        
        widgets = {           

            
            'salary' : TextInput(attrs={
                'class':"form-control",
                'id':"salary",
                'placeholder' : "SALARY"
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
        
            ),
            
            'cash' : TextInput(attrs={
                'class':"form-control",
                'id':"cash",
                'placeholder' : "CASH"
                }
        
            ),
            
            
            'cash_usd' : TextInput(attrs={
                'class':"form-control",
                'id':"cash_usd",
                'placeholder' : "CASH USD"
                }
            ),
            
            'paypal' : TextInput(attrs={
                'class':"form-control",
                'id':"paypal",
                'placeholder' : "PAYPAL"
                }
            ),
            
            'period': TextInput(attrs=
                                {'class':"datetimepicker form-control",
                                'id':"PublishDateTimeTextbox",
                                'type':"date",
                                'placeholder':"Date Start",}),
            
            }