from datetime import datetime
from django.http import HttpResponse

from django.core.mail import EmailMessage

from dashboard.resources import SaleResource, ClientResource, \
    EmployeeResource, ExpenseResource, HolidayResource
    



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
