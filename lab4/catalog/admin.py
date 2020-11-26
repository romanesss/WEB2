from django.contrib import admin
from .models import Product, Comment
from import_export.admin import ImportExportModelAdmin

admin.site.register(Comment)


@admin.register(Product)
class ProductExport(ImportExportModelAdmin):
    pass
