from django.shortcuts import render, redirect,get_object_or_404
from dashboard.forms import ConfigurationForm
from dashboard.models import Configurations
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from dashboard import setup_config
import os
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required 
import pickle
import mimetypes

from datetime import datetime
from datetime import date


from customers.models import *
from customers.forms import *
from sales.models import *
from sales.forms import *
from expenses.models import *
from expenses.forms import * 


import csv
from dashboard.forms import UploadFileForm
from .services import promedio as api_blue
from .services import venta as b_venta
from .services import compra as b_compra

@login_required(login_url='dashboard:login')
def conf(request):
   
    if request.method == "GET":

        form = TierConf()
        
        context = {
            'form': form,
            }
        return render (request, 'dashboard/table/conf.html', context)

    
    if request.method == 'POST':
        form = TierConf(request.POST)
        if form.is_valid():
            
            form.save()
                      
            return HttpResponseRedirect('/conf/')
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        







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
        

@login_required(login_url='dashboard:login')
def expenses(request):
    
    expenses = Expense.objects.all()
    employees = Employee.objects.filter(active="Yes")
    all_bonus = 0
    for employee in employees:
        all_bonus += employee.get_aguinaldo_mensual
  
    
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
        
        
    with_wages = without_wages + all_bonus
    for employee in employees:
        with_wages += employee.white
        with_wages += employee.nigga
        
        
    ceo = 0
    for employee in employees.filter(rol="CEO"):
        ceo += employee.white
        ceo += employee.nigga
        ceo += employee.mp
        ceo += employee.tc
        ceo += employee.atm_cash
        ceo += employee.get_aguinaldo_mensual

        
    staff = 0
    for employee in employees.filter(rol="Staff"):
        staff += employee.white
        staff += employee.nigga
        staff += employee.get_aguinaldo_mensual
   
                
    context={
        "page_title": "Expenses",
        "expenses" : expenses,
        "employees": employees,
        "addform" : addform,
        "all_bonus": all_bonus, 
        "without_wages" : without_wages,
        "with_wages": with_wages,
        "ceo": ceo,
        "staff": staff
    }
    print(without_wages)

    return render(request,'dashboard/table/expenses.html', context)





@login_required(login_url='dashboard:login')
def deleteexpense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect(reverse('dashboard:expenses')+ "?deleted")






@login_required(login_url='dashboard:login')
def editemployee(request, id):
    
    editemployee = Employee.objects.get(id=id)

    if request.method == "GET":
        
        editform = EditEmployeeForm(instance=editemployee)
        editwageform = EditWageForm(instance=editemployee)

        context = {
            'editform': editform,
            'editwageform': editform,
            'editemployee': editemployee,
            'id': id
            }
        
        return render (request, 'dashboard/instructor/editemployee.html', context)

    
    if request.method == 'POST':
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
        else:
            editwageform=EditWageForm(request.POST, instance=editemployee)          
            editwageform.white = request.POST['white']
            editwageform.nigga = request.POST['nigga']
            if editwageform.is_valid():
                editwageform.save()
                return redirect(reverse('dashboard:employees')+ "?ok")

            else: 
                print (editwageform)
                print(editwageform.errors)
                return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        


@login_required(login_url='dashboard:login')
def employees(request):
    staff = Employee.objects.filter(rol="Staff")
    ceo = Employee.objects.filter(rol="CEO")        
    employees  = Employee.objects.filter(active="Yes")
    all = Employee.objects.all()
    
    if request.method == 'GET':
        addform = EmployeeForm()
        
    if request.method == 'POST':
        if "addemployee" in request.POST:
            addform = EmployeeForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('dashboard:employees')+ "?added")
            else:
                return HttpResponse("hacked from las except else form")                            
          
    context={
        "staff": staff,
        "ceo": ceo,
        "employees": employees,
        "all": all,
        "addform": addform,        
        "page_title":"WAGES/EMPLOYEES",
    }
    return render(request,'dashboard/instructor/employees.html',context)

@login_required(login_url='dashboard:login')
def deleteemployee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect(reverse('dashboard:employees')+ "?deleted")





# https://stackoverflow.com/questions/69772662/return-monthly-sales-value-in-django
@login_required(login_url='dashboard:login')
def sales(request):
    
    sales = Sale.objects.all()
    
    if request.method == 'GET':
        addform = SaleForm()
        
    if request.method == 'POST':
        if "addsale" in request.POST:
            addform = SaleForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('dashboard:sales')+ "?added")
            else:
                return HttpResponse("hacked from las except else form")
                
    context={
        "page_title":"SALES",
        "sales" : sales,
        "addform" : addform
    }
    return render(request,'dashboard/table/sales.html',context)


@login_required(login_url='dashboard:login')
def deletesale(request, id):
    sale = Sale.objects.get(id=id)
    sale.delete()
    return redirect(reverse('dashboard:sales')+ "?deleted")


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

@login_required(login_url='dashboard:login')
def clients(request):
    clients = Client.objects.filter(cancelled="Active")
      
    total_rr = 0
    for client in clients:
        if client.cancelled == "Active":
            for sale in client.sales.all():
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total_rr += sale.get_change
    total_rr_k = total_rr/1000
    
    clients_rr = []
    for client in clients.filter(cancelled="Active"):
        if client.get_rr_client == True:
            clients_rr.append(client.id)
    c_rr_total = len(clients_rr)
                        
        
    addform=ClientForm()
    if request.method == 'GET':
        addform = ClientForm()
    if request.method == 'POST':
        if "addclient" in request.POST:
            addform = ClientForm(request.POST)
            if addform.is_valid():
                newclient = addform.save()
                return redirect('dashboard:editclient', id=newclient.id)
            else:
                return HttpResponse("hacked from las except else form")
    
    
    sales_rr=Sale.objects.filter(cancelled="Active").filter(revenue="RR")

    s_seo = 0
    s_gads= 0
    s_fads= 0
    s_lin= 0
    s_cm = 0
    s_combo = 0
    s_webp = 0
    

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
        elif sale.service == "COMBO":
            s_combo  += sale.get_change
        elif sale.service == "Web Plan":
            s_webp += sale.get_change
        else: pass

    get_incomes_by_service = [s_seo, s_gads, s_fads, s_lin, s_cm, s_combo, s_webp]
    
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

        "page_title":"RR ACCOUNTS",
    }
    return render(request,'dashboard/instructor/clients.html',context)


