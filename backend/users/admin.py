from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("username", "email", "role", "turma", "is_staff")
    list_filter = ("role", "is_staff")

    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ("role", "turma"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações adicionais", {
            "fields": ("role", "turma"),
        }),
    )