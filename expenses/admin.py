from django.contrib import admin
'from unfold.admin import ModelAdmin
'from import_export.admin import ImportExportModelAdmin

from dashboard.resources import EmployeeResource, ExpenseResource, HolidayResource
from expenses.models import Employee, Expense, Holiday, Salary

class EmployeeAdmin(ModelAdmin, ImportExportModelAdmin): 
    resource_class = EmployeeResource

admin.site.register(Employee, EmployeeAdmin)


class ExpenseAdmin(ModelAdmin, ImportExportModelAdmin): 
    resource_class = ExpenseResource


admin.site.register(Expense, ExpenseAdmin)




admin.site.register(Salary)


class HolidayAdmin(ModelAdmin, ImportExportModelAdmin): 
    resource_class = HolidayResource


admin.site.register(Holiday, HolidayAdmin)