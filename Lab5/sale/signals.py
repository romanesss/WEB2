from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import InvoiceItem


@receiver(pre_delete, sender=InvoiceItem)
def invoice_total_fix(sender, instance, **kwargs):
    instance.invoice_set.all()[0].total -= instance.price * instance.quantity
