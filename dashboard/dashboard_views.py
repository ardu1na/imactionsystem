### imports
import json
import os
import pickle
import mimetypes
from datetime import datetime, date
from decimal import Decimal
from itertools import chain
## django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required 
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.decorators.http import require_GET
from django.db.models import Sum, Q
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

## external packages 
from easyaudit.models import CRUDEvent, LoginEvent
# dashboard app
from dashboard import setup_config
from dashboard.models import Configurations, Comms, LastBlue
from dashboard.users.models import CustomUser
from dashboard.utils import *
try: 
    from dashboard.services import venta as b_venta
except: pass
from dashboard.forms import CommsForm
from dashboard.resources import ExportSales, ClientResource, ExportRR, ExpenseResource, ExportStaff, ExportCeo
# customers app
from customers.models import ConfTier, BackUps, Client, AutoRevenue
from customers.forms import TierConf, ClientForm, EditClientForm
# sales app
from sales.models import Sale, Service, Adj
from sales.forms import AdjForm, ChangeAdj, SaleForm2, ClientSaleForm, CancellService, EditSaleForm
# expenses app
from expenses.models import Employee, Expense, Holiday, Salary
from expenses.forms import RaiceForm, HolidayEmployeeForm, ExpenseForm, EmployeeForm, EmployeeSalaryForm, CeoForm, CeoSalaryForm, EditEmployeeForm, EditWageCeo 

### END IMPORTS



####################################################################
# VIEWS - LÓGICA DE LA APP

# get today info
today = date.today()

######################## AJAX REQUEST
# ESTA FUNCIÓN SIRVE PARA AUTOCOMPLETAR LOS CLIENTES EN LOS FORMS
@login_required(login_url='dashboard:login')
@require_GET
def client_autocomplete(request):
    q = request.GET.get('q', '')
    clients = Client.objects.filter(name__icontains=q)
    results = [{'id': c.pk, 'text': c.name} for c in clients]
    return JsonResponse({'results': results})

######################################################################################################################################
## HISTORIAL DE CAMBIOS
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())   
@login_required(login_url='dashboard:login')
def activity(request):
  
    # Registro de actividad en el ERP
    # exceptuando cambios en la cotización del blue y usuarios.
    ct = ContentType.objects.get_for_model(LastBlue)
    ct2 = ContentType.objects.get_for_model(CustomUser)
    events = CRUDEvent.objects.exclude(content_type=ct).exclude(content_type=ct2)
    logs = LoginEvent.objects.all()
    combined_list = list(chain(events, logs))     
    paginator = Paginator(combined_list, 20) # Show 20 elements per page.
    elements = paginator.get_page(request.GET.get('page'))
    context={
        "page_title":"Activity",
        "events" : events,
        "logs" : logs,
        "list" : elements,}
    return render(request,'dashboard/activity.html',context)

######################################################################################################################################


## CONFIGURACIONES Y AJUSTES 

@login_required(login_url='dashboard:login')
def setting (request):
    # pestaña principal de acceso a configuraciones
    context = {
            "page_title": "SETTINGS",
            }
    return render (request, 'dashboard/table/settings.html', context)


@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def conf(request):
    
    # ajuste de parámetros de valor del cliente (tier)    
    tier = ConfTier.objects.get(id=1)

    if request.method == "GET":

        form = TierConf(instance=tier)
        
        context = {
            "page_title": "CHANGE TIER PARAMETERS",
            'form': form,
            'id': id
            }
        return render (request, 'dashboard/table/conf.html', context)

    if request.method == 'POST':
        form = TierConf(request.POST, instance=tier)
        print(form.errors)
        if form.is_valid():
            tier = form.save()
                      
            return redirect(reverse('dashboard:index')+ "?changed")
        else:
            return HttpResponse(
                f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {form.errors}")
        
        
### COMISIONES DE VENTA
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def comms(request):
    
    # ajuste de parámetros de valor de las comisiones x venta  
    comms = Comms.objects.get(id=1)

    if request.method == "GET":

        form = CommsForm(instance=comms)
        
        context = {
            "page_title": "CHANGE COMMS PARAMETERS",
            'form': form,
            'id': id
            }
        return render (request, 'dashboard/table/comms.html', context)

    if request.method == 'POST':
        form = CommsForm(request.POST, instance=comms)
        print(form.errors)
        if form.is_valid():
            comms = form.save()
                      
            return redirect(reverse('dashboard:index')+ "?changed")
        else:
            return HttpResponse(
                f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {form.errors}")



##############################################################################################################################################################


## EXPENSES CRUD

@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def editexpense(request, id):
    # EXPENSE DETAIL . EDIT INSTANCE
    editexpense = Expense.objects.get(id=id)
    
    if request.method == "GET":
    
        form = ExpenseForm(instance=editexpense)
        
        context = {
            'form': form,
            'editexpense': editexpense,
            'id': id
            }
        return render (request, 'dashboard/table/editexpense.html', context)

    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=editexpense)
        if form.is_valid():
            form.save()
            return redirect ('dashboard:editexpense', id=editexpense.id)
        else:
            return HttpResponse(
                f"Ups! Something went wrong. You should go back, update the page and try again.\n \n {form.errors}"
                )
        

## exportación de expenses para excel
@login_required(login_url='dashboard:login')
def export_expenses(request):
    dataset = ExpenseResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    return response



        
        
@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def expenses(request):
    
    # EXPENSES + SALARIES -- OF CURRENT MONTH

    expenses = Expense.objects.filter(date__month=today.month, date__year= today.year)
    employees = Employee.objects.filter(active="Yes").exclude(rol="CEO")
    ceo = Employee.objects.filter(rol="CEO", active="Yes")
    
    if request.method == 'GET':
        addform = ExpenseForm()
    
    
    # nueva expense    
    if request.method == 'POST':
        if "addexpense" in request.POST:
            addform = ExpenseForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('dashboard:expenses')+ "?added")
            else:
                return HttpResponse(
                    f"Ups! Something went wrong. You should go back, update the page and try again.\n \n {addform.errors}")
    
    
    ###############################################        
    ## CALCULOS PARA LAS CARDS      
    without_wages = 0
    for expense in expenses:
        if expense.change > 0:
            without_wages += expense.change
        else:
            without_wages += expense.value
    
    all_bonus = 0
    wages_staff = 0
    wages_ceo = 0
    
    try:
        for i in ceo:
            wages_ceo += i.get_total_ceo()
            all_bonus += i.get_aguinaldo_mensual()
            
        for employee in employees:
            wages_staff += employee.get_total()
            all_bonus += employee.get_aguinaldo_mensual()
    except: pass               
    with_wages = without_wages + Decimal(wages_staff) + wages_ceo
        
    
    ## DATA PARA EL GRÁFICO    
    empresa = 0
    lead_gen = 0
    office = 0
    other = 0
    tax = 0
    
    for expense in expenses:
        if expense.category == "Empresa":
            if expense.change > 0:
                empresa += expense.change
            else:
                empresa += expense.value
        if expense.category == "Lead Gen":
            if expense.change > 0:
                lead_gen += expense.change
            else:
                lead_gen += expense.value    
        if expense.category == "Office":
            if expense.change > 0:
                office += expense.change
            else:
                office += expense.value  
        if expense.category == "Other":
            if expense.change > 0:
                other += expense.change
            else:
                other += expense.value           
        if expense.category == "Tax":
            if expense.change > 0:
                tax += expense.change
            else:
                tax += expense.value            
            
    all = empresa + lead_gen + office + tax + other + Decimal(wages_staff) + wages_ceo
    
    try:            
        empresa1 = (empresa*100)/all
        lead_gen1 = (lead_gen*100)/all
        tax1 = (tax*100)/all
        wages_staff1 = (wages_staff*100)/all
        other1 = (other*100)/all
        office1 = (office*100)/all
        wages_ceo1 = (wages_ceo*100)/all
    except:
        empresa1 = 0
        lead_gen1 = 0
        tax1 = 0
        wages_staff1 = 0
        other1 = 0
        office1 = 0
        wages_ceo1 = 0
                    
    context={
        "page_title": "Expenses",
        "expenses" : expenses,
        "addform" : addform,
        "without_wages" : without_wages,
        "with_wages": with_wages,
        "all_bonus" : all_bonus,
        "employees" : employees,
        "ceo" : ceo,     
        #chart data  
        "empresa" : empresa,
        "lead_gen" : lead_gen,
        "office" : office,
        "other" : other,
        "tax" : tax,
        "wages_ceo" : wages_ceo,
        "ceo" : ceo,     
        "wages_staff" : wages_staff,
        "empresa1" : empresa1,
        "lead_gen1" : lead_gen1,
        "office1" : office1,
        "other1" : other1,
        "tax1" : tax1,
        "wages_ceo1" : wages_ceo1,
        "wages_staff1" : wages_staff1,}
    return render(request,'dashboard/table/expenses.html', context)


## borrar expense
@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def deleteexpense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect(reverse('dashboard:expenses')+ "?deleted")


# historial de una expensa    
@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def expenseshistory(request, id):
    editexpense = Expense.objects.get(id=id)
    same_expense = Expense.objects.filter(concept=editexpense.concept)   
    context = {
            'editexpense' : editexpense,
            'same_expense': same_expense,
            'id': id,
            'page_title':'Expense History',
            }
    return render (request, 'dashboard/instructor/expenseshistory.html', context)





########################################################################################################################################################
## EMPLOYEES

## función para exportar la info de los empleados para excel
@login_required(login_url='dashboard:login')
def export_employees(request):
    dataset = ExportStaff().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'
    return response


@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def employees(request):
    staff = Employee.objects.exclude(rol="CEO").filter(active="Yes")
    ceo = Employee.objects.filter(rol="CEO")        
    employees  = Employee.objects.filter(active="Yes")
    all = Employee.objects.all()
    
    if request.method == 'GET':
        addform = EmployeeForm()
        salaryform = EmployeeSalaryForm()
        
    if request.method == 'POST':
        if "addemployee" in request.POST:
            addform = EmployeeForm(request.POST)
            salaryform = EmployeeSalaryForm(request.POST)
            if addform.is_valid() and salaryform.is_valid():
                employee = addform.save()
                salary = salaryform.save(commit=False)
                salary.employee = employee
                salary.save()
                return redirect(reverse('dashboard:employees')+ "?added")
            else:
                return HttpResponse(
                    f"Ups! Something get wrong with the form. Please go back, reload the page and try again. \n \n {addform.errors}")           
    
    # cards data
    total_white = 0
    total_nigga = 0
    total_total = 0    
    for employee in staff:
        try:
            total_white += employee.get_white()        
            total_nigga += employee.get_nigga()
            total_total += employee.get_total()
        except: pass     
          
    context={
        "staff": staff,
        "count_staff": staff.count(),
        "ceo": ceo,
        "employees": employees,
        "all": all,
        "employee_form": addform,
        "salary_form": salaryform,
        "white": total_white,
        "nigga": total_nigga,
        "total": total_total,        
        "page_title":"WAGES STAFF",}
    return render(request,'dashboard/instructor/employees.html', context)


# listado de empleados antiguos
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def employeesold(request):
    old =Employee.objects.filter(active="No")                                
    context={        
        "page_title":"STAFF OLD",
        "old": old,}
    return render(request,'dashboard/instructor/employeesold.html',context)


