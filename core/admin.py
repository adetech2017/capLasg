from django.contrib import admin
from pickle import FALSE
from .models import User, Status, Category
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.site_header = "CAPMPPUD-LASG"

admin.site.register(Status)
admin.site.register(Category)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_accreditor', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(User, CustomUserAdmin)

