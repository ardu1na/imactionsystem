############### imactionsystem

# activar entorno virtual : source venv/bin/activate


## arrancar el servidor:
# python3 manage.py runserver 0.0.0.0:80
# (para detener el sevidor: CTRL + C)

# primera vez
# instalar dependencias: pip install -r requirements.txt

# PD: despues de realizar cualquier modificación en los modelos:
# python3 manage.py makemigrations
# python3 manage.py migrate
## arrancar el servidor otra vez


##### DÓNDE ENCONTRAR:

## TEMPLATES
# HTML files  at:
# /dashboard/templates/
# base: dashboard\templates\dashboard\elements\layouts\admin.html


## STATIC files
# (js, css, icons, fonts, images, etc) at:
# /dashboard/static/

## MAIN LOGIC OF THE VIEWS:
# /dashboard/dashboard_views.py
## config models:  /dashboard/models.py

## USER/PERMS/GROUPS/AUTH VIEWS (LOGIC) - FORMS - MODELS (DB) :
# /dashboard/users/

## API DOLAR BLUE 
# dashboard/services.py

## EXPORTACIÓN/IMPORTACIÓN
# dashboard/resources.py



### apps (ver diagrama de relación en w3cms/models.jpeg)
# customers app: Client

# sales app: Service(Adj), Sale 

#  expenses app: Employee(Holiday, Salary), Expense



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
