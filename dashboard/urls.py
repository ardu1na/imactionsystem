from dashboard.users.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import path


from dashboard import dashboard_views
from dashboard.users import users_views

app_name='dashboard'

urlpatterns = [
    
    path('conf/',dashboard_views.conf, name="conf"),
    path('setting/',dashboard_views.setting, name="setting"),
    path('comms/',dashboard_views.comms, name="comms"),
    

    path('employees/',dashboard_views.employees, name="employees"),
    path('employees/export/',dashboard_views.export_employees, name="export_employees"),

    path('employees/old/', dashboard_views.employeesold, name="old"),

    path('employees/delete/<int:id>/', dashboard_views.deleteemployee, name="deleteemployee"), 
    path('employees/edit/<int:id>/', dashboard_views.editemployee, name="editemployee"),

    
    path('holiday/delete/<int:id>/', dashboard_views.deleteholiday, name="deleteholiday"), 
    path('holiday/edit/<int:id>/', dashboard_views.editholiday, name="editholiday"), 



    path('ceo/',dashboard_views.ceo, name="ceo"),
    path('ceo/edit/<int:id>/', dashboard_views.editceo, name="editceo"),  
    path('ceo/delete/<int:id>/', dashboard_views.deleteceo, name="deleteceo"),  
    path('ceo/export/', dashboard_views.export_ceo, name="export_ceo"),  

    path('expenses/', dashboard_views.expenses, name="expenses"),
    path('expenses/delete/<int:id>/', dashboard_views.deleteexpense, name="deleteexpense"), 
    path('expenses/edit/<int:id>/', dashboard_views.editexpense, name="editexpense"), 
    path('expenses/deleteexpenses/', dashboard_views.delete_expenses, name="deleteexpenses"),
    path('expenses/history/<int:id>/', dashboard_views.expenseshistory, name="expenseshistory"),
    path('expenses/export/', dashboard_views.export_expenses, name="export_expenses"),

    
    path('clients/',dashboard_views.clients, name="clients"),
    path('clients/deleteclient/<int:id>/', dashboard_views.deleteclient, name="deleteclient"),
    path('clients/editclient/<int:id>/', dashboard_views.editclient, name="editclient"),
    path('clients/addclientsale/<int:id>/', dashboard_views.addclientsale, name="addclientsale"),
    path('clients/deleteclients/', dashboard_views.delete_clients, name="deleteclients"),
    path('clients/export/', dashboard_views.export_clients, name="export_clients"),
    path('clients/rr/export/', dashboard_views.export_rr, name="export_rr"),

    path('client-autocomplete/', dashboard_views.client_autocomplete, name='client_autocomplete'),

    path('adjustments/',dashboard_views.adjustment, name="adjustment"),
    path('adjustments/<int:id>/',dashboard_views.adjustment, name="adjustsale"),
    path('adjustment/<int:id>/delete/', dashboard_views.deleteadj, name="canceladj"),
    path('adjustment/<int:id>/change/', dashboard_views.editadj, name="editadj"),

    path('adj/',dashboard_views.adj, name="adj"),


    path('services/<int:id>/', dashboard_views.editservice, name="editservice"),
    path('services/<int:id>/restore/', dashboard_views.restoreservice, name="restoreservice"),




    path('cancellations/', dashboard_views.cancellations, name="cancellations"),




    path('sales/',dashboard_views.sales, name="sales"),
    path('sales/deletesale/<int:id>/', dashboard_views.deletesale, name="deletesale"),
    path('sales/editsale/<int:id>/', dashboard_views.editsale, name="editsale"),
    path('salesdata/',dashboard_views.salesdata, name="salesdata"),
    path('sales/deletesales/', dashboard_views.delete_sales, name="deletesales"),
    path('sales/export/', dashboard_views.export_sales, name='export_sales'),





    
	path('users/',users_views.users,name="users"),
	path('user-details/<int:id>/',users_views.user_details,name="user-details"),
	path('add-user/',users_views.add_user,name="add-user"),
	path('edit-user/<int:id>/',users_views.edit_user,name="edit-user"),
	path('delete-user/<int:id>/',users_views.delete_user,name="delete-user"),
	path('delete-multiple-user/',users_views.delete_multiple_user,name="delete-multiple-user"),

	path('login/',users_views.login_user,name="login"),
	path('logout/',users_views.logout_user,name="logout"),
	path('groups/',users_views.groups_list,name="groups"),
	path('group-edit/<int:id>/',users_views.group_edit,name="group-edit"),
	path('group-delete/<int:id>/',users_views.group_delete,name="group-delete"),
	path('group-add/',users_views.group_add,name="group-add"),
	path('permissions/',users_views.permissions,name="permissions"),
	path('edit-permissions/<int:id>/',users_views.edit_permissions,name="edit-permissions"),
	path('delete-permissions/<int:id>/',users_views.delete_permissions,name="delete-permissions"),
	path('assign-permissions-to-user/<int:id>/',users_views.assign_permissions_to_user,name="assign-permissions-to-user"),
	path('signup/',users_views.signup,name="signup"),
	path('activate/<uidb64>/<token>/',users_views.activate, name='activate'),


    path('',dashboard_views.index,name="index"),
    path('index/',dashboard_views.index,name="index"),
    path('activity/',dashboard_views.activity,name="activity"),
    path('page-lock-screen/',dashboard_views.page_lock_screen,name="page-lock-screen"),
    path('page-error-400/',dashboard_views.page_error_400,name="page-error-400"),
    path('page-error-403/',dashboard_views.page_error_403,name="page-error-403"),
    path('page-error-404/',dashboard_views.page_error_404,name="page-error-404"),
    path('page-error-500/',dashboard_views.page_error_500,name="page-error-500"),
    path('page-error-503/',dashboard_views.page_error_503,name="page-error-503"),


    path('', users_views.password_change, name='password_change'),






    # This Route for PasswordChange
    path('password/', users_views.password_change, name='password_change'),

    # These Routes for PasswordReset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        form_class=EmailValidationOnForgotPassword,
        success_url=reverse_lazy('dashboard:password_reset_done')),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('dashboard:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


] 