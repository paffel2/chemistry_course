from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm


from users.models import User

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            "Главная информация",
            {"fields": ("email", "password", "name")},
        ),
        ("Статус", {"fields": ("is_researcher", "is_superuser", "is_active")}),
    )
    list_display = ("id", "email", "name", "is_superuser", "is_researcher", "is_active")
    ordering = ["-id"]
    search_fields = ["email"]
    form = UserChangeForm
    list_filter = ("is_superuser", "is_researcher", "is_active")
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
