from django.contrib import admin
from django.urls import path,include
from transportapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup") ,  
    path('about/', views.about, name="about") ,  
    path('handlesignup/', views.handlesignup, name="handlesignup") ,  
    # path('login/', views.login, name="login") ,  
    path('handlelogin/', views.handlelogin, name="handlelogin") ,  
    path('handlelogout/', views.handlelogout, name="handlelogout") ,  
    path('dashboard/', views.dashboard, name="dashboard") ,  
    path('api/data/',views.get_data,name="api-data") ,
    # path('api/chart/data/',views.ChartData.as_view()),

    path('cashbook/', views.cashbook, name="cashbook") ,  
    path('<int:id>/cashbook/', views.cashbook_edit, name="cashbook_edit") ,
    path('<int:id>/cashbook_update/', views.cashbook_update, name="cashbook_update") ,
    path('delete/<int:id>/cashbook/',views.cashbook_delete,name='cashbook_delete'),
    path('cashbook_submit/', views.cashbook_submit, name="cashbook_submit"), 
    path('cashbook_show/',views.cashbook_show,name="cashbook_show") ,
    
    path('bilty/', views.bilty, name="bilty") ,  
    path('<int:id>/bilty/', views.bilty_edit, name="bilty_edit") ,
    path('<int:id>/bilty_update/', views.bilty_update, name="bilty_update") ,
    path('delete/<int:id>/bilty/',views.bilty_delete,name='bilty_delete'),
    path('bilty_submit/', views.bilty_submit, name="bilty_submit"),
    path('bilty_show/',views.bilty_show,name="bilty_show") ,

    path('documents/', views.documents, name="documents") ,  
    path('documents/upload/', views.upload, name="upload") , 
    path('delete/<int:id>/documents',views.delete_doc,name='delete_doc'),
    path('<int:id>/documents/', views.edit_doc, name="edit_doc") , 
    path('<int:id>/update_documents/', views.update_doc, name="update_doc") ,
    path('document_show/',views.document_show,name="document_show") ,

    path('loans_record/', views.loans_record, name="loans_record") , 
    path('<int:id>/loans_record/', views.loans_record_edit, name="loans_record_edit") ,
    path('<int:id>/loans_record_update/', views.loans_record_update, name="loans_record_update") ,
    path('<int:id>/loans_paid_update/', views.loans_paid_update, name="loans_paid_update") ,
    path('delete/<int:id>/loans_record/',views.loans_record_delete,name='loans_record_delete'),
    path('loans_record_submit/', views.loans_record_submit, name="loans_record_submit"),
    path('loans_record_show/',views.loans_record_show,name="loans_record_show") ,
    path('<int:id>/loan_paid/',views.loan_paid,name="loan_paid"),


    path('trip_profile/', views.trip_profile, name="trip_profile") ,
    path('trip_submit/', views.trip_submit, name="trip_submit") ,
    path('trip_show/', views.trip_show, name="trip_show") ,
    path('<int:id>/pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('<int:id>/trip_profile/', views.trip_profile_edit, name="trip_profile_edit"),
    path('<int:id>/trip_profile_update/', views.trip_profile_update, name="trip_profile_update"),
    path('delete/<int:id>/trip_profile/', views.trip_profile_delete, name="trip_profile_delete"),
     
    path('truck_maintenance/', views.truck_maintenance, name="truck_maintenance") ,
    path('<int:id>/truck_maintenance/', views.truck_maintenance_edit, name="truck_maintenance_edit") ,
    path('<int:id>/truck_maintenance_update/', views.truck_maintenance_update, name="truck_maintenance_update") ,
    path('delete/<int:id>/truck_maintenance/',views.truck_maintenance_delete,name='truck_maintenance_delete'),
    path('truck_maintenance_submit/', views.truck_maintenance_submit, name="truck_maintenance_submit"), 
    path('truck_maintenance_show/',views.truck_maintenance_show,name="truck_maintenance_show") ,


    path('tyre_record/', views.tyre_record, name="tyre_record") ,
    path('tyre_record_sumbit/', views.tyre_record_submit, name="tyre_record_submit") ,
    path('<int:id>/tyre_record_edit/',views.tyre_record_edit, name="tyre_record_edit"),
    path('<int:id>/tyre_record_update/',views.tyre_record_update, name="tyre_record_update"),
    path('tyre_record_show/', views.tyre_record_show, name="tyre_record_show") ,
    path('delete/<int:id>/tyre_record/',views.tyre_record_delete,name='tyre_record_delete'),

    path('profile/', views.view_profile, name="view_profile") , 
    path('profile/edit/', views.edit_profile, name="edit_profile") , 
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="app/password_reset.html"),name="reset_password"),
    # path('check/',views.check,name="check"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_done.html"),name="password_reset_complete"),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)