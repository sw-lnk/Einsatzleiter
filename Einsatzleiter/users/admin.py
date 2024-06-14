from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "username",
        # "email",
        "last_name",
        "first_name",
        # "date_of_birth",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "last_name",
        "first_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("username", "email"),
                    "password",
                    "date_of_birth",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    ("first_name", "last_name"),
                    ("username", "email"),
                    "date_of_birth",
                    ("password1", "password2"),
                    ("is_staff", "is_active"),
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
