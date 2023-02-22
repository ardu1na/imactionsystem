from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

from dashboard.resources import EmployeeResource, ExpenseResource
from expenses.models import Employee, Expense

class EmployeeAdmin(ModelAdmin, ImportExportModelAdmin): 
    resource_class = EmployeeResource

admin.site.register(Employee, EmployeeAdmin)


class ExpenseAdmin(ModelAdmin, ImportExportModelAdmin): 
    resource_class = ExpenseResource


admin.site.register(Expense, ExpenseAdmin)