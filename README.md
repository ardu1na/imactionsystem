############### imactionsystem


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

## USERS :
# /dashboard/users/


## API DOLAR BLUE 
# dashboard/services.py

## EXPORTACIÓN/IMPORTACIÓN
# dashboard/resources.py


### apps (ver diagrama de relación en w3cms/models.jpeg)
# customers app: Client
# sales app: Service(Adj), Sale, Comm 
# expenses app: Employee(Holiday, Salary), Expense



####################################################################################### primera vez:

## activar entorno virtual : 
#source venv/bin/activate
## instalar dependencias: 
# pip install -r requirements.txt
## migrar db
# python3 manage.py makemigrations
# python3 manage.py migrate 
## (# PD: despues de realizar cualquier modificación en los modelos makemigrations, migrate y  arrancar el servidor otra vez
)
## crear superusuario
# python3 manage.py createsuperuser


## arrancar el servidor:
# python3 manage.py runserver 0.0.0.0:80

## (para detener el sevidor: CTRL + C)


## acceder a la url_del_sitio/admin desde el navegador
## desde el panel de administración se pueden importar o exportar las tablas de backups etc
## hay automatizaciones sobre las tareas crud de las instancias de los modelos que se ejecutan en la lógica de la ui
## por lo que únicamente se recomienda el uso de esta interfaz para tareas de mantenimiento


## iniciar sesión y crear grupos con permisos de usuarios
# admin, sales, clients, expenses, cancellations, employees
## en el panel de CustomUsers asignar los grupos al usuario actual y guardar.
####################################################################################



############################### TODO
#################### PASAR A CRONJOBS

# MONTHLY
## MAIL Y EXPORTACIÓN PARA BACKUP: dashboard/email_backups.py
## CREATE NEW INSTANCE OF MONTH EXPENSES SALARIES SERVICES: dashboard/revenue_expenses.py

# DIARLY
## SEE IF IS SOMETHING TO ADJ OR EMAIL TO SEND: dashboard/email_adj.py


######################## 
