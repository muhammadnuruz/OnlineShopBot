from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from apps.users.models import User
from django.contrib.auth.models import Group as _


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text="Raw passwords are not stored, so there is no way to see this user's password, but you can change the password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('full_name', 'password', 'is_staff')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm

    list_display = ('full_name', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('full_name', 'password', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'password1', 'password2', 'is_staff'),
        }),
    )
    search_fields = ('full_name',)
    ordering = ('full_name',)


admin.site.unregister(_)
admin.site.register(User, UserAdmin)
