from django.contrib import admin
from .models import Categoy, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "last_name",
        "phone",
        "email",
        "category",
        "created_at",
        "show",
    )

    list_display_links = ("name", "last_name")

    list_editable = ("show", "phone", "category", "email")

    list_per_page: int = 10

    search_fields = ("name", "last_name", "phone", "email",)


admin.site.register(Categoy)
admin.site.register(Contact, ContactAdmin)
