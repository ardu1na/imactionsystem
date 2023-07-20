############### imactionsystem

## TEMPLATES
# HTML files  at:
# /dashboard/templates/

## STATIC files
# (js, css, icons, fonts, images, etc) at:
# /dashboard/static/

## MAIN LOGIC OF THE VIEWS:
# /dashboard/dashboard_views.py

## USER/PERMS/GROUPS/AUTH VIEWS (LOGIC) - FORMS - MODELS (DB) :
# /dashboard/users/

## API DOLAR BLUE 
# dashboard/services.py

## EXPORTACIÓN/IMPORTACIÓN
# dashboard/resources.py



### apps

# customers app
# models: ConfTier, BackUps, AutoRevenue, Client
# forms customers/forms.py TierConf, ClientForm, EditClientForm

# sales app
# models: Service(Sale, Adj, Client) 
# forms sales/forms.py AdjForm, ChangeAdj, SaleForm2, ClientSaleForm, CancellService, EditSaleForm

##  expenses app
# models : Employee (Holiday, Salary, Sale), Expense
# forms expenses/forms.py : RaiceForm, HolidayEmployeeForm, ExpenseForm, EmployeeForm, EmployeeSalaryForm, CeoForm, CeoSalaryForm, EditEmployeeForm, EditWageCeo 




############################### TODO
########################## DASHABOARD_VIEWS 
#################### PASAR A CRONJOBS

# MONTHLY
## MAIL Y EXPORTACIÓN PARA BACKUP / DEFINED IN INDEX AND EN DASHBOARD UTILS.PY Y 
## CREATE NEW INSTANCE OF MONTH EXPENSES SALARIES SERVICES

# DIARLY
## GET DOLLAR BLUE
## SEE IF IS SOMETHING TO ADJ OR EMAIL TO SEND



######################## 
