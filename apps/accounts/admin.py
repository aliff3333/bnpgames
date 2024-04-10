from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Address
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["email", "phone_number", "full_name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("اطلاعات ورود به حساب", {"fields": ["email", "password"]}),
        ("اطلاعات شخصی", {"fields": ["full_name", "phone_number"]}),
        ("دسترسی ها", {"fields": ['is_superuser', "is_admin", 'groups', 'user_permissions']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "phone_number", "full_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(Address)
admin.site.register(User, UserAdmin)
