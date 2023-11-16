from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm,CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = Profile
    list_display = ('name','email','ph_no','role','is_staff','is_active')
    list_filter = ['role']

    fieldsets = (
        (None, {
            "fields": (
                'name','email','ph_no','role','email_verified',
            ),
        }),('Permissions',{
            'fields':('is_staff','is_active')
        })
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)    
    
admin.site.register(Profile,CustomUserAdmin)