@login_required(login_url='dashboard:login')
def allclients(request):
    clients = Client.objects.all()
    
    clients_rr = []
    for client in clients.filter(cancelled="Active"):
        if client.get_rr_client == True:
            clients_rr.append(client.id)
    c_rr_total = len(clients_rr)

    total_rr = 0
    for client in clients:
        if client.cancelled == "Active":
            for sale in client.sales.all():
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total_rr += sale.get_change
                        
        
    addform=ClientForm()
    if request.method == 'GET':
        addform = ClientForm()
    if request.method == 'POST':
        if "addclient" in request.POST:
            addform = ClientForm(request.POST)
            if addform.is_valid():
                newclient = addform.save()
                return redirect('dashboard:editclient', id=newclient.id)
            else:
                return HttpResponse("hacked from las except else form")      
    
    context={
        "total_rr": total_rr,
        "clients" : clients,
        "addform": addform,
        "c_rr_total" : c_rr_total,
        "page_title":"All Clients"
    }

    return render(request,'dashboard/instructor/allclients.html',context)



@login_required(login_url='dashboard:login')
def cancellations(request):
    clients_cancelled = Client.objects.filter(cancelled="Cancelled")
    sales_cancelled = Sale.objects.filter(cancelled="Cancelled").filter(revenue="RR")
    
    
    context={
        "clients_cancelled": clients_cancelled,
        "sales_cancelled" : sales_cancelled,
       
        "page_title":"Cancellations"
    }   
    
    return render(request,'dashboard/instructor/cancellations.html',context)


@login_required(login_url='dashboard:login')
def deleteclient(request, id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect(reverse('dashboard:clients')+ "?deleted")



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
def bankdata(request, id):
    
    client = Client.objects.get(id=id)

    if request.method == "GET":
        
        bankdataform = BankDataForm(instance=client)
        context = {
            'bankdataform': bankdataform,
            'client': client,
            }
        return render (request, 'dashboard/instructor/bankdata.html', context)

    
    if request.method == 'POST':
        bankdataform = BankDataForm(request.POST)
              
        if bankdataform.is_valid():
            nbk = bankdataform.save(commit=False)
            nbk.account = client
            nbk.save()
            
            return HttpResponseRedirect('/clients/')

        else:

            print (bankdataform.errors) 
            return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")
        
        
@login_required(login_url='dashboard:login')
def editbankdata(request, id):
    editbankdata = BankData.objects.get(id=id)
    
    if request.method == "GET":
    
        form = BankDataForm(instance=editbankdata)
        
        context = {
            'form': form,
            'editbankdata': editbankdata,
            'id': id
            }
        return render (request, 'dashboard/instructor/editbankdata.html', context)

    
    if request.method == 'POST':
        form = BankDataForm(request.POST, instance=editbankdata)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/clients/')
        else: return HttpResponse("Ups! Something went wrong. You should go back, update the page and try again.")

        

@login_required(login_url='dashboard:login')
def deletebankdata(request, id):
    bank = BankData.objects.get(id=id)
    bank.delete()
    return HttpResponseRedirect('/clients/')




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
def backup_bankdata(request):
        
    # query
    queryset = BankData.objects.all()
    
    # get fields of model
    options = BankData._meta
    fields = [field.name for field in options.fields]
    # ['id', 'name', 'last_name']...
    # build response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'atachment; filename="backupbankdata.csv"'

    # writer
    writer = csv.writer(response)
    # writing header
    writer.writerow([options.get_field(field).verbose_name for field in fields])

    # writing data
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    
    return response


@login_required(login_url='dashboard:login')
def import_bankdata(request):

    accounts = []
    with open("backupbankdata.csv", "r") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))
        for row in data[1:]:
            accounts.append(
                BankData(
                    id=row[0],
                    payment=row[1],
                    cbu=row[2],
                    alias=row[3],
                    cuit=row[4],
                    detail=row[5],
                    account=row[6],        
                )
            )
    if len(accounts) > 0:
        BankData.objects.bulk_create(accounts)
    
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
    
    clients = Client.objects.all()
    
    clients_rr = []
    for client in clients.filter(cancelled="Active"):
        if client.get_rr_client == True:
            clients_rr.append(client.id)
    c_rr_total = len(clients_rr)

    total_rr = 0
    for client in clients:
        if client.cancelled == "Active":
            for sale in client.sales.all():
                if sale.cancelled == "Active":
                    if sale.revenue == "RR":
                        total_rr += sale.get_change

    last_blue = LastBlue.objects.get(pk=1)
    if api_blue:
        last_blue.venta = b_venta
        last_blue.compra = b_compra
        last_blue.save()
        blue = (last_blue.venta+last_blue.compra)/2    
    else:
        blue = (last_blue.venta+last_blue.compra)/2    
    
    context={
        "page_title":"Dashboard",
        "blue": blue,
        "hour": datetime.now(),
        "c_rr_total": c_rr_total,
        "total_rr":total_rr
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
def activity(request):
    context={
        "page_title":"Activity"
    }
    return render(request,'dashboard/activity.html',context)

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

