from  django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .views import MyFormView, AddAccreditorApplicationView



app_name = 'accreditors'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us', views.contact, name='contact'),
    path('about-cap', views.about, name='about'),
    path('help', views.help, name='help'),
    path('privacy-policy', views.policy, name='privacy'),
    path('create-accreditor', views.application_form_view, name='create_accreditor'),
    path('create-account', views.register, name='create_account'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    path('accreditor/dashboard', views.home, name='dashboard'),
    #path('accreditor/application/', AccreditorApplicationView.as_view(), name='accreditor_application'),
    path('dashboard/accreditor-application', views.accreditor_application_create_view, name='application_create'),
    path('download', views.download_document, name='download_document'),
    
    path('dashboard/my_form', MyFormView.as_view(), name='my_form_view_name'),
    
    path('dashboard/add_accreditor_application/', AddAccreditorApplicationView.as_view(), name='add_accreditor_application'),
]