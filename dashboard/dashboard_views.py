from django.shortcuts import render, redirect
from dashboard.models import Configurations
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from dashboard import setup_config
import os
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, permission_required 
import pickle
import mimetypes
from django.db.models import Sum
from datetime import datetime
from decimal import Decimal
from django.db.models import Q
from django.db.models import Count
from customers.models import *
from customers.forms import *
from sales.models import *
from sales.forms import *
from expenses.models import *
from expenses.forms import * 
from dashboard.users.models import CustomUser
from dashboard.utils import *
import csv
from dashboard.forms import UploadFileForm
try: 
    from .services import venta as b_venta
    from .services import compra as b_compra
except: pass



from django.http import HttpResponse
    
    
from easyaudit.models import CRUDEvent, LoginEvent

from django.contrib.contenttypes.models import ContentType

from itertools import chain


from django.core.paginator import Paginator

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

   
    
@user_passes_test(lambda user: user.groups.filter(name='admin').exists())   
@login_required(login_url='dashboard:login')
def activity(request):
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
        "list" : elements,

    }
    return render(request,'dashboard/activity.html',context)



@login_required(login_url='dashboard:login')
def setting (request):
    context = {
            "page_title": "SETTINGS",
            }
    return render (request, 'dashboard/table/settings.html', context)



@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def conf(request):
    
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
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        




@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def editexpense(request, id):
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
            return HttpResponseRedirect('/expenses/')
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def expenses(request):
    today = date.today()

    expenses = Expense.objects.filter(date__month=today.month, date__year= today.year)
    employees = Employee.objects.filter(active="Yes").exclude(rol="CEO")
    ceo = Employee.objects.filter(rol="CEO", active="Yes")
    
    if request.method == 'GET':
        addform = ExpenseForm()
        
    if request.method == 'POST':
        if "addexpense" in request.POST:
            addform = ExpenseForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('dashboard:expenses')+ "?added")
            else:
                return HttpResponse("hacked from las except else form")
            
    without_wages = 0
    for expense in expenses:
        without_wages += expense.value
    
    all_bonus = 0
    wages_staff = 0
    wages_ceo = 0
    
    for i in ceo:
        wages_ceo += i.get_total_ceo()
        all_bonus += i.get_aguinaldo_mensual()
        
    for employee in employees:
        wages_staff += employee.get_total()
        all_bonus += employee.get_aguinaldo_mensual()
        
    
    with_wages = without_wages + wages_staff + wages_ceo
    
    empresa = 0
    lead_gen = 0
    office = 0
    other = 0
    tax = 0

    
    for expense in expenses:
        if expense.category == "Empresa":
            empresa += expense.value
        if expense.category == "Lead Gen":
            lead_gen += expense.value
        if expense.category == "Office":
            office += expense.value
        if expense.category == "Other":
            other += expense.value
        if expense.category == "Tax":
            tax += expense.value    
            
            
    all = empresa + lead_gen + office + tax + other + wages_staff + wages_ceo
    
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
        "wages_staff1" : wages_staff1,

    }

    return render(request,'dashboard/table/expenses.html', context)




