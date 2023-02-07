from django.contrib import admin
from unfold.admin import ModelAdmin
from expenses.models import Employee, Expense

class EmployeeAdmin(ModelAdmin): 
    pass

admin.site.register(Employee, EmployeeAdmin)


class ExpenseAdmin(ModelAdmin): 
    pass

admin.site.register(Expense, ExpenseAdmin)