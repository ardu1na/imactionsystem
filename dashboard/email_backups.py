from datetime import datetime
from django.core.mail import EmailMessage
from dashboard.resources import (
    ServiceResource, SaleResource, AdjResource, CommResource,
    EmployeeResource, SalaryResource, ExpenseResource, HolidayResource, ClientResource )

"""
## EMAIL relevant tables BACKUP monthly ##

    This file must to be excecuted monthly
    
    # TODO
    # test
    # CRON JOB EACH 1 DAY OF MONTH

"""


def export_resource(resource):
    # Retrieve all objects for the resource
    queryset = resource.Meta.model.objects.all()

    # Generate Excel data using ImportExportMixin
    dataset = resource().export(queryset)
    return dataset.xlsx

def export_and_send_all_resources_data():
    # List of resources for which you want to create Excel backups
    resources = [
        ServiceResource, SaleResource, AdjResource, CommResource,
        EmployeeResource, SalaryResource, ExpenseResource, HolidayResource, ClientResource
    ]

    # Create the email
    email_subject = 'System Backup'
    email_body = 'Please find attached the backup of all resources data.'
    email_recipients = ['aprendizajenaturalconciente@gmail.com'] # "hola@imactions.com"

    # Create the email message
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=email_recipients,
    )

    # Attach each resource's Excel file to the email
    current_date = datetime.now().strftime('%Y-%m-%d')
    for resource in resources:
        # Generate Excel data for the resource
        excel_data = export_resource(resource)

        # Create a filename for the resource's Excel file
        resource_name = resource.Meta.model._meta.verbose_name_plural.replace(" ", "_").lower()
        filename = f"{resource_name}_backup_{current_date}.xlsx"

        # Attach the Excel data to the email
        email.attach(filename, excel_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    try:
        email.send()
        return True
    except Exception as e:
        # Handle the email error
        print(f"Failed to send the email: {e}")
        return False
