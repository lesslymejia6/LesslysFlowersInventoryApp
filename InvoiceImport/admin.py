from django.contrib import admin

from .models import InvoiceProducts, Product, Invoice

# Register your models here.
admin.site.register(InvoiceProducts)
admin.site.register(Product)
admin.site.register(Invoice)