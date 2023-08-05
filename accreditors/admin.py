from django.contrib import admin
from .models import Review, Application, Accreditor
from pickle import FALSE
from datetime import datetime
from .utils import generate_unique_string
from django import forms 
from django.db import models
# Register your models here.



#admin.site.register(User)

admin.site.register(Review)
admin.site.register(Application)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    max_num = 1
    can_delete = FALSE
    
    #editable_fields = ['comment']
    #exclude = ['reviewer']


class ApplicationInline(admin.TabularInline):
    model = Application
    can_delete = FALSE
    
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '20'})},  # Reduce size to 10 characters
    }
    


class AccreditorAdmin(admin.ModelAdmin):
    #form = ApplicationForm 
    pass
    inlines = [ApplicationInline, ReviewInline]
    list_display = ("user", "accreditor_code", "category", "contact_number", "contact_email")
    search_fields = ['category']
    
    # Exclude the accreditor_code field from the admin form
    exclude = ['accreditor_code']
    
    

admin.site.register(Accreditor, AccreditorAdmin)