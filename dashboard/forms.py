from django import forms
from dashboard.models import Configurations, Comms



class CommsForm(forms.ModelForm):
    class Meta:
        model = Comms
        exclude = ['id']
        
        widgets = {
            'rr_1' : forms.TextInput(attrs={'class':"form-control",
            'id':"rr_1",
            'placeholder':"RR I"}),
            
            'com_rr_1' : forms.TextInput(attrs={'class':"form-control",
            'id':"com_rr_1",
            'placeholder':"COMM RR I"}),
            
            'rr_2' : forms.TextInput(attrs={'class':"form-control",
            'id':"rr_2",
            'placeholder':"RR II"}),
            
            'com_rr_2' : forms.TextInput(attrs={'class':"form-control",
            'id':"com_rr_2",
            'placeholder':"COMM RR II"}),
            
            'rr_3' : forms.TextInput(attrs={'class':"form-control",
            'id':"rr_3",
            'placeholder':"RR III"}),
            
            'com_rr_3' : forms.TextInput(attrs={'class':"form-control",
            'id':"com_rr_3",
            'placeholder':"COMM III"}),
            
            'rr_4' : forms.TextInput(attrs={'class':"form-control",
            'id':"rr_4",
            'placeholder':"RR IV"}),
            
            'com_rr_4' : forms.TextInput(attrs={'class':"form-control",
            'id':"com_rr_4",
            'placeholder':"COMM RR IV"}),
            
            'rr_5' : forms.TextInput(attrs={'class':"form-control",
            'id':"rr_5",
            'placeholder':"RR V"}),
            
            'com_rr_5' : forms.TextInput(attrs={'class':"form-control",
            'id':"com_rr_5",
            'placeholder':"COMM RR V"}),
            
            'one_off' : forms.TextInput(attrs={'class':"form-control",
            'id':"one_off",
            'placeholder':"One Off"}),
            
            'up_sell' : forms.TextInput(attrs={'class':"form-control",
            'id':"up_sell",
            'placeholder':"Up Sell"}),         
            
        }

class UploadFileForm(forms.Form):
    file = forms.FileField()



class ConfigurationForm(forms.ModelForm):
    
    class Meta:
        model = Configurations
        fields = ( 
                  'name',
                  'value',
                  'title',
                  'description',
                  'input_type',
                  'editable',
                  'params'
                  )
                    