@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def bi(request):
    sales = Sale.objects.all()
    clients = Client.objects.all()
    expenses = Expense.objects.all()
    employees = Employee.objects.all()
    combined_list = list(chain(sales, clients, expenses, employees))
    
    #services = ["Google Ads", "SEO","Facebook Ads","Web Design", "Hosting", "LinkedIn", "SSL certificate","Web Plan","Combo", "Community Management", "Email Marketing", "Others", "Others RR"]
    kind = ["Upsell", "New Client", "Cross Sell"]
    revenue = ["RR", "OneOff"]
    cancelled = ["Cancelled", "Active"]
    
    services = ["Google Ads", "SEO","Facebook Ads","Web Design", "Hosting", "LinkedIn", "SSL certificate","Web Plan","Combo", "Community Management", "Email Marketing", "Others", "Others RR"]

    

    if request.GET.getlist('service'):
        selected_services = request.GET.getlist('service')
        sales = sales.filter(service__in=selected_services)
    else:
        selected_services = services
        sales = Sale.objects.all()

        if request.GET.getlist('kind'):
            selected_kinds = request.GET.getlist('kind')
            sales = sales.filter(kind__in=selected_kinds)

        if request.GET.getlist('revenue'):
            selected_revenues = request.GET.getlist('revenue')
            sales = sales.filter(revenue__in=selected_revenues)

        if request.GET.getlist('cancelled'):
            selected_cancelled = request.GET.getlist('cancelled')
            sales = sales.filter(cancelled__in=selected_cancelled)
    
    
    # Annotate the sales queryset with the total amount for each service
    totals = sales.values('service').annotate(total_amount=Sum('change')).order_by('service')

    # Create a dictionary mapping each service to its index in the `services` list
    service_index = {service: index for index, service in enumerate(services)}

    # Sort the totals by the index of the service in the `services` list
    # Annotate the sales queryset with the total amount and count for each service
    totals = sales.values('service').annotate(total_amount=Sum('change'), count=Count('id')).order_by('service')

    # Create a new list of labels with the count of sales for each service
    labels = [f"{total['service']} ({total['count']})" for total in totals]

    # Extract the total amounts and labels in the correct order
    total_amounts = [total['total_amount'] for total in totals]
   
    context={
        "page_title": "BUSINESS INTELLIGENCE",
        "data": combined_list,
        "services": services,
        "kind": kind,
        "revenue": revenue,
        "cancelled": cancelled,
        "sales":sales,
        "labels": labels,
        "total_amounts": total_amounts
    }

    return render(request,'dashboard/table/bi.html', context)




@user_passes_test(lambda user: user.groups.filter(name='expenses').exists())
@login_required(login_url='dashboard:login')
def deleteexpense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect(reverse('dashboard:expenses')+ "?deleted")





