from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted
from catalog.models import Product, Category


class CustomAdmin(SafeDeleteAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field",) + SafeDeleteAdmin.list_display
    list_filter = (SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"


CustomAdmin.highlight_deleted_field.short_description = CustomAdmin.field_to_highlight

admin.site.register(Product, CustomAdmin)
admin.site.register(Category, CustomAdmin)
