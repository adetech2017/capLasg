from  django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
#from .views import AccreditorApplicationView



app_name = 'accreditors'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us', views.contact, name='contact'),
    path('about-cap', views.about, name='about'),
    path('help', views.help, name='help'),
    path('create-accreditor', views.application_form_view, name='create_accreditor'),
    path('create-account', views.register, name='create_account'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    path('accreditor/dashboard', views.home, name='dashboard'),
    #path('accreditor/application/', AccreditorApplicationView.as_view(), name='accreditor_application'),
    path('application/create/', views.accreditor_application_create_view, name='application_create'),
]