@user_passes_test(lambda user: user.groups.filter(name='employees').exists())
@login_required(login_url='dashboard:login')
def editemployee(request, id):
    
    editemployee = Employee.objects.get(id=id)
    holidays = Holiday.objects.filter(employee=editemployee)

    if request.method == "GET":
        
        editform = EditEmployeeForm(instance=editemployee)
        wage_instance = Salary.objects.filter(employee=editemployee).last()
        editwageform = EditWageForm(instance=wage_instance) if wage_instance else EditWageForm()
        holydayform = HolidayEmployeeForm()
        raice = RaiceForm()

        context = {
            'raice': raice,
            'holidayform'  : holydayform,
            'editform': editform,
            'editwageform': editwageform,
            'editemployee': editemployee,
            'id': id,
            'holidays': holidays
            }
        
        return render (request, 'dashboard/instructor/editemployee.html', context)

    
    if request.method == 'POST':
        
        if "raice" in request.POST:
            raice = RaiceForm(request.POST)
            print (raice)
            if raice.is_valid():
                raice_nigga = raice.cleaned_data['nigga']
                raice_salary = raice.cleaned_data['salary']
                
                last_wage = Salary.objects.filter(employee=editemployee.pk).last()
                last_wage.salary = last_wage.salary + (last_wage.salary*Decimal(raice_salary))/100
                last_wage.nigga = Decimal(raice_nigga)
                last_wage.save()
                return redirect(reverse('dashboard:employees')+ "?ok")
            else:
                print (editform)

                print(editform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        
        if "editemployee" in request.POST:
            editform = EditEmployeeForm(request.POST, instance=editemployee)
            print (editform)
            if editform.is_valid():
                editform.save()
                return redirect(reverse('dashboard:employees')+ "?ok")
            else:
                print (editform)

                print(editform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        if "holiday" in request.POST:
            
            holydayform = HolidayEmployeeForm(request.POST)
            if holydayform.is_valid():
                holiday = holydayform.save(commit=False)
                holiday.employee = editemployee
                holiday.save()
                return redirect(reverse('dashboard:employees')+ "?ok")
            else:
                print (holydayform)
                print(holydayform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")

        
        if "editwage" in request.POST:
            wage_instance = Salary.objects.filter(employee=editemployee).last()
            editwageform = EditWageForm(request.POST, instance=wage_instance) if wage_instance else EditWageForm(request.POST)
            if editwageform.is_valid():
                wage = editwageform.save(commit=False)
                wage.employee = editemployee
                wage.save()
                return redirect(reverse('dashboard:employees')+ "?ok")
            else: 
                print (editwageform)
                print(editwageform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")


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
            'id': id
            }
        
        return render (request, 'dashboard/instructor/editholiday.html', context)


    if request.method == 'POST':
                
        if "holiday" in request.POST:
            holyday_instance = Holiday.objects.filter(employee=editemployee).last()
            holydayform = HolidayEmployeeForm(request.POST, instance=holyday_instance) if holyday_instance else HolidayEmployeeForm(request.POST)
            if holydayform.is_valid():
                holiday = holydayform.save(commit=False)
                holiday.employee = editemployee
                holiday.save()
                return redirect(reverse('dashboard:employees')+ "?ok")
            else:
                print (holydayform)
                print(holydayform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")



@user_passes_test(lambda user: user.groups.filter(name='employees').exists())
@login_required(login_url='dashboard:login')
def employeesold(request):
    
    old =Employee.objects.filter(active="No")
                              
          
    context={
        
        "page_title":"STAFF OLD",
        "old": old,
    }
    
    return render(request,'dashboard/instructor/employeesold.html',context)


@user_passes_test(lambda user: user.groups.filter(name='employees').exists())
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
                return HttpResponse("hacked from las except else form") 
            
    total_white = 0
    total_nigga = 0
    total_total = 0
    
    
    for employee in staff:
        try:
            total_white += employee.get_white()
        
            total_nigga += employee.get_nigga()
            total_total += employee.get_total()
        except:
            pass     
          
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
        "page_title":"WAGES STAFF",
        
    }
    
    return render(request,'dashboard/instructor/employees.html',context)


@user_passes_test(lambda user: user.groups.filter(name='employees').exists())
@login_required(login_url='dashboard:login')
def deleteholiday(request, id):
    holiday = Holiday.objects.get(id=id)
    holiday.delete()
    if holiday.employee.rol == "CEO":
        return redirect(reverse('dashboard:editceo')+ "?deleted")
    else:
        return redirect(reverse('dashboard:employees')+ "?deleted")

@user_passes_test(lambda user: user.groups.filter(name='employees').exists())
@login_required(login_url='dashboard:login')
def deleteemployee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect(reverse('dashboard:employees')+ "?deleted")


@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def deleteceo(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect(reverse('dashboard:ceo')+ "?deleted")

@user_passes_test(lambda user: user.groups.filter(name='admin').exists())
@login_required(login_url='dashboard:login')
def editceo(request, id):
    
    editemployee = Employee.objects.get(id=id)
    holidays = Holiday.objects.filter(employee=editemployee)

    if request.method == "GET":
        
        editform = EditEmployeeForm(instance=editemployee)
        wage_instance = Salary.objects.filter(employee=editemployee).last()
        editwageform = EditWageCeo(instance=wage_instance) if wage_instance else EditWageCeo()
        holydayform = HolidayEmployeeForm()

        context = {
            'holidayform'  : holydayform,
            'editform': editform,
            'editwageform': editwageform,
            'editemployee': editemployee,
            'id': id,
            'holidays': holidays
            }
        
        return render (request, 'dashboard/instructor/editceo.html', context)

    
    if request.method == 'POST':
        if "editemployee" in request.POST:
            editform = EditEmployeeForm(request.POST, instance=editemployee)
            print (editform)
            if editform.is_valid():
                editform.save()
                return redirect(reverse('dashboard:ceo')+ "?ok")
            else:
                print (editform)

                print(editform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        if "holiday" in request.POST:
            
            holydayform = HolidayEmployeeForm(request.POST)
            if holydayform.is_valid():
                holiday = holydayform.save(commit=False)
                holiday.employee = editemployee
                holiday.save()
                return redirect(reverse('dashboard:ceo')+ "?ok")
            else:
                print (holydayform)
                print(holydayform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")

        
        if "editwage" in request.POST:
            wage_instance = Salary.objects.filter(employee=editemployee).last()
            editwageform = EditWageCeo(request.POST, instance=wage_instance) if wage_instance else EditWageForm(request.POST)
            if editwageform.is_valid():
                wage = editwageform.save(commit=False)
                wage.employee = editemployee
                wage.save()
                return redirect(reverse('dashboard:ceo')+ "?ok")
            else: 
                print (editwageform)
                print(editwageform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")



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
                return HttpResponse("hacked from las except else form")                            
    
              
    context={
        "ceo": ceo,
        "ceo_form": addform,
        "salary_form": salaryform,        
        "page_title":"WAGES CEO",
    }
    
    return render(request,'dashboard/instructor/ceo.html',context)







@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def sales(request):
    
    services = ['SEO','Google Ads','Facebook Ads','Web Design', 'Hosting', 'LinkedIn', 'SSL certificate','Web Plan','Combo', 'Community Management', 'Email Marketing', 'Others', 'Others RR']
    today = date.today()
    this_month = date.today().month
    month_name = date(1900, this_month, 1).strftime('%B')
    
    sales_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, revenue="RR", cancelled="Active")
    total_amount = sales_this_month.aggregate(Sum('change'))['change__sum']
    def get_total_format():
        try:
            return '{:,.0f}'.format(total_amount)
        except: return 0

    sales1_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, revenue="OneOff", cancelled="Active")
    total1_amount = sales1_this_month.aggregate(Sum('change'))['change__sum']
    def get_total1_format():
        try:
            return '{:,.0f}'.format(total1_amount)
        except: return 0
        
    clients_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, kind="New Client", cancelled="Active")
    total_clients = clients_this_month.count()
    
    
    upsell_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, kind="Upsell", cancelled="Active")
    total_upsell_this_month = upsell_this_month.count()
    
    crosssell_this_month = Sale.objects.filter(date__month=today.month, date__year=today.year, kind="Cross Sell", cancelled="Active")
    total_crosssell_this_month = crosssell_this_month.count()
    
    sales = Sale.objects.all()
    
    if request.method == 'GET':
        addform = SaleForm()
        
    if request.method == 'POST':
        if "addsale" in request.POST:
            addform = SaleForm(request.POST)
            print(addform.errors)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('dashboard:sales')+ "?added")
            else:
                return HttpResponse("hacked from las except else form")
    

    
    sales_by_service =Sale.objects.filter(cancelled="Active", date__month=today.month, date__year=today.year)

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
    sales_rr_current_year = Sale.objects.filter(revenue="RR").filter(cancelled="Active")\
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
    sale.delete()
    return redirect(reverse('dashboard:sales')+ "?deleted")


@user_passes_test(lambda user: user.groups.filter(name='sales').exists())
@login_required(login_url='dashboard:login')
def editsale(request, id):
    
    editsale = Sale.objects.get(id=id)

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
            editform.save()
            return redirect(reverse('dashboard:sales')+ "?ok")
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")

@user_passes_test(lambda user: user.groups.filter(name='clients').exists())
@login_required(login_url='dashboard:login')
def clients(request):
    clients = Client.objects.filter(cancelled="Active")
      
    total_rr = 0
    for client in clients:
        if client.cancelled == "Active":
            for sale in client.sales.filter(date__month=date.today().month, date__year=date.today().year):
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total_rr += sale.get_change
    total_rr_k = total_rr
    
    clients_rr = []
    for client in clients.filter(cancelled="Active"):
        if client.get_rr_client == True:
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
    
    
    sales_rr=Sale.objects.filter(cancelled="Active").filter(revenue="RR", date__month=date.today().month, date__year=date.today().year)

    s_seo = 0
    s_gads= 0
    s_fads= 0
    s_lin= 0
    s_cm = 0
    s_combo = 0
    s_webp = 0
    s_other = 0
    

    for sale in sales_rr:
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
        elif sale.service == "Others":
            s_webp += sale.get_change
        else: pass

    get_incomes_by_service = [s_seo, s_gads, s_fads, s_lin, s_cm, s_combo, s_webp, s_other]
    
    t1=0
    t2=0
    t3=0
    t4=0
    t5=0

    for sale in sales_rr:
        if sale.client.tier == "I":
            t1 += sale.get_change
        elif sale.client.tier == "II":
            t2 += sale.get_change
        elif sale.client.tier == "III":
            t3 += sale.get_change
        elif sale.client.tier == "IV":
            t4 += sale.get_change
        elif sale.client.tier == "V":
            t5 += sale.get_change
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
    clients_cancelled = Client.objects.filter(cancelled="Cancelled")
    sales_cancelled = Sale.objects.filter(cancelled="Cancelled").filter(revenue="RR")
    
    today = date.today()
    this_month = date.today().month
    month = date(1900, this_month, 1).strftime('%B')
    
    sales_this_month = sales_cancelled.filter(date_can__month=today.month, client__cancelled="Active")
    clients_this_month = clients_cancelled.filter(date_can__month=today.month)


    total_amount = sales_cancelled.filter(date_can__month=today.month).aggregate(Sum('change'))['change__sum']
    def get_total_format():
        try:
            return '{:,.0f}'.format(total_amount)
        except: return 0
    
    context={
        "clients_cancelled": clients_cancelled,
        "sales_cancelled" : sales_cancelled,
        "month" : month,
        "sales" : sales_this_month.count(),
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
        
        editform = EditClientForm(instance=editclient)
        context = {
            'editform': editform,
            'editclient': editclient,
            'id': id
            }
        return render (request, 'dashboard/instructor/editclient.html', context)

    
    if request.method == 'POST':
        editform = EditClientForm(request.POST, instance=editclient)
        if editform.is_valid():
            clientedit = editform.save(commit=False)
            if clientedit.cancelled == "Cancelled":
                for sale in clientedit.sales.all():
                    sale.cancelled = "Cancelled"
                    sale.comment_can = clientedit.comment_can
                    sale.fail_can = clientedit.fail_can
                    sale.date_can = clientedit.date_can
                    sale.save()
            clientedit.save()
            return redirect(reverse('dashboard:clients')+ "?ok")
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        
        
        
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
           
            return HttpResponseRedirect('/clients/')

        else:

            print (addclientsaleform.errors) 
            return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        
        


@login_required(login_url='dashboard:login')
def backup_clients(request):
        
    # query
    queryset = Client.objects.all()
    
    # get fields of model
    options = Client._meta
    fields = [field.name for field in options.fields]
    # ['id', 'name', 'last_name']...
    # build response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename="backupclients.csv"'

    # writer
    writer = csv.writer(response)
    # writing header
    writer.writerow([options.get_field(field).verbose_name for field in fields])

    # writing data
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    
    return response


def handle_uploaded_file(file):
    clients = []
    with open(file, "r") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))
        print("from function")
        for row in data[1:]:
            clients.append(
                Client(
                    id=row[0],
                    name=row[1],
                    business_name=row[2],
                    source=row[3],
                    date=row[4],
                    website=row[5],
                    email=row[6],
                    email_2=row[7],
                    email_admin=row[8],
                    phone_number=row[9],
                    phone_2=row[10],
                    landing_page=row[11],
                    cancelled=row[12],
                    comment_can=row[13],
                    date_can=row[14],
                    fail_can=row[15]             
                )
            )
    if len(clients) > 0:
        Client.objects.bulk_create(clients)
    

@login_required(login_url='dashboard:login')
def import_clients(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('uploaded')
        else:
            print (form.errors)
    else:
        form = UploadFileForm()
    return render(request, 'dashboard/instructor/uploadbackup.html', {'form': form})


@login_required(login_url='dashboard:login')
def backup_sales(request):
        
    # query
    queryset = Sale.objects.all()
    
    # get fields of model
    options = Sale._meta
    fields = [field.name for field in options.fields]
    # ['id', 'name', 'last_name']...
    # build response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename="backupsales.csv"'

    # writer
    writer = csv.writer(response)
    # writing header
    writer.writerow([options.get_field(field).verbose_name for field in fields])

    # writing data
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    
    return response


@login_required(login_url='dashboard:login')
def import_sales(request):

    sales = []
    with open("backupsales.csv", "r") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))
        for row in data[1:]:
            sales.append(
                Sale(
                    id=row[0],
                    client=row[1],
                    kind=row[2],
                    date=row[3],
                    total=row[4],
                    comments=row[5],
                    revenue=row[6],
                    service=row[7],
                    price=row[8],
                    note=row[9],
                    cost=row[10],
                    status=row[11],
                    cancelled=row[12],
                    comment_can=row[13],
                    date_can=row[14],
                    fail_can=row[15]             
                )
            )
    if len(sales) > 0:
        Sale.objects.bulk_create(sales)
    
    return HttpResponse("Successfully imported")




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
    today = date.today()
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
    except: pass
        
    staff = Employee.objects.filter(active="Yes")
    
    for employee in staff:
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
            
    expenses_list = Expense.objects.all()
    for expense in expenses_list:    
        if expense.date.month != today.month:
            update_expense = Expense.objects.create(
            date=today,
            category=expense.category,
            concept=expense.concept,
            value=expense.value,
            wop=expense.wop,
        )
            
    sales_rr_list = Sale.objects.filter(revenue="RR", cancelled="Active")
    for sale in sales_rr_list:
        if sale.date.month != today.month:
            update_rr = Sale.objects.create(
                client=sale.client,
                kind= sale.kind,
                date=today,
                comments=sale.comments,
                revenue=sale.revenue,
                service=sale.service,
                price=sale.price,
                currency=sale.currency,
                note="auto revenue sale",
                cost=sale.cost,
                status="FC",
                cancelled="Active",               
                    
            )        
            
        
    clients = Client.objects.all()
    
    clients_rr = []
    for client in clients.filter(cancelled="Active"):
        if client.get_rr_client == True:
            clients_rr.append(client.id)
    c_rr_total = len(clients_rr)

    total_rr = 0
    
    i = 0
    ii = 0
    iii = 0
    iv = 0
    v = 0
    
    for client in clients:
        if client.cancelled == "Active":
            for sale in client.sales.all():
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total_rr += sale.get_change
            if client.tier == "I":
                i += 1
            elif client.tier == "II":
                ii += 1
            elif client.tier == "III":
                iii += 1
            elif client.tier == "IV":
                iv += 1
            elif client.tier == "V":
                v += 1

    
    last_blue = LastBlue.objects.get(pk=1) 
    
    try:
        blue = (b_venta+b_compra)/2
        if last_blue.venta != b_venta:
                last_blue.venta = b_venta
        if last_blue.compra != b_compra:
                last_blue.compra = b_compra
        last_blue.save()
            
    except:
       blue = (last_blue.venta+last_blue.compra)/2

    
    
    
    # GRAPHS rr   
    sales_rr_current_year = Sale.objects.filter(revenue="RR").filter(cancelled="Active")\
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
            
            
    sales_rr_last_year = Sale.objects.filter(revenue="RR").filter(cancelled="Active")\
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
    sales_one_current_year = Sale.objects.filter(revenue="OneOff").filter(cancelled="Active")\
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
            
            
    sales_one_last_year = Sale.objects.filter(revenue="OneOff").filter(cancelled="Active")\
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
            sales_seo_current_year = Sale.objects.filter(service="SEO").filter(cancelled="Active")\
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
                    
                    
            sales_combo_current_year = Sale.objects.filter(service="Combo").filter(cancelled="Active")\
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
                    
                    
            sales_fads_current_year = Sale.objects.filter(service="Facebook Ads").filter(cancelled="Active")\
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
                    
                    
            sales_wp_current_year = Sale.objects.filter(service="Web Plan").filter(cancelled="Active")\
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
                    
                                
            sales_gads_current_year = Sale.objects.filter(service="Google Ads").filter(cancelled="Active")\
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
                    
                    
            sales_cm_current_year = Sale.objects.filter(service="Community Management").filter(cancelled="Active")\
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
                    
            
            
            sales_lk_current_year = Sale.objects.filter(service="LinkedIn").filter(cancelled="Active")\
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
            
            sales_seo_current_year = Sale.objects.filter(service="SEO").filter(cancelled="Active")
            
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
                    
                    
            sales_combo_current_year = Sale.objects.filter(service="Combo").filter(cancelled="Active")
                
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
                    
                    
            sales_fads_current_year = Sale.objects.filter(service="Facebook Ads").filter(cancelled="Active")
                
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
                    
                    
            sales_wp_current_year = Sale.objects.filter(service="Web Plan").filter(cancelled="Active")
                
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
                    
                                
            sales_gads_current_year = Sale.objects.filter(service="Google Ads").filter(cancelled="Active")
                
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
                    
                    
            sales_cm_current_year = Sale.objects.filter(service="Community Management").filter(cancelled="Active")
                
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
                    
            
            
            sales_lk_current_year = Sale.objects.filter(service="LinkedIn").filter(cancelled="Active")
                
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
        "v" : v,
        
        
    }
    
    
    return render(request,'dashboard/index.html',context)









