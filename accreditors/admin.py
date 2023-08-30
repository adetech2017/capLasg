from django.contrib import admin
from .models import Review, Application, Accreditor
from pickle import FALSE
from datetime import datetime
from .utils import generate_unique_string
from django import forms 
from django.db import models
from core.models import User
# Register your models here.
from django.db.models import Count
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _





class ApplicationStatusFilter(admin.SimpleListFilter):
    title = _('Application Status')
    parameter_name = 'application_status'

    def lookups(self, request, model_admin):
        return (
            ('incomplete', _('Incomplete Application')),
            ('complete', _('Complete Application')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'incomplete':
            return queryset.annotate(application_count=models.Count('applications')).filter(application_count__lt=4)
        if self.value() == 'complete':
            return queryset.annotate(application_count=models.Count('applications')).filter(application_count__gte=4)

#admin.site.register(User)

admin.site.register(Review)
#admin.site.register(Application)

class ReviewInlineFormSet(forms.models.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['reviewer'].widget.can_add_related = False
        form.fields['reviewer'].widget.can_change_related = False  # Disable "Edit" link
        form.fields['reviewer'].widget.can_view_related = False  # Disable "View" link

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    max_num = 1
    can_delete = False
    formset = ReviewInlineFormSet  # Use the custom formset
    
    list_display = ('reviewer', 'accreditor', 'created_at')
    list_filter = ('reviewer', 'accreditor', 'created_at')
    search_fields = ('reviewer__username', 'accreditor__name', 'comment')
    readonly_fields = ('accreditor', 'created_at')
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reviewer":
            # Filter choices to staff users
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ApplicationInlineFormSet(forms.models.BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['status'].widget.can_add_related = False
        form.fields['status'].widget.can_change_related = False  # Disable "Edit" link
        form.fields['status'].widget.can_view_related = False  # Disable "View" link



class ApplicationInline(admin.TabularInline):
    model = Application
    can_delete = FALSE
    editable_fields = ['status',]
    readonly_fields = []
    exclude = ['created_at', 'updated_at', 'id']
    formset = ApplicationInlineFormSet
    
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '20'})},  # Reduce size to 10 characters
    }
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
            [field.name for field in self.model._meta.fields
            if field.name not in self.editable_fields and
                field.name not in self.exclude]


class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        # Add a link to your custom view in the sidebar
        custom_link = reverse('admin:accreditor_application_count')
        sidebar_links = [
            format_html('<li><a href="{}">Accreditor Application Count</a></li>', custom_link),
        ]
        
        extra_context = extra_context or {}
        extra_context['sidebar_links'] = '\n'.join(sidebar_links)

        return super().index(request, extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')


class AccreditorAdmin(admin.ModelAdmin):
    #form = ApplicationForm 
    pass
    inlines = [ApplicationInline, ReviewInline]
    can_delete = FALSE
    list_display = ("user", "accreditor_code", "category", "contact_number", "contact_email",)
    search_fields = ("user__username", "contact_number", 'category__category', 'contact_email',)
    

    # Add the filter to the admin list page
    list_filter = ("category", ApplicationStatusFilter)
    # Exclude the accreditor_code field from the admin form
    exclude = ['accreditor_code']
    
    readonly_fields = ('contact_number',)  # Specify the fields you want to make readonly
    
    def get_readonly_fields(self, request, obj=None):
        # If obj is not None (meaning this is an update), make all fields readonly
        if obj:
            return self.readonly_fields + tuple([field.name for field in obj._meta.fields])
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


admin.site.register(Accreditor, AccreditorAdmin)   
#custom_admin_site.register(Accreditor, AccreditorAdmin)