# eliminar un empleado
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def deleteemployee(request, id):
    employee = Employee.objects.get(id=id)
    id = employee.id
    employee.delete()
    return redirect(reverse('dashboard:employees')+ "?deleted")


## detalle de un EMPLEADO
@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def editemployee(request, id):
    # employee detail    
    editemployee = Employee.objects.get(id=id)
    holidays = Holiday.objects.filter(employee=editemployee)
    salaries = Salary.objects.filter(employee=editemployee)
    try:
        wage_instance = Salary.objects.get(employee=editemployee, period__month=today.month, period__year=today.year)
    except:
        wage_instance =Salary.objects.filter(employee=editemployee).first()
            
    # if rol == seller get employees comms of current month
    comms_this_m = 0
    if editemployee.rol == "Sales":
        for sale in editemployee.sales.filter(date__month=today.month, date__year=today.year):
            comms_this_m += sale.get_comm
        
        
    if request.method == "GET":      
        editform = EditEmployeeForm(instance=editemployee)
        
        editwageform = EmployeeSalaryForm(instance=wage_instance) if wage_instance else EmployeeSalaryForm()
        raice = RaiceForm()
        
        holydayform = HolidayEmployeeForm()
        context = {
            'comms_this_m': comms_this_m,
            'raice': raice,
            'holidayform'  : holydayform,
            'editform': editform,
            'editwageform': editwageform,
            'editemployee': editemployee,
            'id': id,
            'holidays': holidays,
            'salaries': salaries,
            }       
        return render (request, 'dashboard/instructor/editemployee.html', context)

    # edit employee
    if request.method == 'POST':
        # para modificar el salario
        if "editwage" in request.POST:
            
            editwageform = EmployeeSalaryForm(request.POST, instance=wage_instance) if wage_instance else EmployeeSalaryForm(request.POST)
            if editwageform.is_valid():
                wage = editwageform.save(commit=False)
                wage.employee = editemployee
                wage.save()
                return redirect(reverse('dashboard:editemployee', kwargs={'id': editemployee.id}) + '#pay')
            else: 
                return HttpResponse(f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {editwageform.errors}")

        # para aumentar el salario con porcentajes
        if "raice" in request.POST:
            raice = RaiceForm(request.POST)
            if raice.is_valid():
                raice_nigga = raice.cleaned_data['nigga']
                raice_salary = raice.cleaned_data['salary']
                
                last_wage = wage_instance
                last_wage.salary = last_wage.salary + (last_wage.salary*Decimal(raice_salary))/100
                last_wage.nigga = Decimal(raice_nigga)
                last_wage.raice = Decimal(raice_salary)
                last_wage.save()
                return redirect(reverse('dashboard:editemployee', kwargs={'id': editemployee.id}) + '#pay')
            else:
                return HttpResponse(f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {raice.errors}")
        
        # detalles del empleado
        if "editemployee" in request.POST:
            editform = EditEmployeeForm(request.POST, instance=editemployee)
            print (editform)
            if editform.is_valid():
                editform.save()
                return redirect('dashboard:editemployee', id=editemployee.id)
            else:
                return HttpResponse(f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {editform.errors}")
        
        # vacaciones
        if "holiday" in request.POST:
            holydayform = HolidayEmployeeForm(request.POST)
            if holydayform.is_valid():
                holiday = holydayform.save(commit=False)
                holiday.employee = editemployee
                holiday.save()
                return redirect(reverse('dashboard:editemployee', kwargs={'id': editemployee.id}) + '#holiday')
            else:
                return HttpResponse(f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {holydayform.errors}")



# detalle de una vacacion
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def editholiday(request, id):
    editholiday = Holiday.objects.get(id=id)
    editemployee = editholiday.employee      
    if request.method == "GET":          
        holyday_instance = Holiday.objects.filter(employee=editemployee).last()
        holydayform = HolidayEmployeeForm(instance=holyday_instance) if holyday_instance else HolidayEmployeeForm()
        context = {
            'holidayform'  : holydayform,
            'editemployee': editemployee,
            'id': id}
        return render (request, 'dashboard/instructor/editholiday.html', context)

    # editar una vacacion
    if request.method == 'POST':                
        if "holiday" in request.POST:
            holyday_instance = Holiday.objects.filter(employee=editemployee).last()
            holydayform = HolidayEmployeeForm(request.POST, instance=holyday_instance) if holyday_instance else HolidayEmployeeForm(request.POST)
            if holydayform.is_valid():
                holiday = holydayform.save(commit=False)
                holiday.employee = editemployee
                holiday.save()
                return redirect('dashboard:editemployee', id=editemployee.id)
            else:
                return HttpResponse(
                    f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {holydayform.errors}")


# borrar una vacación
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def deleteholiday(request, id):
    holiday = Holiday.objects.get(id=id)
    holiday.delete()
    employeeid=holiday.employee.id
    
    if holiday.employee.rol == "CEO":
        return redirect(reverse('dashboard:editceo', kwargs={'id': employeeid}) + '#holiday')
    else:
        return redirect(reverse('dashboard:editemployee', kwargs={'id': employeeid}) + '#holiday')



############ CEO


## función para exportar data de ceo para excel
@login_required(login_url='dashboard:login')
def export_ceo(request):
    dataset = ExportCeo().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ceo.xlsx"'
    return response


# lista de ceo
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def ceo(request):
    ceo = Employee.objects.filter(rol="CEO")           
    if request.method == 'GET':
        addform = CeoForm()
        salaryform = CeoSalaryForm()                   
    if request.method == 'POST':
        if "addemployee" in request.POST:
            addform = CeoForm(request.POST)
            salaryform = CeoSalaryForm(request.POST)
            if addform.is_valid() and salaryform.is_valid():
                employee = addform.save()
                salary = salaryform.save(commit=False)
                salary.employee = employee
                salary.save()
                return redirect(reverse('dashboard:ceo')+ "?added")
            else:
                return HttpResponse(
                    f"Ups! Something get wrong. \n\n {addform.errors}")                                     
    context={
        "ceo": ceo,
        "ceo_form": addform,
        "salary_form": salaryform,        
        "page_title":"WAGES CEO",}
    return render(request,'dashboard/instructor/ceo.html',context)


# borrar ceo
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def deleteceo(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect(reverse('dashboard:ceo')+ "?deleted")


# ver detalle editar ceo
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def editceo(request, id):   
    editemployee = Employee.objects.get(id=id)
    holidays = Holiday.objects.filter(employee=editemployee)
    salaries = Salary.objects.filter(employee=editemployee)
    try:
        wage_instance = Salary.objects.get(employee=editemployee, period__month=today.month, period__year=today.year)
    except:
        wage_instance =Salary.objects.filter(employee=editemployee).first()
        
        
    if request.method == "GET":       
        editform = EditEmployeeForm(instance=editemployee)
        editwageform = EditWageCeo(instance=wage_instance) if wage_instance else EditWageCeo()
        
        holydayform = HolidayEmployeeForm()
        context = {
            'holidayform'  : holydayform,
            'editform': editform,
            'editwageform': editwageform,
            'editemployee': editemployee,
            'id': id,
            'holidays': holidays,
            'salaries': salaries,
            }      
        return render (request, 'dashboard/instructor/editceo.html', context)
    
    if request.method == 'POST':
        # editar datos generales de ceo
        if "editemployee" in request.POST:
            editform = EditEmployeeForm(request.POST, instance=editemployee)
            if editform.is_valid():
                editform.save()
                return redirect('dashboard:editceo', id=editemployee.id)
            else:
                return HttpResponse(
                    f"Ups! Something went wrong. You should go back, update the page and try again. \n\n {editform.errors}")
        # nueva vacacion
        if "holiday" in request.POST:
            holydayform = HolidayEmployeeForm(request.POST)
            if holydayform.is_valid():
                holiday = holydayform.save(commit=False)
                holiday.employee = editemployee
                holiday.save()
                return redirect(reverse('dashboard:editceo', kwargs={'id': editemployee.id}) + '#holiday')
            else:
                return HttpResponse(
                    f"Ups! Something went wrong. You should go back, update the page and try again. \n\n {holydayform.errors}")
        # editar salario        
        if "editwage" in request.POST:
            editwageform = EditWageCeo(request.POST, instance=wage_instance) if wage_instance else EditWageCeo(request.POST)
            if editwageform.is_valid():
                wage = editwageform.save(commit=False)
                wage.employee = editemployee
                wage.save()
                return redirect(reverse('dashboard:editceo', kwargs={'id': editemployee.id}) + '#pay')
            else: 
                return HttpResponse(
                    f"Ups! Something went wrong. You should go back, update the page and try again. \n\n {editwageform.errors}")




#######################################################################################################################################################3
## SERVICES
# un servicio es la suscripción mensual (de una sale RR)


# ver detalle de un servicio
@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def editservice(request, id):   
    editservice = get_object_or_404(Service, id=id)
    context = {
        'editservice': editservice,
    }                   
    return render (request, 'dashboard/table/editservice.html', context)


# restaurar un servicio cancelado
@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def restoreservice(request, id):        
    editservice = get_object_or_404(Service, id=id)
    client_id = editservice.client.id
    editservice.state = True
    editservice.save()
    print(f'Service {editservice} restored.')                  
    return redirect ('dashboard:editclient', id=client_id)
            




#####################################################################################################################################
## AJUSTES
# ajustes a los servicios
@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def adj(request):      
    services = Service.objects.filter(state=True)
    accounts = Client.objects.filter(cancelled="Active")
    adjform = AdjForm()
    
    if request.method == "POST" and "adj" in request.POST:
        
        adjform =AdjForm(request.POST)

        if adjform.is_valid():
            
            instance = adjform.save(commit=False)
            
            client_name = adjform.cleaned_data['client']
            client_instance = Client.objects.get(name=client_name)
            instance.client = client_instance
            

            
            if adjform.cleaned_data['type'] == "Service":
                service_name = adjform.cleaned_data['service']
                instance.service = service_name
        
            instance.save() 
                
                 
        else:
            print(adjform)
            print(adjform.errors)
    

    context = {
        'adjform': adjform,
        'services': services,
        'clients': accounts,

    }
    return render (request, 'dashboard/table/adj.html', context)







@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def deleteadj(request, id):
    
    adj = Adj.objects.get(id=id)
    
    if adj.adj_done == False:  
        adj.delete()
    else:
        if adj.type == "Service":
            service = adj.service
            service.total = adj.old_value
            service.save()
        else:
            client = adj.client
            for service in client.services.exclude(state=False):
                corregido = Decimal(service.total / (1 + (adj.adj_percent / 100)))
                service.total = corregido
                service.save()
        adj.delete()        
            
            
    return redirect(reverse('dashboard:adjustment')+ "?deleted")








@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def editadj(request, id):  
      
    adj = Adj.objects.get(id=id)

    if request.method == "GET":
        
        adjform = ChangeAdj(instance=adj)
        context = {
            'adjform': adjform,
            'adj': adj,
            'id': id,
            }
        return render (request, 'dashboard/table/editadj.html', context)

    
    if request.method == 'POST':
        adjform = ChangeAdj(request.POST, instance=adj)
        
        if adjform.is_valid():
            instance = adjform.save(commit=False)
            
            
            client_instance = adj.client
            

            adj_percent = adjform.cleaned_data['adj_percent']

            if adj.type == "Service":
                service = adj.service
                new = Decimal(service.total + ((adj_percent / 100) * service.total))
                instance.new_value = new
                instance.dif = new - service.total               
                
            elif adj.type == "Account":
                services = client_instance.services.filter(state=True)
                total_services = 0
                for service in services:
                    total_services += service.total
                
                new = Decimal(total_services + ((adj_percent / 100) * total_services))
                instance.new_value = new
                instance.dif = new - total_services          
        
            instance.save()
            return redirect('dashboard:adjustment')
        else: 
            return HttpResponse(f"Ups! Something went wrong. You should go back, update the page and try again. \n \n {adjform.errors}")
        
        

@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def adjustment(request):
    
    # adjust services script from adjustment view
    print("")

    print("#######################################")
    print("####################################### ADJUST SERVICES ")

    adj_list = Adj.objects.filter(
                        adj_done=False,
                        notice_date__lte=today
                    )
    if adj_list:
        print(f"############################### adjust list:\n {adj_list}")
        print("##############################################")
        for adj in adj_list:
            if adj.type == "Service":
                service = adj.service
                print(f"######################################### item found -------- --- - -- - > {adj.type} ######")
                print(f"{service}")
                print(f"######################################### old value-- - > {service.total} ######")
                service.total = adj.new_value
                
                service.save() 
                print(f"######################################### new value-- - > {service.total} ######")
                adj.adj_done = True
                adj.save()
                print(f"###### Adjust {service} done ---- > {adj.adj_done} ######")
            elif adj.type == "Account":
                client = adj.client
                print(f"######################################### item found -------- --- - -- - > {adj.type}: {client} ######")
                services = client.services.filter(state=True)
                for service in services:
                    print(f"{service}")
                    print(f"######################################### old value-- - > {service.total} ######")
                    
                    
                    service.total = Decimal(service.total + ((adj.adj_percent / 100) * service.total))

                    service.save() 
                    print(f"######################################### new value-- - > {service.total} ######")
                adj.adj_done = True
                adj.save()
                print(f"###### Adjust {client} done ---- > {adj.adj_done}######")
        print("")
        print(f"############################### done with adjustments ")
        print("############################################################################################")
    else:
        print(f"############################### nothing to adjust ")
    
    services = Service.objects.filter(state=True)
    clients = Client.objects.filter(cancelled="Active")
    adjform = AdjForm()
    adjusts = Adj.objects.all()
    if request.method == "POST" and "adj" in request.POST:
        
        adjform =AdjForm(request.POST)

        if adjform.is_valid():
            
            instance = adjform.save(commit=False)
            
            client_name = adjform.cleaned_data['client']
            client_instance = Client.objects.get(name=client_name)
            instance.client = client_instance
            

            adj_percent = adjform.cleaned_data['adj_percent']

            if adjform.cleaned_data['type'] == "Service":
                service = adjform.cleaned_data['service']
                instance.service = service
                
                instance.old_value = service.total
                new = Decimal(service.total + ((adj_percent / 100) * service.total))
                instance.new_value = new
                instance.dif = new - service.total               
                
            elif adjform.cleaned_data['type'] == "Account":
                services = client_instance.services.filter(state=True)
                total_services = 0
                for service in services:
                    total_services += service.total
                
                instance.old_value = total_services
                new = Decimal(total_services + ((adj_percent / 100) * total_services))
                instance.new_value = new
                instance.dif = new - total_services          
        
            instance.save()
            return redirect('dashboard:adjustment') 
                
                 
        else:
            print(adjform.errors) 

    context = {
        'services': services,
        'clients': clients,
        "page_title":"ADJUSTMENTS",
        'adjform':adjform,
        'adjusts': adjusts,

    }
    return render (request, 'dashboard/table/adjustments.html', context)











#####################################################################################################################################
## VENTAS

## función para exportar ventas para excel
@login_required(login_url='dashboard:login')
def export_sales(request):
    dataset = ExportSales().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales.xlsx"'
    return response


@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def sales(request):
    clients = Client.objects.all()
    services = ['SEO','Google Ads','Facebook Ads','Web Design', 'Hosting', 'LinkedIn', 'SSL certificate','Web Plan','Combo', 'Community Management', 'Email Marketing', 'Others', 'Others RR']
    this_month = today.month
    month_name = date(1900, this_month, 1).strftime('%B')
    
    sales_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, revenue="RR").exclude(note="auto revenue sale")
    
    total_amount = sales_this_month.aggregate(Sum('change'))['change__sum']
    
    def get_total_format():
        try:
            return '{:,.0f}'.format(total_amount)
        except: return 0

    sales1_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, revenue="OneOff").exclude(note="auto revenue sale")
    total1_amount = sales1_this_month.aggregate(Sum('change'))['change__sum']
    def get_total1_format():
        try:
            return '{:,.0f}'.format(total1_amount)
        except: return 0
        
    clients_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, kind="New Client").exclude(note="auto revenue sale")
    total_clients = clients_this_month.count()
    
    
    upsell_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, kind="Upsell").exclude(note="auto revenue sale")
    total_upsell_this_month = upsell_this_month.count()
    
    crosssell_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, kind="Cross Sell").exclude(note="auto revenue sale")
    total_crosssell_this_month = crosssell_this_month.count()
    
    sales = Sale.objects.filter(date__month=today.month, date__year=today.year)
        
        
        
    if request.method == 'GET':
        initial_data = {}
        client_id = request.GET.get('client')
        if client_id:
            initial_data['client'] = client_id
        addform = SaleForm2(initial=initial_data)

    if request.method == 'POST':
        if "addsale" in request.POST:
            client_name = request.POST.get('client')
            addform = SaleForm2(request.POST)

            if addform.is_valid():
                instance = addform.save(commit=False)
                client_instance = Client.objects.get(name=client_name)
                instance.client = client_instance
                instance.save()
                return redirect(reverse('dashboard:sales') + "?added")
            else:
               
                return HttpResponse(f"Ups! Something went wrong: \n\n {addform.errors}")

                
            
            
            
    
    sales_by_service =Sale.objects.filter(date__month=today.month, date__year=today.year).exclude(note="auto revenue sale")

    s_seo = 0
    s_gads= 0
    s_fads= 0
    s_lin= 0
    s_cm = 0
    s_combo = 0
    s_webp = 0
    s_other = 0
    s_web = 0
    s_hos = 0
    s_ssl = 0
    s_em = 0
    s_other1 = 0
    

    for sale in sales_by_service:
        if sale.service == "SEO":
            s_seo += sale.get_change
        elif sale.service == "Google Ads":
            s_gads += sale.get_change
        elif sale.service == "Facebook Ads":
            s_fads += sale.get_change
        elif sale.service == "LinkedIn":
            s_lin  += sale.get_change
        elif sale.service == "Community Management":
            s_cm  += sale.get_change
        elif sale.service == "Combo":
            s_combo  += sale.get_change
        elif sale.service == "Web Plan":
            s_webp += sale.get_change
        elif sale.service == "Others RR":
            s_other += sale.get_change
        elif sale.service == "Web Design":
            s_web += sale.get_change
        elif sale.service == "Hosting":
            s_hos += sale.get_change
        elif sale.service == "SSL certificate":
            s_ssl += sale.get_change
        elif sale.service == "Email Marketing":
            s_em += sale.get_change
        elif sale.service == "Others":
            s_other1 += sale.get_change
            
        else: pass

                
    context={
        "clients": clients,
        "page_title":"SALES",
        "sales" : sales,
        "sales_this_month" : get_total_format,
        "sales1_this_month" : get_total1_format,
        "clients_this_month" : total_clients,
        "this_month": month_name,
        'upsell': total_upsell_this_month,
        'cross': total_crosssell_this_month,
        'services': services,
        "addform" : addform,
        "total_seo" : '{:,.0f}'.format(s_seo),
        "total_googleads" : '{:,.0f}'.format(s_gads),
        "total_facebookads" : '{:,.0f}'.format(s_fads),
        "total_linkedin" : '{:,.0f}'.format(s_lin),
        "total_communitymanagement" : '{:,.0f}'.format(s_cm),
        "total_combo" :'{:,.0f}'.format(s_combo),
        "total_webplan" :'{:,.0f}'.format(s_webp), 
        "total_otherrr" : '{:,.0f}'.format(s_other),
        "total_webdesign" :'{:,.0f}'.format(s_web),
        "total_hosting":'{:,.0f}'.format(s_hos),
        "total_sslcertificate": '{:,.0f}'.format(s_ssl),
        "total_emailmarketing" :'{:,.0f}'.format(s_em),
        "total_other" : '{:,.0f}'.format(s_other1)
    }
    return render(request,'dashboard/table/sales.html',context)

@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def salesdata(request):
    sales_rr_current_year = Sale.objects.filter(revenue="RR")\
                                        .filter(date__year=datetime.now().date().year)
    total_rr_this_year = 0
    for s in sales_rr_current_year:
        total_rr_this_year += s.get_change
            
    enero = 0
    febrero = 0
    marzo = 0
    abril = 0
    mayo = 0
    junio = 0
    julio = 0
    agosto = 0
    septiembre = 0
    octubre = 0
    noviembre = 0
    diciembre = 0
    
    for sale in sales_rr_current_year:
        if sale.date.month == 1:
            enero +=sale.get_change
            
        elif sale.date.month == 2:
            febrero +=sale.get_change
        elif sale.date.month == 3:
            marzo +=sale.get_change
        elif sale.date.month == 4:
            abril +=sale.get_change
        elif sale.date.month == 5:
            mayo +=sale.get_change
        elif sale.date.month == 6:
            junio +=sale.get_change
        elif sale.date.month == 7:
            julio +=sale.get_change
        elif sale.date.month == 8:
            agosto +=sale.get_change
        elif sale.date.month == 9:
            septiembre +=sale.get_change
        elif sale.date.month == 10:
            octubre +=sale.get_change
        elif sale.date.month == 11:
            noviembre +=sale.get_change
        else:
            diciembre +=sale.get_change
            
            
    context={
        "total_rr_this_year": total_rr_this_year,
        "enero" : enero,
        "febrero": febrero,
        "marzo": marzo,
        "abril": abril,
        "mayo": mayo,
        "junio": junio,
        "julio": julio,
        "agosto": agosto,
        "septiembre": septiembre,
        "octubre": octubre,
        "noviembre": noviembre,
        "diciembre": diciembre
    }
    
    "SALES RR Y 1OFF BY YEAR AND MONTH"
    "SERVICES BY YEAR AND MONTH"
    "KIND AND SOURCE BY YEAR AND MONTH"
    
    return render(request,'dashboard/table/salesdata.html', context)







@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def deletesale(request, id):
    sale = Sale.objects.get(id=id)
    # update asociated suscription values       
    print("look for service asociated")

    try:

        servicio = sale.suscription
        print(f"service finded {servicio}, sustracting sale price {sale.change} from service total {servicio.total}")

        servicio.total -= sale.change
        print(f'new total: {servicio.total}')
        if servicio.total < 1:
            print("service total is less than 1, deleting service...")
            servicio.delete()
            print("done")
        else: 
            print("service total is biggetr than 1, saving service")
            servicio.save()
            print("done")
        
    except:
        print("cant find associated service")
        pass
    print("deleting the sale")
    
    sale.delete()
    return redirect(reverse('dashboard:sales')+ "?deleted")


@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def editsale(request, id):
    
    editsale = Sale.objects.get(id=id)
    service = editsale.suscription
    if request.method == "GET":
        
        editform = EditSaleForm(instance=editsale)
        context = {
            'editform': editform,
            'editsale': editsale,
            'id': id,
            }
        return render (request, 'dashboard/table/editsale.html', context)

    
    if request.method == 'POST':
        editform = EditSaleForm(request.POST, instance=editsale)
        if editform.is_valid():
            antiguo = editsale.change
            print(f'precio anterior de la venta: {antiguo}') 
            sale = editform.save() 
            if service is not None:
                print(f'total atual del servicio {service.total}')
                service.total -= antiguo
                
                print(f'restar el valor viejo de la venta: {antiguo}')
                service.save()
                print(f'SERVICIO GUARDADO total sin precio antiguo {service.total}')

                print(f'precio nueva de la venta: {sale.change}')
                print(f'sumar el nuevo valor al nuevo total {service.total}+ {sale.change}')

                service.total += sale.change

                service.save() 
                print(service.total)
                
                
            else:
                print("not service asocciated")
            sale.save() 
                
                
            return redirect('dashboard:editsale', id=editsale.id)
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")

## exportación de todos los clientes para excel
@login_required(login_url='dashboard:login')
def export_clients(request):
    dataset = ClientResource().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="clients.xlsx"'
    return response


## exportación de las cuentas rr activas
@login_required(login_url='dashboard:login')
def export_rr(request):
    dataset = ExportRR().export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="rr.xlsx"'
    return response






@user_passes_test(lambda user: user.groups.filter(name='clients').exists())
@login_required(login_url='dashboard:login')
def clients(request):
    clients_all = Client.objects.filter(cancelled="Active")
    clients = []
    for client in clients_all:
        if client.services.filter(state=True).exists():
            clients.append(client)
        
    total_rr = 0
    for client in clients:
        if client.cancelled == "Active":
            for service in client.services.filter(state=True):
                total_rr += service.total                
    total_rr_k = total_rr
    
    
    clients_rr = []
    for client in clients_all.filter(cancelled="Active"):
        if client.services.filter(state=True).exists():
            clients_rr.append(client.id)
    c_rr_total = len(clients_rr)

    if len(clients_rr) > 0:
        formula = total_rr/c_rr_total
    else:
        formula = 0
        
       
    addform=ClientForm()
    if request.method == 'GET':
        addform = ClientForm()
    if request.method == 'POST':
        if "addclient" in request.POST:
            addform = ClientForm(request.POST)
            print(addform.errors)
            if addform.is_valid():
                newclient = addform.save()
                return redirect('dashboard:editclient', id=newclient.id)
            else:
                return HttpResponse("hacked from las except else form")
    
    
    services = Service.objects.filter(state=True)
    s_seo = 0
    s_gads= 0
    s_fads= 0
    s_lin= 0
    s_cm = 0
    s_combo = 0
    s_webp = 0
    s_other = 0
    

    for sale in services:
        if sale.service == "SEO":
            s_seo += sale.total
        elif sale.service == "Google Ads":
            s_gads += sale.total
        elif sale.service == "Facebook Ads":
            s_fads += sale.total
        elif sale.service == "LinkedIn":
            s_lin  += sale.total
        elif sale.service == "Community Management":
            s_cm  += sale.total
        elif sale.service == "Combo":
            s_combo  += sale.total
        elif sale.service == "Web Plan":
            s_webp += sale.total
        elif sale.service == "Others":
            s_webp += sale.total
        else: pass

    get_incomes_by_service = [s_seo, s_gads, s_fads, s_lin, s_cm, s_combo, s_webp, s_other]
    
    t1=0
    t2=0
    t3=0
    t4=0
    t5=0

    for sale in services:
        
        if sale.client.tier == "I":
            
            t1 += sale.total
        elif sale.client.tier == "II":
            t2 += sale.total
        elif sale.client.tier == "III":
            t3 += sale.total
        elif sale.client.tier == "IV":
            t4 += sale.total
        elif sale.client.tier == "V":
            t5 += sale.total
        else: pass
    get_incomes_by_tier = [t1, t2, t3, t4, t5]      
    
    context={
        "total_rr": total_rr,
        "clients" : clients,
        "addform": addform,
        "c_rr_total":c_rr_total,
        "total_rr_k":total_rr_k,
        'get_incomes_by_service' : get_incomes_by_service,
        'get_incomes_by_tier' : get_incomes_by_tier,
        'seo' : s_seo,       
        'gads': s_gads,
        'fads' : s_fads,
        'lin' : s_lin ,
        'cm' : s_cm ,
        'combo' : s_combo,
        'web' : s_webp,
        'formula': formula,
        "page_title":"RR ACCOUNTS",
    }
    return render(request,'dashboard/instructor/clients.html',context)



@user_passes_test(lambda user: user.groups.filter(Q(name='sales')).exists())
@login_required(login_url='dashboard:login')
def cancellations(request):
    
    
    this_month = today.month
    month = date(1900, this_month, 1).strftime('%B')
    
    clients_cancelled = Client.objects.filter(cancelled="Cancelled")
    services_cancelled = Service.objects.filter(state=False)
    services_this_month = services_cancelled.filter(date_can__month=today.month, client__cancelled="Active")
    clients_this_month = clients_cancelled.filter(date_can__month=today.month)


    total_amount = services_cancelled.filter(date_can__month=today.month).aggregate(Sum('total'))['total__sum']
    def get_total_format():
        try:
            return '{:,.0f}'.format(total_amount)
        except: return 0
    
    context={
        "clients_cancelled": clients_cancelled,
        "services_cancelled" : services_cancelled,
        "month" : month,
        "sales" : services_this_month.count(),
        "clients": clients_this_month.count(),
        "total": get_total_format,       
        "page_title":"Cancellations"
    }   
    
    return render(request,'dashboard/instructor/cancellations.html',context)


@user_passes_test(lambda user: user.groups.filter(name='clients').exists())
@login_required(login_url='dashboard:login')
def deleteclient(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect(reverse('dashboard:clients')+ "?deleted")



@user_passes_test(lambda user: user.groups.filter(name='clients').exists())
@login_required(login_url='dashboard:login')
def delete_clients(request):
    if request.method == 'POST' and 'delete' in request.POST:
        selected_ids = request.POST.getlist('selected_clients')
        Client.objects.filter(id__in=selected_ids).delete()
        return redirect('dashboard:clients')
    else:
        return HttpResponseBadRequest('Invalid request')

@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def delete_sales(request):
    if request.method == 'POST' and 'delete' in request.POST:
        selected_ids = request.POST.getlist('selected_sales')
        # update asociated suscription values    
        for sale in Sale.objects.filter(id__in= selected_ids):
            print(f"deleting {sale}")       
            print("look for service asociated")
        
            try:

                servicio = sale.suscription
                print(f"service finded {servicio}, sustracting sale price {sale.change} from service total {servicio.total}")

                servicio.total -= sale.change
                print(f'new total: {servicio.total}')
                if servicio.total < 1:
                    print("service total is less than 1, deleting service...")
                    servicio.delete()
                    print("done")
                else: 
                    print("service total is biggetr than 1, saving service")
                    servicio.save()
                    print("done")
                
            except:
                print("cant find associated service")
                pass
            print("deleting the sale")
        
        Sale.objects.filter(id__in=selected_ids).delete()
        return redirect('dashboard:sales')
    else:
        return HttpResponseBadRequest('Invalid request')
    
    
@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def delete_expenses(request):
    if request.method == 'POST' and 'delete' in request.POST:
        selected_ids = request.POST.getlist('selected_expenses')
        Expense.objects.filter(id__in=selected_ids).delete()
        return redirect('dashboard:expenses')
    else:
        return HttpResponseBadRequest('Invalid request')    


@user_passes_test(lambda user: user.groups.filter(name='clients').exists())
@login_required(login_url='dashboard:login')
def editclient(request, id):
    
    editclient = Client.objects.get(id=id)

    if request.method == "GET":
        sales = editclient.sales.exclude(note="auto revenue sale")
        services = editclient.services.all()
        editform = EditClientForm(instance=editclient)
        cancelform = CancellService()
        context = {
            'editform': editform,
            'editclient': editclient,
            'cancelform': cancelform,
            'id': id,
            'sales': sales,
            'services': services,
            }
        return render (request, 'dashboard/instructor/editclient.html', context)

    
    if request.method == 'POST':
        if 'editclient' in request.POST:
            editform = EditClientForm(request.POST, instance=editclient)
            if editform.is_valid():
                clientedit = editform.save(commit=False)
                if clientedit.cancelled == "Cancelled":
                    for sale in clientedit.services.all():
                        sale.state = False
                        sale.comment_can = clientedit.comment_can
                        sale.fail_can = clientedit.fail_can
                        sale.date_can = clientedit.date_can
                        sale.save()
                clientedit.save()
                return redirect('dashboard:editclient', id=clientedit.id)
            else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
            
        if 'cancelservice' in request.POST:
            
            cancelform = CancellService(request.POST)
            if cancelform.is_valid():
                id = cancelform.cleaned_data['id']
                instance = Service.objects.get(id=id)
                instance.state = False
                instance.comment_can = cancelform.cleaned_data['comment_can']
                instance.date_can = cancelform.cleaned_data['date_can']
                instance.fail_can = cancelform.cleaned_data['fail_can']
                instance.save()
                return redirect('dashboard:editclient', id=instance.client.id)

            else:
                print(cancelform.errors)
                return HttpResponse(f"something get wrong: {cancelform.errors}")    
        
        
        
@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def addclientsale(request, id):
    
    client = Client.objects.get(id=id)

    if request.method == "GET":
        
        addclientsaleform = ClientSaleForm()
        context = {
            'addclientsaleform': addclientsaleform,
            'client': client,
            }
        return render (request, 'dashboard/instructor/addclientsale.html', context)

    
    if request.method == 'POST':
        addclientsaleform = ClientSaleForm(request.POST)
              
        if addclientsaleform.is_valid():
            instance = addclientsaleform.save(commit=False)
            instance.client=client
            instance.save()
           
            return redirect('dashboard:editclient', id=client.id)

        else:

            print (addclientsaleform.errors) 
            return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        
        





@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.delete_configurations'}, raise_exception=True)
def delete_config(request,id):
    config_obj = Configurations.objects.get(id=id)
    if config_obj:
        config_obj.delete()
        setup_config.updateConfig()
        messages.success(request, "Configuration Delete Successfully") 
    else:
        messages.error(request, "Configuration Not Valid") 

    return redirect("dashboard:all-config")



def count(d):
    return max(count(v) if isinstance(v,dict) else 0 for v in d.values()) + 1


@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.delete_configurations','dashboard.add_configurations'}, raise_exception=True)
def reset_config(request):
    path = "configurations/config.json"
    full_path = os.path.join(settings.BASE_DIR,path)
    Configurations.objects.all().delete()

    with open(full_path,'r') as f:
        configdata = json.load(f)
       
        for key1, value1 in configdata.items():
            if count(value1) == 2:
                for key2, value2 in value1.items():
                    name = key1+"."+key2
                    value = value2.get('value')
                    title = value2.get('title')
                    description = value2.get('description')
                    input_type = value2.get('input_type')
                    editable = value2.get('editable')
                    order = value2.get('order')
                    params = value2.get('params')
                    config_obj = Configurations(
                                    name=name,
                                    value=value,
                                    title=title,
                                    description=description,
                                    input_type=input_type,
                                    editable=editable,
                                    order=order,
                                    params=params
                                )
                    config_obj.save()
    setup_config.updateConfig()
    return redirect("dashboard:all-config")
        
        


@login_required(login_url='dashboard:login')
def download_config(request):
    path = "configurations/Config"
    pickle_file_path = os.path.join(settings.BASE_DIR, path)
   
    dbfile = open(pickle_file_path, 'rb')
    config_data = pickle.load(dbfile)
    dbfile.close()
    
    json_file_path =os.path.join(settings.BASE_DIR,'configurations/config.json')
    json_file = open(json_file_path,'w')
    json_file.write(json.dumps(config_data,indent=4))
    json_file.close()
    mime_type, _ = mimetypes.guess_type(json_file_path)
    
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as fh:
            response = HttpResponse(fh, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % 'config.json'
            return response
    raise Http404



#######################################################################################



@login_required(login_url='dashboard:login')
def index(request):
    #######################################################################################
    ########### PROCESOS EN SEGUNDO PLANO PARA CRONJOBS
    
    
    
    #############          B A C K U P S        #####################
    try :
        last_backup = BackUps.objects.get(id=1)
        if last_backup.date.month != today.month:
            print("doing back up")
            
            
            export_sales()
            export_clients()
            export_employees()
            export_expenses()
            export_holidays()
            
            last_backup.date = today
            last_backup.save()
        else:
            print("don't need to back up, allready updated")
    except: last_backup = BackUps.objects.create(id=1)    
    
    try:
        auto  = AutoRevenue.objects.get(pk=1)
                
    except:
        auto = AutoRevenue.objects.create(
                pk=1,
                date=today,
                sales=True,
                wages=True,
                expenses=True,                                 
            )            
        
    if auto.date.month != today.month:
        auto.date=today
        auto.sales=True
        auto.wages=True
        auto.expenses=True
        auto.save()

        staff = Employee.objects.filter(active="Yes")
        for employee in staff:
            try:
                last_salary = employee.salaries.last()
                if last_salary.period.month != today.month:
                    new_salary = Salary.objects.create(
                    employee=last_salary.employee,
                    period=today,
                    salary=last_salary.salary,
                    nigga=last_salary.nigga,
                    mp=last_salary.mp,
                    tc=last_salary.tc,
                    cash=last_salary.cash,
                    atm_cash=last_salary.atm_cash,
                    cash_usd=last_salary.cash_usd,
                    paypal=last_salary.paypal,
                )
            
            except:
                pass

                
        expenses_list = Expense.objects.filter(date__month=today.month-1, date__year=today.year)
        for expense in expenses_list:    
            if expense.date.month != today.month:
                update_expense = Expense.objects.create(
                date=today,
                category=expense.category,
                concept=expense.concept,
                value=expense.value,
                currency=expense.currency,
                wop=expense.wop,
            )
        
    #######################################################################################    
    # ACTUALIZACIÓN DEL DOLAR BLUE
    # ESTO TIENE QUE IR A UN CRONJOB'
    last_blue = 490
    try:
        last_blue =  LastBlue.objects.get(pk=1)
        blue = last_blue.venta
    # si aun  no se creo ningún valor de cotización crearlo
    except:
        last_blue = LastBlue.objects.create(
            venta = 490
        )
    # solicitar a la api de dolarhoy para mantener actualizado el valor de la venta
    # b_venta viene de dashboard.services.py
    try:
        blue = b_venta
        if last_blue.venta != b_venta:
                last_blue.venta = b_venta
        last_blue.save()
        
    except: # si la api no esta disponible devolver el ultimo valor guardado en la db
        blue = last_blue.venta
    #############33
    
    

       
       
       
    ##############################################    ##############################################

    print("##############################################")
    print("##############################################")
    print("##############################################  ADJUSTMENTS")

    #  internal reminder ----adjust client------ for email send 
    print("#######################################")
    print("####################################### REMINDER ")
    
    remind_list = Adj.objects.filter(
                        adj_done=False,
                        remind_sent = False,
                        email_date__lte=today
                    )
    if remind_list:
        for adj in remind_list:
            if adj.type == "Service":
                service = adj.service
                print(f"######################################### REMIND found -------- --- - -- - > {adj.type} {service} ######")
                print(f"######################################### values- - > OLD {service.total} NEW {adj.new_value} ######")
                
                email_message = render_to_string('dashboard/email_adjust_service_template.html', {'adj': adj})
                actual = Decimal(adj.old_value)
                con = Decimal(adj.new_value)
                ajuste = Decimal(adj.dif)
                try:
                    send_mail(
                        subject='Aviso: IMPORTANTE',
                        message=f'({adj.notice_date} {adj.client.name} {adj.client.admin_email} {adj.service.service}) \n Estimado cliente,  \n  El motivo de este email es para comunicarte un ajuste por inflación.\n Inversión actual: ${actual} \n Inversión con ajuste: ${con} \n Ajuste: ${ajuste} \n El ajuste se hará en el próximo pago. \n Cualquier duda no dejes de consultarnos. \n Saludos, \n Imactions \n www.imactions.agency',
                        html_message=email_message,
                        from_email='systemimactions@gmail.com',
                        recipient_list=['hola@imactions.com'],
                        fail_silently=False,
                    )
                    print (f" adjust -- {adj} - {service} -- EMAIL reminder SEND")
                    adj.remind_sent = True
                    adj.save()
                except:
                    print("cant send email for adj, you  must be on dev")

                
            elif adj.type == "Account":
                client = adj.client
                print(f"######################################### REMIND found -------- --- - -- - > {adj.type}: {client} ######")
                services = client.services.filter(state=True)
                services_list = []
                for service in services:
                    print(f"{service}")
                    services_list.append(service.service)
                    
                    
                email_message = render_to_string('dashboard/email_adjust_account_template.html', {'adj': adj, 'services': services})
                actual = Decimal(adj.old_value)
                con = Decimal(adj.new_value)
                ajuste = Decimal(adj.dif)
                try:
                    send_mail(
                        subject='Aviso: IMPORTANTE',
                        message=f'({adj.notice_date} {adj.client.name} {adj.client.admin_email} {services_list}) \n Estimado cliente, \n El motivo de este email es para comunicarte un ajuste por inflación.\n  \n Inversión actual: ${actual} \n Inversión con ajuste: ${con} \n Ajuste: ${ajuste} \n El ajuste se hará en el próximo pago. \n Cualquier duda no dejes de consultarnos. \n Saludos, \n Imactions \n www.imactions.agency',
                        html_message=email_message,
                        from_email='systemimactions@gmail.com',
                        recipient_list=['hola@imactions.com'],
                        fail_silently=False,
                    )
                    print (f" adjust -- {adj} - {client} -- EMAIL reminder SEND")
                    adj.remind_sent = True
                    adj.save()
                except:
                    print("cant send email you must be in dev")
                    
                    
                    
    print("##############         end reminders             ###############")

                
                


    # adjust services script from adjustment view
    print("")

    print("#######################################")
    print("####################################### ADJUST SERVICES ")

    adj_list = Adj.objects.filter(
                        adj_done=False,
                        notice_date__lte=today
                    )
    if adj_list:
        print(f"############################### adjust list:\n {adj_list}")
        print("##############################################")
        for adj in adj_list:
            if adj.type == "Service":
                service = adj.service
                print(f"######################################### item found -------- --- - -- - > {adj.type} ######")
                print(f"{service}")
                print(f"######################################### old value-- - > {service.total} ######")
                service.total = adj.new_value
                
                service.save() 
                print(f"######################################### new value-- - > {service.total} ######")
                adj.adj_done = True
                adj.save()
                print(f"###### Adjust {service} done ---- > {adj.adj_done} ######")
            elif adj.type == "Account":
                client = adj.client
                print(f"######################################### item found -------- --- - -- - > {adj.type}: {client} ######")
                services = client.services.filter(state=True)
                for service in services:
                    print(f"{service}")
                    print(f"######################################### old value-- - > {service.total} ######")
                    
                    
                    service.total = Decimal(service.total + ((adj.adj_percent / 100) * service.total))

                    service.save() 
                    print(f"######################################### new value-- - > {service.total} ######")
                adj.adj_done = True
                adj.save()
                print(f"###### Adjust {client} done ---- > {adj.adj_done}######")
        print("")
        print(f"############################### done with adjustments ")
        print("############################################################################################")
    else:
        print(f"############################### nothing to adjust ")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ###############
    # birthdays
    bds = []
    employees = Employee.objects.filter(active="Yes")
    for e in employees:
        try:
            if today.month == e.dob.month and today.day == e.dob.day:
                bds.append(e)
        except:
            pass
    #######################################################################################
    # card activity
    ct = ContentType.objects.get_for_model(LastBlue)
    ct2 = ContentType.objects.get_for_model(CustomUser)

    events = CRUDEvent.objects.exclude(content_type=ct).exclude(content_type=ct2)
    
    
    last_act = events[:7]   
    
    #######################################################################################
    # RR CLIENTS --- $
    rr_t_clients = 0
    rr_q_clients_list = []

    clients = Client.objects.filter(cancelled="Active")
    for client in clients:
        if client.total_rr > 0 and client not in rr_q_clients_list:
            rr_q_clients_list.append(client)
        services = client.services.filter(state=True)
        for service in services:
            rr_t_clients += service.total
    
    rr_q_clients = len(rr_q_clients_list)
    
    
    #######################################################################################
    # BALANCE --- $
    outcome = 0
    expenses = Expense.objects.filter(date__month=today.month, date__year=today.year)
    salaries = Salary.objects.filter(period__month=today.month, period__year=today.year)
    for salary in salaries:
        if salary.employee.rol != "CEO":
            outcome +=  salary.employee.get_total()
        else:
            try:
                outcome += salary.employee.get_total_ceo()
            except:
                pass
    for e in expenses:
        try:
            if e.change is not None and e.change > 0:
                outcome += e.change
            else:
                outcome += e.value
        except:
            pass
    balance = rr_t_clients - outcome

    #######################################################################################

    #######################################################################################

    # SALES RR THIS MONTH --- $
    # SALES 1OFF THIS MONTH --- $
    this_month = today.month
    month = date(1900, this_month, 1).strftime('%B')
    rr_s_thism = 0
    oneoff_s_thism = 0
    sales_this_m = Sale.objects.filter(date__month=today.month, date__year=today.year)
    if sales_this_m:
        for sale in sales_this_m:
            if sale.revenue == "RR":
                rr_s_thism += sale.change
            else:
                oneoff_s_thism += sale.change
    #######################################################################################

    # CANCELL THIS MONTH --- Q
    clients_cancelled = Client.objects.filter(cancelled="Cancelled")
    sales_cancelled = Service.objects.filter(state=False)
    sales_c_this_m = sales_cancelled.filter(date_can__month=today.month, date_can__year=today.year, client__cancelled="Active")
    clients_c_this_m = clients_cancelled.filter(date_can__month=today.month, date_can__year=today.year)
    cancellations = []
    for sale in sales_c_this_m:
        cancellations.append(sale)
    for client in clients_c_this_m:
        cancellations.append(client)
    cancell_q = len(cancellations)
       
       
    #######################################################################################
    clients = Client.objects.filter(cancelled="Active")
    
    clients_rr = []
    for client in clients:
        if client.get_rr_client == True:
            clients_rr.append(client)
    c_rr_total = len(clients_rr)
    
    #  % clients by service    -  pie chart data
               
    seo_clients = Service.objects.filter(service="SEO", state=True).count()
    gads_clients = Service.objects.filter(service="Google Ads", state=True).count()
    fads_clients = Service.objects.filter(service="Facebook Ads", state=True).count()
    lkdn_clients = Service.objects.filter(service="LinkedIn", state=True).count()
    wp_clients = Service.objects.filter(service="Web Plan", state=True).count()
    combo_clients = Service.objects.filter(service="Combo", state=True).count()
    cm_clients = Service.objects.filter(service="Community Management", state=True).count()
    emk_clients = Service.objects.filter(service="Email Marketing", state=True).count()
    other_clients = Service.objects.filter(service="Others RR", state=True).count() 
    
    s_c = 0
    g_c = 0
    f_c = 0
    l_c = 0
    w_c = 0
    co_c = 0
    cm_c = 0
    e_c = 0             
    o_c = 0   
    
    try:
        s_c = (seo_clients*100)/c_rr_total
        g_c = (gads_clients*100)/c_rr_total
        f_c = (fads_clients*100)/c_rr_total
        l_c = (lkdn_clients*100)/c_rr_total
        w_c = (wp_clients*100)/c_rr_total
        co_c = (combo_clients*100)/c_rr_total
        cm_c = (cm_clients*100)/c_rr_total
        e_c = (emk_clients*100)/c_rr_total
        o_c = (other_clients*100)/c_rr_total

    except:
        pass
    
    ####################################################################
    #######################                 GET CLIENTS RR    ##########

    clients = Client.objects.filter(cancelled="Active")
    
    clients_rr = []
    for client in clients:
        if client.get_rr_client == True:
            clients_rr.append(client)
    c_rr_total = len(clients_rr)

    
    ####################################################################
    ###############################################
    ############### CLIENTS BY TIER PieCHART
        
    n_clients = len(clients_rr)
    i = 0
    ii = 0
    iii = 0
    iv = 0
    for client in clients_rr:
        if client.tier == "I":
            i += 1
        elif client.tier == "II":
            ii += 1
        elif client.tier == "III":
            iii += 1
        elif client.tier == "IV":
            iv += 1
    t_i = 0
    t_ii = 0
    t_iii = 0
    t_iv = 0
    try:
        t_i = (i*100)/n_clients
        t_ii = (ii*100)/n_clients
        t_iii = (iii*100)/n_clients
        t_iv = (iv*100)/n_clients
    except:
        pass
    

####################################################################
    total_rr = 0

    for client in clients:
        if client.cancelled == "Active":
            for sale in client.services.filter(state=True):
                total_rr += sale.total           
        
    ##############################################

    # GRAPHS rr   
    sales_rr_current_year = Sale.objects.filter(revenue="RR")\
                                        .filter(date__year=datetime.now().date().year)
    total_rr_this_year = 0
    for s in sales_rr_current_year:
        total_rr_this_year += s.get_change
    
    enero = 0
    febrero = 0
    marzo = 0
    abril = 0
    mayo = 0
    junio = 0
    julio = 0
    agosto = 0
    septiembre = 0
    octubre = 0
    noviembre = 0
    diciembre = 0
    
    for sale in sales_rr_current_year:
        if sale.date.month == 1:
            enero +=sale.get_change
            
        elif sale.date.month == 2:
            febrero +=sale.get_change
        elif sale.date.month == 3:
            marzo +=sale.get_change
        elif sale.date.month == 4:
            abril +=sale.get_change
        elif sale.date.month == 5:
            mayo +=sale.get_change
        elif sale.date.month == 6:
            junio +=sale.get_change
        elif sale.date.month == 7:
            julio +=sale.get_change
        elif sale.date.month == 8:
            agosto +=sale.get_change
        elif sale.date.month == 9:
            septiembre +=sale.get_change
        elif sale.date.month == 10:
            octubre +=sale.get_change
        elif sale.date.month == 11:
            noviembre +=sale.get_change
        else:
            diciembre +=sale.get_change
            
            
    sales_rr_last_year = Sale.objects.filter(revenue="RR")\
                                        .filter(date__year=datetime.now().date().year-1)
    total_rr_last_year = 0
    for s in sales_rr_last_year:
        total_rr_last_year += s.get_change
    
    enero_l = 0
    febrero_l = 0
    marzo_l = 0
    abril_l = 0
    mayo_l = 0
    junio_l = 0
    julio_l = 0
    agosto_l = 0
    septiembre_l = 0
    octubre_l = 0
    noviembre_l = 0
    diciembre_l = 0
    
    for sale in sales_rr_last_year:
        if sale.date.month == 1:
            enero_l +=sale.get_change            
        elif sale.date.month == 2:
            febrero_l +=sale.get_change
        elif sale.date.month == 3:
            marzo_l +=sale.get_change
        elif sale.date.month == 4:
            abril_l +=sale.get_change
        elif sale.date.month == 5:
            mayo_l +=sale.get_change
        elif sale.date.month == 6:
            junio_l +=sale.get_change
        elif sale.date.month == 7:
            julio_l +=sale.get_change
        elif sale.date.month == 8:
            agosto_l +=sale.get_change
        elif sale.date.month == 9:
            septiembre_l +=sale.get_change
        elif sale.date.month == 10:
            octubre_l +=sale.get_change
        elif sale.date.month == 11:
            noviembre_l +=sale.get_change
        else:
            diciembre_l +=sale.get_change           
            
            
    # GRAPHS ONEOFF   
    sales_one_current_year = Sale.objects.filter(revenue="OneOff")\
                                        .filter(date__year=datetime.now().date().year)
    total_one_this_year = 0
    for s in sales_one_current_year:
        total_one_this_year += s.get_change
    
    enero_o = 0
    febrero_o = 0
    marzo_o = 0
    abril_o = 0
    mayo_o = 0
    junio_o = 0
    julio_o = 0
    agosto_o = 0
    septiembre_o = 0
    octubre_o = 0
    noviembre_o = 0
    diciembre_o = 0
    
    for sale in sales_one_current_year:
        if sale.date.month == 1:
            enero_o +=sale.get_change
            
        elif sale.date.month == 2:
            febrero_o +=sale.get_change
        elif sale.date.month == 3:
            marzo_o +=sale.get_change
        elif sale.date.month == 4:
            abril_o +=sale.get_change
        elif sale.date.month == 5:
            mayo_o +=sale.get_change
        elif sale.date.month == 6:
            junio_o +=sale.get_change
        elif sale.date.month == 7:
            julio_o +=sale.get_change
        elif sale.date.month == 8:
            agosto_o +=sale.get_change
        elif sale.date.month == 9:
            septiembre_o +=sale.get_change
        elif sale.date.month == 10:
            octubre_o +=sale.get_change
        elif sale.date.month == 11:
            noviembre_o +=sale.get_change
        else:
            diciembre_o +=sale.get_change
            
            
    sales_one_last_year = Sale.objects.filter(revenue="OneOff")\
                                        .filter(date__year=datetime.now().date().year-1)
    total_one_last_year = 0
    for s in sales_one_last_year:
        total_one_last_year += s.get_change
    
    enero_l_o = 0
    febrero_l_o = 0
    marzo_l_o = 0
    abril_l_o = 0
    mayo_l_o = 0
    junio_l_o = 0
    julio_l_o = 0
    agosto_l_o = 0
    septiembre_l_o = 0
    octubre_l_o = 0
    noviembre_l_o = 0
    diciembre_l_o = 0
    
    for sale in sales_one_last_year:
        if sale.date.month == 1:
            enero_l_o +=sale.get_change            
        elif sale.date.month == 2:
            febrero_l_o +=sale.get_change
        elif sale.date.month == 3:
            marzo_l_o +=sale.get_change
        elif sale.date.month == 4:
            abril_l_o +=sale.get_change
        elif sale.date.month == 5:
            mayo_l_o +=sale.get_change
        elif sale.date.month == 6:
            junio_l_o +=sale.get_change
        elif sale.date.month == 7:
            julio_l_o +=sale.get_change
        elif sale.date.month == 8:
            agosto_l_o +=sale.get_change
        elif sale.date.month == 9:
            septiembre_l_o +=sale.get_change
        elif sale.date.month == 10:
            octubre_l_o +=sale.get_change
        elif sale.date.month == 11:
            noviembre_l_o +=sale.get_change
        else:
            diciembre_l_o +=sale.get_change

            
            
    # GRAPHS SERVICES  current year
    
    if request.method == 'GET':
        year = request.GET.get('year')
        if year:
            sales_seo_current_year = Sale.objects.filter(service="SEO")\
                                        .filter(date__year=year)
        
            enero_seo = 0
            febrero_seo = 0
            marzo_seo = 0
            abril_seo = 0
            mayo_seo = 0
            junio_seo = 0
            julio_seo = 0
            agosto_seo = 0
            septiembre_seo = 0
            octubre_seo = 0
            noviembre_seo = 0
            diciembre_seo = 0
            
            for sale in sales_seo_current_year:
                if sale.date.month == 1:
                    enero_seo +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_seo +=sale.get_change
                elif sale.date.month == 3:
                    marzo_seo +=sale.get_change
                elif sale.date.month == 4:
                    abril_seo +=sale.get_change
                elif sale.date.month == 5:
                    mayo_seo +=sale.get_change
                elif sale.date.month == 6:
                    junio_seo +=sale.get_change
                elif sale.date.month == 7:
                    julio_seo +=sale.get_change
                elif sale.date.month == 8:
                    agosto_seo +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_seo +=sale.get_change
                elif sale.date.month == 10:
                    octubre_seo +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_seo +=sale.get_change
                else:
                    diciembre_seo +=sale.get_change
                    
                    
            sales_combo_current_year = Sale.objects.filter(service="Combo")\
                                                .filter(date__year=year)
                
            enero_combo = 0
            febrero_combo = 0
            marzo_combo = 0
            abril_combo = 0
            mayo_combo = 0
            junio_combo = 0
            julio_combo = 0
            agosto_combo = 0
            septiembre_combo = 0
            octubre_combo = 0
            noviembre_combo = 0
            diciembre_combo = 0
            
            for sale in sales_combo_current_year:
                if sale.date.month == 1:
                    enero_combo +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_combo +=sale.get_change
                elif sale.date.month == 3:
                    marzo_combo +=sale.get_change
                elif sale.date.month == 4:
                    abril_combo +=sale.get_change
                elif sale.date.month == 5:
                    mayo_combo +=sale.get_change
                elif sale.date.month == 6:
                    junio_combo +=sale.get_change
                elif sale.date.month == 7:
                    julio_combo +=sale.get_change
                elif sale.date.month == 8:
                    agosto_combo +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_combo +=sale.get_change
                elif sale.date.month == 10:
                    octubre_combo +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_combo +=sale.get_change
                else:
                    diciembre_combo +=sale.get_change
                    
                    
            sales_fads_current_year = Sale.objects.filter(service="Facebook Ads")\
                                                .filter(date__year=year)
                
            enero_fads = 0
            febrero_fads = 0
            marzo_fads = 0
            abril_fads = 0
            mayo_fads = 0
            junio_fads = 0
            julio_fads = 0
            agosto_fads = 0
            septiembre_fads = 0
            octubre_fads = 0
            noviembre_fads = 0
            diciembre_fads = 0
            
            for sale in sales_fads_current_year:
                if sale.date.month == 1:
                    enero_fads +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_fads +=sale.get_change
                elif sale.date.month == 3:
                    marzo_fads +=sale.get_change
                elif sale.date.month == 4:
                    abril_fads +=sale.get_change
                elif sale.date.month == 5:
                    mayo_fads +=sale.get_change
                elif sale.date.month == 6:
                    junio_fads +=sale.get_change
                elif sale.date.month == 7:
                    julio_fads +=sale.get_change
                elif sale.date.month == 8:
                    agosto_fads +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_fads +=sale.get_change
                elif sale.date.month == 10:
                    octubre_fads +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_fads +=sale.get_change
                else:
                    diciembre_fads +=sale.get_change
                    
                    
            sales_wp_current_year = Sale.objects.filter(service="Web Plan")\
                                                .filter(date__year=year)
                
            enero_wp = 0
            febrero_wp = 0
            marzo_wp = 0
            abril_wp = 0
            mayo_wp = 0
            junio_wp = 0
            julio_wp = 0
            agosto_wp = 0
            septiembre_wp = 0
            octubre_wp = 0
            noviembre_wp = 0
            diciembre_wp = 0
            
            for sale in sales_wp_current_year:
                if sale.date.month == 1:
                    enero_wp +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_wp +=sale.get_change
                elif sale.date.month == 3:
                    marzo_wp +=sale.get_change
                elif sale.date.month == 4:
                    abril_wp +=sale.get_change
                elif sale.date.month == 5:
                    mayo_wp +=sale.get_change
                elif sale.date.month == 6:
                    junio_wp +=sale.get_change
                elif sale.date.month == 7:
                    julio_wp +=sale.get_change
                elif sale.date.month == 8:
                    agosto_wp +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_wp +=sale.get_change
                elif sale.date.month == 10:
                    octubre_wp +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_wp +=sale.get_change
                else:
                    diciembre_wp +=sale.get_change
                    
                                
            sales_gads_current_year = Sale.objects.filter(service="Google Ads")\
                                                .filter(date__year=year)
                
            enero_gads = 0
            febrero_gads = 0
            marzo_gads = 0
            abril_gads = 0
            mayo_gads = 0
            junio_gads = 0
            julio_gads = 0
            agosto_gads = 0
            septiembre_gads = 0
            octubre_gads = 0
            noviembre_gads = 0
            diciembre_gads = 0
            
            for sale in sales_gads_current_year:
                if sale.date.month == 1:
                    enero_gads +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_gads +=sale.get_change
                elif sale.date.month == 3:
                    marzo_gads +=sale.get_change
                elif sale.date.month == 4:
                    abril_gads +=sale.get_change
                elif sale.date.month == 5:
                    mayo_gads +=sale.get_change
                elif sale.date.month == 6:
                    junio_gads +=sale.get_change
                elif sale.date.month == 7:
                    julio_gads +=sale.get_change
                elif sale.date.month == 8:
                    agosto_gads +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_gads +=sale.get_change
                elif sale.date.month == 10:
                    octubre_gads +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_gads +=sale.get_change
                else:
                    diciembre_gads +=sale.get_change
                    
                    
            sales_cm_current_year = Sale.objects.filter(service="Community Management")\
                                                .filter(date__year=year)
                
            enero_cm = 0
            febrero_cm = 0
            marzo_cm = 0
            abril_cm = 0
            mayo_cm = 0
            junio_cm = 0
            julio_cm = 0
            agosto_cm = 0
            septiembre_cm = 0
            octubre_cm = 0
            noviembre_cm = 0
            diciembre_cm = 0
            
            for sale in sales_cm_current_year:
                if sale.date.month == 1:
                    enero_cm +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_cm +=sale.get_change
                elif sale.date.month == 3:
                    marzo_cm +=sale.get_change
                elif sale.date.month == 4:
                    abril_cm +=sale.get_change
                elif sale.date.month == 5:
                    mayo_cm +=sale.get_change
                elif sale.date.month == 6:
                    junio_cm +=sale.get_change
                elif sale.date.month == 7:
                    julio_cm +=sale.get_change
                elif sale.date.month == 8:
                    agosto_cm +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_cm +=sale.get_change
                elif sale.date.month == 10:
                    octubre_cm +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_cm +=sale.get_change
                else:
                    diciembre_cm +=sale.get_change
                    
            
            
            sales_lk_current_year = Sale.objects.filter(service="LinkedIn")\
                                                .filter(date__year=year)
                
            enero_lk = 0
            febrero_lk = 0
            marzo_lk = 0
            abril_lk = 0
            mayo_lk = 0
            junio_lk = 0
            julio_lk = 0
            agosto_lk = 0
            septiembre_lk = 0
            octubre_lk = 0
            noviembre_lk = 0
            diciembre_lk = 0
            
            for sale in sales_lk_current_year:
                if sale.date.month == 1:
                    enero_lk +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_lk +=sale.get_change
                elif sale.date.month == 3:
                    marzo_lk +=sale.get_change
                elif sale.date.month == 4:
                    abril_lk +=sale.get_change
                elif sale.date.month == 5:
                    mayo_lk +=sale.get_change
                elif sale.date.month == 6:
                    junio_lk +=sale.get_change
                elif sale.date.month == 7:
                    julio_lk +=sale.get_change
                elif sale.date.month == 8:
                    agosto_lk +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_lk +=sale.get_change
                elif sale.date.month == 10:
                    octubre_lk +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_lk +=sale.get_change
                else:
                    diciembre_lk +=sale.get_change
                    
        else:
            
            sales_seo_current_year = Sale.objects.filter(service="SEO")
            
            enero_seo = 0
            febrero_seo = 0
            marzo_seo = 0
            abril_seo = 0
            mayo_seo = 0
            junio_seo = 0
            julio_seo = 0
            agosto_seo = 0
            septiembre_seo = 0
            octubre_seo = 0
            noviembre_seo = 0
            diciembre_seo = 0
            
            for sale in sales_seo_current_year:
                if sale.date.month == 1:
                    enero_seo +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_seo +=sale.get_change
                elif sale.date.month == 3:
                    marzo_seo +=sale.get_change
                elif sale.date.month == 4:
                    abril_seo +=sale.get_change
                elif sale.date.month == 5:
                    mayo_seo +=sale.get_change
                elif sale.date.month == 6:
                    junio_seo +=sale.get_change
                elif sale.date.month == 7:
                    julio_seo +=sale.get_change
                elif sale.date.month == 8:
                    agosto_seo +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_seo +=sale.get_change
                elif sale.date.month == 10:
                    octubre_seo +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_seo +=sale.get_change
                else:
                    diciembre_seo +=sale.get_change
                    
                    
            sales_combo_current_year = Sale.objects.filter(service="Combo")
                
            enero_combo = 0
            febrero_combo = 0
            marzo_combo = 0
            abril_combo = 0
            mayo_combo = 0
            junio_combo = 0
            julio_combo = 0
            agosto_combo = 0
            septiembre_combo = 0
            octubre_combo = 0
            noviembre_combo = 0
            diciembre_combo = 0
            
            for sale in sales_combo_current_year:
                if sale.date.month == 1:
                    enero_combo +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_combo +=sale.get_change
                elif sale.date.month == 3:
                    marzo_combo +=sale.get_change
                elif sale.date.month == 4:
                    abril_combo +=sale.get_change
                elif sale.date.month == 5:
                    mayo_combo +=sale.get_change
                elif sale.date.month == 6:
                    junio_combo +=sale.get_change
                elif sale.date.month == 7:
                    julio_combo +=sale.get_change
                elif sale.date.month == 8:
                    agosto_combo +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_combo +=sale.get_change
                elif sale.date.month == 10:
                    octubre_combo +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_combo +=sale.get_change
                else:
                    diciembre_combo +=sale.get_change
                    
                    
            sales_fads_current_year = Sale.objects.filter(service="Facebook Ads")
                
            enero_fads = 0
            febrero_fads = 0
            marzo_fads = 0
            abril_fads = 0
            mayo_fads = 0
            junio_fads = 0
            julio_fads = 0
            agosto_fads = 0
            septiembre_fads = 0
            octubre_fads = 0
            noviembre_fads = 0
            diciembre_fads = 0
            
            for sale in sales_fads_current_year:
                if sale.date.month == 1:
                    enero_fads +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_fads +=sale.get_change
                elif sale.date.month == 3:
                    marzo_fads +=sale.get_change
                elif sale.date.month == 4:
                    abril_fads +=sale.get_change
                elif sale.date.month == 5:
                    mayo_fads +=sale.get_change
                elif sale.date.month == 6:
                    junio_fads +=sale.get_change
                elif sale.date.month == 7:
                    julio_fads +=sale.get_change
                elif sale.date.month == 8:
                    agosto_fads +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_fads +=sale.get_change
                elif sale.date.month == 10:
                    octubre_fads +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_fads +=sale.get_change
                else:
                    diciembre_fads +=sale.get_change
                    
                    
            sales_wp_current_year = Sale.objects.filter(service="Web Plan")
                
            enero_wp = 0
            febrero_wp = 0
            marzo_wp = 0
            abril_wp = 0
            mayo_wp = 0
            junio_wp = 0
            julio_wp = 0
            agosto_wp = 0
            septiembre_wp = 0
            octubre_wp = 0
            noviembre_wp = 0
            diciembre_wp = 0
            
            for sale in sales_wp_current_year:
                if sale.date.month == 1:
                    enero_wp +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_wp +=sale.get_change
                elif sale.date.month == 3:
                    marzo_wp +=sale.get_change
                elif sale.date.month == 4:
                    abril_wp +=sale.get_change
                elif sale.date.month == 5:
                    mayo_wp +=sale.get_change
                elif sale.date.month == 6:
                    junio_wp +=sale.get_change
                elif sale.date.month == 7:
                    julio_wp +=sale.get_change
                elif sale.date.month == 8:
                    agosto_wp +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_wp +=sale.get_change
                elif sale.date.month == 10:
                    octubre_wp +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_wp +=sale.get_change
                else:
                    diciembre_wp +=sale.get_change
                    
                                
            sales_gads_current_year = Sale.objects.filter(service="Google Ads")
                
            enero_gads = 0
            febrero_gads = 0
            marzo_gads = 0
            abril_gads = 0
            mayo_gads = 0
            junio_gads = 0
            julio_gads = 0
            agosto_gads = 0
            septiembre_gads = 0
            octubre_gads = 0
            noviembre_gads = 0
            diciembre_gads = 0
            
            for sale in sales_gads_current_year:
                if sale.date.month == 1:
                    enero_gads +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_gads +=sale.get_change
                elif sale.date.month == 3:
                    marzo_gads +=sale.get_change
                elif sale.date.month == 4:
                    abril_gads +=sale.get_change
                elif sale.date.month == 5:
                    mayo_gads +=sale.get_change
                elif sale.date.month == 6:
                    junio_gads +=sale.get_change
                elif sale.date.month == 7:
                    julio_gads +=sale.get_change
                elif sale.date.month == 8:
                    agosto_gads +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_gads +=sale.get_change
                elif sale.date.month == 10:
                    octubre_gads +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_gads +=sale.get_change
                else:
                    diciembre_gads +=sale.get_change
                    
                    
            sales_cm_current_year = Sale.objects.filter(service="Community Management")
                
            enero_cm = 0
            febrero_cm = 0
            marzo_cm = 0
            abril_cm = 0
            mayo_cm = 0
            junio_cm = 0
            julio_cm = 0
            agosto_cm = 0
            septiembre_cm = 0
            octubre_cm = 0
            noviembre_cm = 0
            diciembre_cm = 0
            
            for sale in sales_cm_current_year:
                if sale.date.month == 1:
                    enero_cm +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_cm +=sale.get_change
                elif sale.date.month == 3:
                    marzo_cm +=sale.get_change
                elif sale.date.month == 4:
                    abril_cm +=sale.get_change
                elif sale.date.month == 5:
                    mayo_cm +=sale.get_change
                elif sale.date.month == 6:
                    junio_cm +=sale.get_change
                elif sale.date.month == 7:
                    julio_cm +=sale.get_change
                elif sale.date.month == 8:
                    agosto_cm +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_cm +=sale.get_change
                elif sale.date.month == 10:
                    octubre_cm +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_cm +=sale.get_change
                else:
                    diciembre_cm +=sale.get_change
                    
            
            
            sales_lk_current_year = Sale.objects.filter(service="LinkedIn")
                
            enero_lk = 0
            febrero_lk = 0
            marzo_lk = 0
            abril_lk = 0
            mayo_lk = 0
            junio_lk = 0
            julio_lk = 0
            agosto_lk = 0
            septiembre_lk = 0
            octubre_lk = 0
            noviembre_lk = 0
            diciembre_lk = 0
            
            for sale in sales_lk_current_year:
                if sale.date.month == 1:
                    enero_lk +=sale.get_change            
                elif sale.date.month == 2:
                    febrero_lk +=sale.get_change
                elif sale.date.month == 3:
                    marzo_lk +=sale.get_change
                elif sale.date.month == 4:
                    abril_lk +=sale.get_change
                elif sale.date.month == 5:
                    mayo_lk +=sale.get_change
                elif sale.date.month == 6:
                    junio_lk +=sale.get_change
                elif sale.date.month == 7:
                    julio_lk +=sale.get_change
                elif sale.date.month == 8:
                    agosto_lk +=sale.get_change
                elif sale.date.month == 9:
                    septiembre_lk +=sale.get_change
                elif sale.date.month == 10:
                    octubre_lk +=sale.get_change
                elif sale.date.month == 11:
                    noviembre_lk +=sale.get_change
                else:
                    diciembre_lk +=sale.get_change    
              
            
            
                    
    
    context={
        "page_title":"Dashboard",
        "bds" : bds,        
        "activity": last_act[:7],
        "balance": balance,
        "rr_t_clients": rr_t_clients,
        "rr_q_clients": rr_q_clients,
        "rr_this":rr_s_thism,
        "month":month,
        "one_this":oneoff_s_thism,
        "cancell_q": cancell_q,
        
        "seo_clients": seo_clients,
        "gads_clients": gads_clients,
        "fads_clients": fads_clients,
        "lkdn_clients": lkdn_clients,
        "wp_clients": wp_clients,
        "combo_clients": combo_clients,
        "cm_clients": cm_clients,
        "emk_clients": emk_clients,
        "other_clients": other_clients,
        
        "s_c": s_c,
        "g_c": g_c,
        "f_c": f_c,
        "l_c": l_c,
        "w_c": w_c,
        "co_c": co_c,
        "cm_c": cm_c,
        "e_c": e_c,
        "o_c": o_c,
        
        "blue": blue,
        "hour": datetime.now(),
        "c_rr_total": c_rr_total,
        "total_rr":total_rr,
        "total_rr_this_year": round(total_rr_this_year),
        "enero" : round(enero),
        "febrero": round(febrero),
        "marzo": round(marzo),
        "abril": round(abril),
        "mayo": round(mayo),
        "junio": round(junio),
        "julio": round(julio),
        "agosto": round(agosto),
        "septiembre": round(septiembre),
        "octubre": round(octubre),
        "noviembre": round(noviembre),
        "diciembre": round(diciembre),
        "enero_l" : round(enero_l),
        "febrero_l": round(febrero_l),
        "marzo_l": round(marzo_l),
        "abril_l": round(abril_l),
        "mayo_l": round(mayo_l),
        "junio_l": round(junio_l),
        "julio_l": round(julio_l),
        "agosto_l": round(agosto_l),
        "septiembre_l": round(septiembre_l),
        "octubre_l": round(octubre_l),
        "noviembre_l": round(noviembre_l),
        "diciembre_l": round(diciembre_l),
        "enero_o" : round(enero_o),
        "febrero_o": round(febrero_o),
        "marzo_o": round(marzo_o),
        "abril_o": round(abril_o),
        "mayo_o": round(mayo_o),
        "junio_o": round(junio_o),
        "julio_o": round(julio_o),
        "agosto_o": round(agosto_o),
        "septiembre_o": round(septiembre_o),
        "octubre_o": round(octubre_o),
        "noviembre_o": round(noviembre_o),
        "diciembre_o": round(diciembre_o),
        "enero_l_o" : round(enero_l_o),
        "febrero_l_o": round(febrero_l_o),
        "marzo_l_o": round(marzo_l_o),
        "abril_l_o": round(abril_l_o),
        "mayo_l_o": round(mayo_l_o),
        "junio_l_o": round(junio_l_o),
        "julio_l_o": round(julio_l_o),
        "agosto_l_o": round(agosto_l_o),
        "septiembre_l_o": round(septiembre_l_o),
        "octubre_l_o": round(octubre_l_o),
        "noviembre_l_o": round(noviembre_l_o),
        "diciembre_l_o": round(diciembre_l_o),
        "enero_seo" : round(enero_seo),
        "febrero_seo": round(febrero_seo),
        "marzo_seo": round(marzo_seo),
        "abril_seo": round(abril_seo),
        "mayo_seo": round(mayo_seo),
        "junio_seo": round(junio_seo),
        "julio_seo": round(julio_seo),
        "agosto_seo": round(agosto_seo),
        "septiembre_seo": round(septiembre_seo),
        "octubre_seo": round(octubre_seo),
        "noviembre_seo": round(noviembre_seo),
        "diciembre_seo": round(diciembre_seo),
        "enero_combo" : round(enero_combo),
        "febrero_combo": round(febrero_combo),
        "marzo_combo": round(marzo_combo),
        "abril_combo": round(abril_combo),
        "mayo_combo": round(mayo_combo),
        "junio_combo": round(junio_combo),
        "julio_combo": round(julio_combo),
        "agosto_combo": round(agosto_combo),
        "septiembre_combo": round(septiembre_combo),
        "octubre_combo": round(octubre_combo),
        "noviembre_combo": round(noviembre_combo),
        "diciembre_combo": round(diciembre_combo),
        "enero_fads" : round(enero_fads),
        "febrero_fads": round(febrero_fads),
        "marzo_fads": round(marzo_fads),
        "abril_fads": round(abril_fads),
        "mayo_fads": round(mayo_fads),
        "junio_fads": round(junio_fads),
        "julio_fads": round(julio_fads),
        "agosto_fads": round(agosto_fads),
        "septiembre_fads": round(septiembre_fads),
        "octubre_fads": round(octubre_fads),
        "noviembre_fads": round(noviembre_fads),
        "diciembre_fads": round(diciembre_fads),
         "enero_wp" : round(enero_wp),
        "febrero_wp": round(febrero_wp),
        "marzo_wp": round(marzo_wp),
        "abril_wp": round(abril_wp),
        "mayo_wp": round(mayo_wp),
        "junio_wp": round(junio_wp),
        "julio_wp": round(julio_wp),
        "agosto_wp": round(agosto_wp),
        "septiembre_wp": round(septiembre_wp),
        "octubre_wp": round(octubre_wp),
        "noviembre_wp": round(noviembre_wp),
        "diciembre_wp": round(diciembre_wp),
        "enero_gads" : round(enero_gads),
        "febrero_gads": round(febrero_gads),
        "marzo_gads": round(marzo_gads),
        "abril_gads": round(abril_gads),
        "mayo_gads": round(mayo_gads),
        "junio_gads": round(junio_gads),
        "julio_gads": round(julio_gads),
        "agosto_gads": round(agosto_gads),
        "septiembre_gads": round(septiembre_gads),
        "octubre_gads": round(octubre_gads),
        "noviembre_gads": round(noviembre_gads),
        "diciembre_gads": round(diciembre_gads),
        "enero_cm" : round(enero_cm),
        "febrero_cm": round(febrero_cm),
        "marzo_cm": round(marzo_cm),
        "abril_cm": round(abril_cm),
        "mayo_cm": round(mayo_cm),
        "junio_cm": round(junio_cm),
        "julio_cm": round(julio_cm),
        "agosto_cm": round(agosto_cm),
        "septiembre_cm": round(septiembre_cm),
        "octubre_cm": round(octubre_cm),
        "noviembre_cm": round(noviembre_cm),
        "diciembre_cm": round(diciembre_cm),
        "enero_lk" : round(enero_lk),
        "febrero_lk": round(febrero_lk),
        "marzo_lk": round(marzo_lk),
        "abril_lk": round(abril_lk),
        "mayo_lk": round(mayo_lk),
        "junio_lk": round(junio_lk),
        "julio_lk": round(julio_lk),
        "agosto_lk": round(agosto_lk),
        "septiembre_lk": round(septiembre_lk),
        "octubre_lk": round(octubre_lk),
        "noviembre_lk": round(noviembre_lk),
        "diciembre_lk": round(diciembre_lk),
        "i" : i,
        "ii" : ii,
        "iii" : iii,
        "iv" : iv,
        "t_i" : t_i,
        "t_ii" : t_ii,
        "t_iii" : t_iii,
        "t_iv" : t_iv,
        
        
    }
    
    
    return render(request,'dashboard/index.html',context)








    

        
def page_lock_screen(request):
    return render(request,'dashboard/pages/page-lock-screen.html')





def page_error_400(request):
    return render(request,'400.html')
    
def page_error_403(request):
    return render(request,'403.html')

def page_error_404(request):
    return render(request,'404.html')

def page_error_500(request):
    return render(request,'500.html')

def page_error_503(request):
    return render(request,'503.html')