@login_required(login_url='dashboard:login')
def index2(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'dashboard/index-2.html',context)

@login_required(login_url='dashboard:login')
def schedule(request):
    context={
        "page_title":"Schedule"
    }
    return render(request,'dashboard/schedule.html',context)



@login_required(login_url='dashboard:login')
def instructors(request):
    context={
        "page_title":"Instructors"
    }
    return render(request,'dashboard/instructors.html',context)




@login_required(login_url='dashboard:login')
def message(request):
    context={
        "page_title":"Message"
    }
    return render(request,'dashboard/message.html',context)






@login_required(login_url='dashboard:login')
def profile(request):
    context={
        "page_title":"Profile"
    }
    return render(request,'dashboard/profile.html',context)




@login_required(login_url='dashboard:login')
def course_details_1(request):
    
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/courses/course-details-1.html',context)

@login_required(login_url='dashboard:login')
def course_details_2(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/courses/course-details-2.html',context)

@login_required(login_url='dashboard:login')
def instructor_dashboard(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'dashboard/instructor/instructor-dashboard.html',context)

@login_required(login_url='dashboard:login')
def instructor_courses(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/instructor/instructor-courses.html',context)

@login_required(login_url='dashboard:login')
def instructor_schedule(request):
    context={
        "page_title":"Instructor Schedule"
    }
    return render(request,'dashboard/instructor/instructor-schedule.html',context)



@login_required(login_url='dashboard:login')
def courses(request):
    sales = Sale.objects.all()
    context={
        "page_title":"Sales",
        "sales" : sales
    }
    return render(request,'dashboard/courses/courses.html',context)








@login_required(login_url='dashboard:login')
def instructor_resources(request):
    context={
        "page_title":"Instructor Resources"
    }
    return render(request,'dashboard/instructor/instructor-resources.html',context)


@login_required(login_url='dashboard:login')
def instructor_transactions(request):
    context={
        "page_title":"Instructor Transactions"
    }
    return render(request,'dashboard/instructor/instructor-transactions.html',context)

@login_required(login_url='dashboard:login')
def instructor_liveclass(request):
    context={
        "page_title":"Live Class"
    }
    return render(request,'dashboard/instructor/instructor-liveclass.html',context)

@login_required(login_url='dashboard:login')
def app_profile(request):
    context={
        "page_title":"Profile"
    }
    return render(request,'dashboard/apps/app-profile.html',context)

@login_required(login_url='dashboard:login')
def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'dashboard/apps/post-details.html',context)

@login_required(login_url='dashboard:login')
def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'dashboard/apps/email/email-compose.html',context)

