from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from manager.models import (
    AttributeCategory,
    Country,
    OfferStatus,
    OfferType,
    Player,
    PlayerPosition,
    PlayerStatus,
    User,
)


class UserAdmin(BaseUserAdmin):
    """Define Admin for User with email and no username"""

    fieldsets = (
        (
            None,
            {"fields": ("email", "password")},
        ),
        (
            "Permissions",
            {"fields": ("is_admin",)},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
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
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(AttributeCategory)
admin.site.register(Country)
admin.site.register(OfferStatus)
admin.site.register(OfferType)
admin.site.register(Player)
admin.site.register(PlayerPosition)
admin.site.register(PlayerStatus)
