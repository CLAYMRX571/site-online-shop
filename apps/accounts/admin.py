from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import User, PasswordResetCode
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (("Personal info"), {"fields":("first_name", "last_name", "email", 'photo', 'address')}),
        (
            ("Permissions"),
            {
                "fields":(
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "email", "password1", "password2"),
            },
        ),
    )

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'code', 'email', 'created_at', 'expired_time', 'is_confirmed']
    search_fields = ['email', 'code']
    list_filter = ['created_at']
    readonly_fields = ['uuid', 'code', 'email', 'created_at']