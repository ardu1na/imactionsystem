from django import template
from django.urls import resolve
from django.urls.exceptions import Resolver404
from loguru import logger
from dashboard.models import Configurations
import json



register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) + 1] # access the next element
    except:
        return '' # return empty string in case of exception

@register.filter
def previous(some_list, current_index):
    """
    Returns the previous element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) - 1] # access the previous element
    except:
        return '' # return empty string in case of exception
    
def percentage_increase(current_salary, previous_salary):
    if previous_salary == 0:
        return "-"
    else:
        return "{:.2f}%".format((current_salary - previous_salary) / previous_salary * 100)
register.filter('percentage_increase', percentage_increase)


def getdata(json_data, args):    
    func_name=''
    try:
        myfunc, myargs, mykwargs = resolve(args)
        if myfunc:
            logger.success("*"*50)
            print()
            logger.debug("Function Name:> {} ",myfunc.__name__,feature="f-strings")
            logger.debug("Module Name:> {} ",myfunc.__module__,feature="f-strings")
            logger.debug("URL_Path:> {} ",args,feature="f-strings")
            func_name=myfunc.__name__
            print()
            logger.success("*"*50)
    except Resolver404:
        logger.debug("something went wrong",feature="f-strings")
        pass

    return json_data.get(func_name)


register.filter('getdata', getdata)



# Get Menus


def getAllprefix(var):
    name_list = Configurations.objects.all().order_by('created_at').values_list('name',flat=True)
    prefixes=[]
    for name in name_list:
        if len(name.split('.')) > 1:
            prefix=name.split('.')[0]
            if prefix not in prefixes:
                prefixes.append(prefix)
        else:
            prefixes.append(name)            
    
    return prefixes

register.filter('getAllprefix', getAllprefix)



def split(val,args):
    return val.split(args)
register.filter('split', split)



def multiply(val1,val2):
    return val1*val2
register.filter('multiply', multiply)



# def getStringToJson(val):
#     print("String to Dict")
#     print(val)
#     print(type(val))
   
#     return val
    
# register.filter('getStringToJson', getStringToJson)


# request.path	                  /home/
# request.get_full_path	         /home/?q=test
# request.build_absolute_uri	 http://127.0.0.1:8000/home/?q=test