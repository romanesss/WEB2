from django.contrib import admin
from .models import Cart, CartItem, Invoice, InvoiceItem


admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
