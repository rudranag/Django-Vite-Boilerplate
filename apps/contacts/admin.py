from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "company_name",
        "address",
    )
    search_fields = ("first_name", "last_name", "email", "company_name")


admin.site.register(Contact, ContactAdmin)
