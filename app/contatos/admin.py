from django.contrib import admin
from .models import Category, Contact, Contacts_User


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


admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Contacts_User)
