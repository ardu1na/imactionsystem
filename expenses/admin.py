from django.contrib import admin
from unfold.admin import ModelAdmin
from expenses.models import Expense, Salary, Employee

class SalaryInstanceInline(admin.TabularInline):
    model = Salary
    extra = 0
    verbose_name = "WAGE DETAIL"
    verbose_name_plural = "WAGES"


class ExpenseAdmin(ModelAdmin):
    inlines = [SalaryInstanceInline,]
    list_display = ('category', 'concept', 'get_value', 'wop')
    date_hierarchy = 'date'
    search_fields = ("concept",)
    list_filter = ('category',)

    
    @admin.display(description='VALUE')
    def get_value(self, obj):
        return '${:,}'.format(obj.value)

admin.site.register(Expense, ExpenseAdmin)





class EmployeeAdmin(ModelAdmin):
    list_display = ('name', 'get_salary_w', 'get_social', 'get_salary_n', 'get_total', 'get_mensual')

    @admin.display(description='WAGE')
    def get_salary_w(self, obj):
        last_wage_w= obj.salarys.filter(kind='White').latest('-id')
        return '${:,}'.format(last_wage_w.expense.value)

    @admin.display(description='NIGGA')
    def get_salary_n(self, obj):
        last_wage_n= obj.salarys.filter(kind='Nigga').latest('-id')
        return '${:,}'.format(last_wage_n.expense.value)

    @admin.display(description='CARGAS SOCIALES')
    def get_social(self, obj):
        last_wage_n= obj.salarys.filter(kind='White').latest('-id')
        return '${:,}'.format(int(last_wage_n.expense.value)/2)

    @admin.display(description='TOTAL')
    def get_total(self, obj):
        last_wage_n= obj.salarys.filter(kind='White').latest('-id')
        last_wage_w= obj.salarys.filter(kind='Nigga').latest('-id')
        social = last_wage_n.expense.value/2
        total = last_wage_n.expense.value + last_wage_w.expense.value + social
        return '${:,}'.format(total)

    @admin.display(description='MENSUAL')
    def get_mensual(self, obj):
        last_wage_n= obj.salarys.filter(kind='White').latest('-id')
        last_wage_w= obj.salarys.filter(kind='Nigga').latest('-id')
        social = last_wage_n.expense.value/2
        total = last_wage_n.expense.value + last_wage_w.expense.value + social
        mensual = total/12
        multiplier = 10 ** 2
        value = int(mensual * multiplier) / multiplier
        return '${:,}'.format(value)

admin.site.register(Employee, EmployeeAdmin)