@login_required(login_url='dashboard:login')
def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'dashboard/apps/email/email-inbox.html',context)

@login_required(login_url='dashboard:login')
def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'dashboard/apps/email/email-read.html',context)

@login_required(login_url='dashboard:login')
def app_calender(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'dashboard/apps/app-calender.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_grid(request):
    context={
        "page_title":"Product-Grid"
    }
    return render(request,'dashboard/apps/shop/ecom-product-grid.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_list(request):
    context={
        "page_title":"Product-List"
    }
    return render(request,'dashboard/apps/shop/ecom-product-list.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_detail(request):
    context={
        "page_title":"Product-Detail"
    }
    return render(request,'dashboard/apps/shop/ecom-product-detail.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_order(request):
    context={
        "page_title":"Product-Order"
    }
    return render(request,'dashboard/apps/shop/ecom-product-order.html',context)

@login_required(login_url='dashboard:login')
def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'dashboard/apps/shop/ecom-checkout.html',context)

@login_required(login_url='dashboard:login')
def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'dashboard/apps/shop/ecom-invoice.html',context)

@login_required(login_url='dashboard:login')
def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'dashboard/apps/shop/ecom-customers.html',context)

@login_required(login_url='dashboard:login')
def chart_flot(request):
    context={
        "page_title":"Chart-Flot"
    }
    return render(request,'dashboard/charts/chart-flot.html',context)

@login_required(login_url='dashboard:login')
def chart_morris(request):
    context={
        "page_title":"Chart-Morris"
    }
    return render(request,'dashboard/charts/chart-morris.html',context)

@login_required(login_url='dashboard:login')
def chart_chartjs(request):
    context={
        "page_title":"Chart-Chartjs"
    }
    return render(request,'dashboard/charts/chart-chartjs.html',context)

@login_required(login_url='dashboard:login')
def chart_chartist(request):
    context={
        "page_title":"Chart-Chartist"
    }
    return render(request,'dashboard/charts/chart-chartist.html',context)

@login_required(login_url='dashboard:login')
def chart_sparkline(request):
    context={
        "page_title":"Chart-Sparkline"
    }
    return render(request,'dashboard/charts/chart-sparkline.html',context)

@login_required(login_url='dashboard:login')
def chart_peity(request):
    context={
        "page_title":"Chart-Peity"
    }
    return render(request,'dashboard/charts/chart-peity.html',context)

@login_required(login_url='dashboard:login')
def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'dashboard/bootstrap/ui-accordion.html',context)

