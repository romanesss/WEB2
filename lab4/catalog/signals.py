from django.db.models.signals import pre_delete
from django.dispatch import receiver
from sale.models import InvoiceItem
from .models import Product


@receiver(pre_delete, sender=Product)
def invoice_items_fix(sender, instance, **kwargs):
    invoice_items = InvoiceItem.objects.filter(product=instance)
    for invoice_item in invoice_items:
        invoice_item.product_name = invoice_item.product.title
        invoice_item.product_price = invoice_item.product.price
        invoice_item.save()
