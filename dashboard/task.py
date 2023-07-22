
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import  date
today = date.today()
from dashboard.models import BackUps, AutoRevenue
from dashboard.utils import *


    
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
    
    