
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import  date
from decimal import Decimal
from sales.models import Adj

today = date.today()
        

"""
## EMAIL ADJ SERVICE/ACCOUNT REMINDER ------------- ADJUSTMENT EMAIL ##

    This file must to be excecuted every day
    
    # TODO
    # test
    # CRON JOB EACH every day at not workable time

"""

##############################################    ##############################################
def email_adj_remind():
    print("##############################################  ADJUSTMENTS EMAIL REMINDERS ###################################")

    #  internal reminder ----adjust client------ for email send 
    
    remind_list = Adj.objects.filter(
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
                        recipient_list=['systemimactions@gmail.com', 'hola@imactions.com'], # ['hola@imactions.com'],
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

                