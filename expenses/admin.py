from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from dashboard.resources import SalaryResource, EmployeeResource, ExpenseResource, HolidayResource
from expenses.models import Employee, Expense, Holiday, Salary











class EmployeeAdmin(ImportExportModelAdmin): 
    resource_class = EmployeeResource

admin.site.register(Employee, EmployeeAdmin)


class ExpenseAdmin(ImportExportModelAdmin): 
    resource_class = ExpenseResource


admin.site.register(Expense, ExpenseAdmin)



class SalaryAdmin(ImportExportModelAdmin):
    resource_class = SalaryResource
admin.site.register(Salary, SalaryAdmin)


class HolidayAdmin(ImportExportModelAdmin): 
    resource_class = HolidayResource


admin.site.register(Holiday, HolidayAdmin)