@login_required(login_url='dashboard:login')
def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'dashboard/bootstrap/ui-alert.html',context)

@login_required(login_url='dashboard:login')  
def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'dashboard/bootstrap/ui-badge.html',context)

@login_required(login_url='dashboard:login')
def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'dashboard/bootstrap/ui-button.html',context)

@login_required(login_url='dashboard:login')
def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'dashboard/bootstrap/ui-modal.html',context)

@login_required(login_url='dashboard:login')
def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'dashboard/bootstrap/ui-button-group.html',context)

@login_required(login_url='dashboard:login')
def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'dashboard/bootstrap/ui-list-group.html',context)

@login_required(login_url='dashboard:login')
def ui_media_object(request):
    context={
        "page_title":"Media Object"
    }
    return render(request,'dashboard/bootstrap/ui-media-object.html',context)

@login_required(login_url='dashboard:login')
def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'dashboard/bootstrap/ui-card.html',context)

@login_required(login_url='dashboard:login')
def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'dashboard/bootstrap/ui-carousel.html',context)

@login_required(login_url='dashboard:login')
def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'dashboard/bootstrap/ui-dropdown.html',context)

@login_required(login_url='dashboard:login')
def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'dashboard/bootstrap/ui-popover.html',context)

@login_required(login_url='dashboard:login')
def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'dashboard/bootstrap/ui-progressbar.html',context)

