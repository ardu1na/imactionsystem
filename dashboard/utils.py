from datetime import datetime
from django.http import HttpResponse

from django.core.mail import EmailMessage

from dashboard.resources import SaleResource, ClientResource, \
    EmployeeResource, ExpenseResource, HolidayResource
    
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render
from django.utils.html import strip_tags
from django.utils import timezone


def adj_email(request):
    if 'adjaccount' in request.POST:
        inversion_actual = request.POST['inversion_actual']
        ajuste_porcentaje = request.POST['ajuste_porcentaje']
        correo_destinatario = request.POST['correo_destinatario']
    
    # Calcula el ajuste necesario
    inversion_ajustada = inversion_actual * (1 + ajuste_porcentaje / 100)
    ajuste = inversion_ajustada - inversion_actual
    
    # Crea el correo electrónico utilizando la clase EmailMessage
    asunto = 'Ajuste por inflación'
    mensaje = f'Hola estimado,\n\nEl motivo de este email es para comunicarte un ajuste por inflación.\n\nInversión actual: ${inversion_actual}\nInversión con ajuste: ${inversion_ajustada}\nAjuste: ${ajuste}\n\nEl ajuste se hará en el próximo pago.\n\nCualquier duda no dejes de consultarnos.\n\nSaludos,\n\nImactions\nwww.imactions.agency'
    correo = EmailMessage(asunto, mensaje, to=[correo_destinatario])

    # Envía el correo electrónico
    correo.send()

    # Redirige al usuario a la página de éxito
    return redirect('exito.html')
"""






def export_holidays():
    holiday_resource = HolidayResource()
    data = holiday_resource.export()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"holidays_{current_date}.xlsx"
    response = HttpResponse(data.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create email message with attachment
    email_subject = 'Holidays backup'
    email_body = 'Please find attached the latest sales data.'
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=["hola@imactions.com"]
    )
    email.attach(filename, response.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()




def export_sales():
    sale_resource = SaleResource()
    data = sale_resource.export()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"sales_{current_date}.xlsx"
    response = HttpResponse(data.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create email message with attachment
    email_subject = 'Sales backup'
    email_body = 'Please find attached the latest sales data.'
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=["hola@imactions.com"]
    )
    email.attach(filename, response.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()


def export_clients():
    client_resource = ClientResource()
    data = client_resource.export()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"clients_{current_date}.xlsx"
    response = HttpResponse(data.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    email_subject = 'Clients backup'
    email_body = 'Please find attached the latest clients data.'
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=["hola@imactions.com"]
    )
    email.attach(filename, response.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    
    
    

def export_employees ():
    employee_resource = EmployeeResource()
    data = employee_resource.export()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"employees_{current_date}.xlsx"
    response = HttpResponse(data.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    email_subject = 'employees backup'
    email_body = 'Please find attached the latest employees data.'
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=["hola@imactions.com"]
    )
    email.attach(filename, response.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    
def export_expenses ():
    expense_resource = ExpenseResource()
    data = expense_resource.export()
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"expenses_{current_date}.xlsx"
    response = HttpResponse(data.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    email_subject = 'expenses backup'
    email_body = 'Please find attached the latest expenses data.'
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=["hola@imactions.com"]
    )
    email.attach(filename, response.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
