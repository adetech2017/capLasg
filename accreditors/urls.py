from  django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .views import MyFormView
from . import admin_views


app_name = 'accreditors'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us', views.contact, name='contact'),
    path('about-cap', views.about, name='about'),
    path('help', views.help, name='help'),
    path('privacy-policy', views.policy, name='privacy'),
    path('grade-1-details', views.grade_a, name='grade_a'),
    path('grade-2-details', views.grade_b, name='grade_b'),
    path('grade-3-details', views.grade_c, name='grade_c'),
    path('grade-4-details', views.grade_d, name='grade_d'),
    path('create-accreditor', views.application_form_view, name='create_accreditor'),
    path('create-account', views.register, name='create_account'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    path('accreditor/dashboard', views.home, name='dashboard'),
    #path('accreditor/application/', AccreditorApplicationView.as_view(), name='accreditor_application'),
    path('dashboard/accreditor-application', views.accreditor_application_create_view, name='application_create'),
    path('download', views.download_document, name='download_document'),
    
    path('dashboard/my_form', MyFormView.as_view(), name='my_form_view_name'),
    
    
    path('dashboard/test-app', views.create_accreditor_and_applications, name='create_accreditor_application'),
    
    path('downloadpdf/', views.download_pdf_file, name='download_pdf_file'),
    path('downloadpdf//', views.download_pdf_file, name='download_pdf_file'),
    
    path('admin/accreditor_application_count/', admin_views.accreditor_application_count, name='accreditor_application_count'),

]