from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'storage_capacity','hard_disk_interface','brand','special_feature','compatible_devices','color','price', 'stock','category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)
