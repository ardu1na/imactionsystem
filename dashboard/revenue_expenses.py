
from expenses.models import Employee, Salary, Expense
from datetime import date

today = date.today()
last_month = today.month - 1 if today.month > 1 else 12
last_month_year = today.year if today.month > 1 else today.year - 1


"""
## REVENUE EXPENSES AND SALARIES ##

    This file must to be excecuted monthly
    
    # TODO
    # test
    # CRON JOB EACH 1 DAY OF MONTH

"""

def revenue_expenses_and_salaries():
    staff = Employee.objects.filter(active="Yes")
    for employee in staff:
        try:
            last_salary = employee.salaries.last()
            if last_salary is not None and last_salary.period.month != today.month and last_salary.period.year != today.year:
                new_salary = Salary.objects.create(
                                                employee=employee,
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
                
            else:
                print(f"Cant create new {employee.name} salary or retrieve previous one")
                try:
                    new_salary = Salary.objects.create(
                                                employee=employee,
                                                period=today,
                                            
                                            )
                    new_salary.save()
                    print ("First empty salary created for today")
                except:
                    print("caution!! second try also fail ")
        except:
            print("CANT REVENUE SALARIES SEE DASHBOARD/REVENUE_eXPENSES_AND_SALARIES.PY")

            
    expenses_list = Expense.objects.filter(date__month=last_month, date__year=last_month_year)
    for expense in expenses_list:    
        try:

            update_expense = Expense.objects.create(
                                                date=today,
                                                category=expense.category,
                                                concept=expense.concept,
                                                value=expense.value,
                                                currency=expense.currency,
                                                wop=expense.wop,
                                            )
        except:
            print(f"Cant copy expense {expense}")
        