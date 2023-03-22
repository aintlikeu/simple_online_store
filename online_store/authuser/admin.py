from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authuser.models import User
from authuser.forms import RegistrationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    ordering = ('email',)


# Register your models here.
admin.site.register(User, CustomUserAdmin)