@login_required(login_url='dashboard:login')
def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'dashboard/bootstrap/ui-tab.html',context)

@login_required(login_url='dashboard:login')
def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'dashboard/bootstrap/ui-typography.html',context)

@login_required(login_url='dashboard:login')
def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'dashboard/bootstrap/ui-pagination.html',context)

@login_required(login_url='dashboard:login')
def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'dashboard/bootstrap/ui-grid.html',context)

@login_required(login_url='dashboard:login')
def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'dashboard/plugins/uc-select2.html',context)

@login_required(login_url='dashboard:login')
def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'dashboard/plugins/uc-nestable.html',context)

@login_required(login_url='dashboard:login')
def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'dashboard/plugins/uc-noui-slider.html',context)

@login_required(login_url='dashboard:login')
def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'dashboard/plugins/uc-sweetalert.html',context)

@login_required(login_url='dashboard:login')
def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'dashboard/plugins/uc-toastr.html',context)

@login_required(login_url='dashboard:login')
def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'dashboard/plugins/map-jqvmap.html',context)

@login_required(login_url='dashboard:login')
def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'dashboard/plugins/uc-lightgallery.html',context)

@login_required(login_url='dashboard:login')
def widget_basic(request):
    context={
        "page_title":"Widget"
    }
    return render(request,'dashboard/widget-basic.html',context)

@login_required(login_url='dashboard:login')
def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'dashboard/forms/form-element.html',context)

@login_required(login_url='dashboard:login')
def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'dashboard/forms/form-wizard.html',context)

@login_required(login_url='dashboard:login')
def form_ckeditor(request):
    context={
        "page_title":"Ckeditor"
    }
    return render(request,'dashboard/forms/form-ckeditor.html',context)

@login_required(login_url='dashboard:login')
def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'dashboard/forms/form-pickers.html',context)

@login_required(login_url='dashboard:login')
def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'dashboard/forms/form-validation-jquery.html',context)


@login_required(login_url='dashboard:login')
def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'dashboard/table/table-bootstrap-basic.html',context)







    

        
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

def empty_page(request):
    context={
        "page_title":"Page Empty"
    }
    return render(request,'dashboard/pages/empty-page.html',context)

