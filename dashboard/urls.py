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


    path('employees/',dashboard_views.employees, name="employees"),
    path('employees/old/', dashboard_views.employeesold, name="old"),

    path('employees/delete/<int:id>/', dashboard_views.deleteemployee, name="deleteemployee"), 
    path('employees/edit/<int:id>/', dashboard_views.editemployee, name="editemployee"),
    path('employees/salaries/<int:id>/', dashboard_views.salaries, name="salaries"),

    
    path('holiday/delete/<int:id>/', dashboard_views.deleteholiday, name="deleteholiday"), 
    path('holiday/edit/<int:id>/', dashboard_views.editholiday, name="editholiday"), 



    path('ceo/',dashboard_views.ceo, name="ceo"),
    path('ceo/edit/<int:id>/', dashboard_views.editceo, name="editceo"),  
    path('ceo/delete/<int:id>/', dashboard_views.deleteceo, name="deleteceo"),  

    path('expenses/', dashboard_views.expenses, name="expenses"),
    path('expenses/delete/<int:id>/', dashboard_views.deleteexpense, name="deleteexpense"), 
    path('expenses/edit/<int:id>/', dashboard_views.editexpense, name="editexpense"), 
    path('expenses/deleteexpenses/', dashboard_views.delete_expenses, name="deleteexpenses"),
    path('expenses/history/<int:id>/', dashboard_views.expenseshistory, name="expenseshistory"),

    
    path('clients/',dashboard_views.clients, name="clients"),
    path('clients/deleteclient/<int:id>/', dashboard_views.deleteclient, name="deleteclient"),
    path('clients/editclient/<int:id>/', dashboard_views.editclient, name="editclient"),
    path('clients/addclientsale/<int:id>/', dashboard_views.addclientsale, name="addclientsale"),
    path('clients/deleteclients/', dashboard_views.delete_clients, name="deleteclients"),


    path('bi/', dashboard_views.bi, name="bi"),


    path('cancellations/', dashboard_views.cancellations, name="cancellations"),

    path('sales/',dashboard_views.sales, name="sales"),
    path('sales/deletesale/<int:id>/', dashboard_views.deletesale, name="deletesale"),
    path('sales/editsale/<int:id>/', dashboard_views.editsale, name="editsale"),
    path('salesdata/',dashboard_views.salesdata, name="salesdata"),
    path('sales/deletesales/', dashboard_views.delete_sales, name="deletesales"),




    
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
    path('index-2/',dashboard_views.index2,name="index-2"),
    path('schedule/',dashboard_views.schedule,name="schedule"),
    path('instructors/',dashboard_views.instructors,name="instructors"),
    path('message/',dashboard_views.message,name="message"),
    path('activity/',dashboard_views.activity,name="activity"),
    path('profile/',dashboard_views.profile,name="profile"),
    path('courses/',dashboard_views.courses,name="courses"),
    path('course-details-1/',dashboard_views.course_details_1,name="course-details-1"),
    path('course-details-2/',dashboard_views.course_details_2,name="course-details-2"),
    path('instructor-dashboard/',dashboard_views.instructor_dashboard,name="instructor-dashboard"),
    path('instructor-courses/',dashboard_views.instructor_courses,name="instructor-courses"),
    path('instructor-schedule/',dashboard_views.instructor_schedule,name="instructor-schedule"),
    path('instructor-resources/',dashboard_views.instructor_resources,name="instructor-resources"),
    path('instructor-transactions/',dashboard_views.instructor_transactions,name="instructor-transactions"),
    path('instructor-liveclass/',dashboard_views.instructor_liveclass,name="instructor-liveclass"),
    path('app-profile/',dashboard_views.app_profile,name="app-profile"),
    path('post-details/',dashboard_views.post_details,name="post-details"),
    path('email-compose/',dashboard_views.email_compose,name="email-compose"),
    path('email-inbox/',dashboard_views.email_inbox,name="email-inbox"),
    path('email-read/',dashboard_views.email_read,name="email-read"),
    path('app-calender/',dashboard_views.app_calender,name="app-calender"),
    path('ecom-product-grid/',dashboard_views.ecom_product_grid,name="ecom-product-grid"),
    path('ecom-product-list/',dashboard_views.ecom_product_list,name="ecom-product-list"),
    path('ecom-product-detail/',dashboard_views.ecom_product_detail,name="ecom-product-detail"),
    path('ecom-product-order/',dashboard_views.ecom_product_order,name="ecom-product-order"),
    path('ecom-checkout/',dashboard_views.ecom_checkout,name="ecom-checkout"),
    path('ecom-invoice/',dashboard_views.ecom_invoice,name="ecom-invoice"),
    path('ecom-customers/',dashboard_views.ecom_customers,name="ecom-customers"),
    path('chart-flot/',dashboard_views.chart_flot,name="chart-flot"),
    path('chart-morris/',dashboard_views.chart_morris,name="chart-morris"),
    path('chart-chartjs/',dashboard_views.chart_chartjs,name="chart-chartjs"),
    path('chart-chartist/',dashboard_views.chart_chartist,name="chart-chartist"),
    path('chart-sparkline/',dashboard_views.chart_sparkline,name="chart-sparkline"),
    path('chart-peity/',dashboard_views.chart_peity,name="chart-peity"),

    path('ui-accordion/',dashboard_views.ui_accordion,name="ui-accordion"),
    path('ui-alert/',dashboard_views.ui_alert,name="ui-alert"),
    path('ui-badge/',dashboard_views.ui_badge,name="ui-badge"),
    path('ui-button/',dashboard_views.ui_button,name="ui-button"),
    path('ui-modal/',dashboard_views.ui_modal,name="ui-modal"),
    path('ui-button-group/',dashboard_views.ui_button_group,name="ui-button-group"),
    path('ui-list-group/',dashboard_views.ui_list_group,name="ui-list-group"),
    path('ui-media-object/',dashboard_views.ui_media_object,name="ui-media-object"),
    path('ui-card/',dashboard_views.ui_card,name="ui-card"),
    path('ui-carousel/',dashboard_views.ui_carousel,name="ui-carousel"),
    path('ui-dropdown/',dashboard_views.ui_dropdown,name="ui-dropdown"),
    path('ui-popover/',dashboard_views.ui_popover,name="ui-popover"),
    path('ui-progressbar/',dashboard_views.ui_progressbar,name="ui-progressbar"),
    path('ui-tab/',dashboard_views.ui_tab,name="ui-tab"),
    path('ui-typography/',dashboard_views.ui_typography,name="ui-typography"),
    path('ui-pagination/',dashboard_views.ui_pagination,name="ui-pagination"),
    path('ui-grid/',dashboard_views.ui_grid,name="ui-grid"),

    path('uc-select2/',dashboard_views.uc_select2,name="uc-select2"),
    path('uc-nestable/',dashboard_views.uc_nestable,name="uc-nestable"),
    path('uc-noui-slider/',dashboard_views.uc_noui_slider,name="uc-noui-slider"),
    path('uc-sweetalert/',dashboard_views.uc_sweetalert,name="uc-sweetalert"),
    path('uc-toastr/',dashboard_views.uc_toastr,name="uc-toastr"),
    path('map-jqvmap/',dashboard_views.map_jqvmap,name="map-jqvmap"),
    path('uc-lightgallery/',dashboard_views.uc_lightgallery,name="uc-lightgallery"),
    path('uc-lightgallery/',dashboard_views.uc_lightgallery,name="uc-lightgallery"),
    path('widget-basic/',dashboard_views.widget_basic,name="widget-basic"),

    path('form-element/',dashboard_views.form_element,name="form-element"),
    path('form-wizard/',dashboard_views.form_wizard,name="form-wizard"),
    path('form-ckeditor/',dashboard_views.form_ckeditor,name="form-ckeditor"),
    path('form-pickers/',dashboard_views.form_pickers,name="form-pickers"),
    path('form-validation/',dashboard_views.form_validation,name="form-validation"),

    path('table-bootstrap-basic/',dashboard_views.table_bootstrap_basic,name="table-bootstrap-basic"),

    path('page-lock-screen/',dashboard_views.page_lock_screen,name="page-lock-screen"),
    path('page-error-400/',dashboard_views.page_error_400,name="page-error-400"),
    path('page-error-403/',dashboard_views.page_error_403,name="page-error-403"),
    path('page-error-404/',dashboard_views.page_error_404,name="page-error-404"),
    path('page-error-500/',dashboard_views.page_error_500,name="page-error-500"),
    path('page-error-503/',dashboard_views.page_error_503,name="page-error-503"),
    path('empty-page/',dashboard_views.empty_page,name="empty-page"),


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