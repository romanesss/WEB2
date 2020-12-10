from django.db import models
from users.models import CustomerProfile
from catalog.models import Product
from django.db import transaction


class Invoice(models.Model):
    date = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True)
    total = models.IntegerField(default=0)

    def add_item(self, product, quantity):
        invoice_item = InvoiceItem.objects.create(invoice=self, product=product, quantity=quantity)
        self.total += product.price * quantity
        invoice_item.save()


class Cart(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)

    def get_total(self):
        total = 0
        for cart_item in self.cartitem_set.all():
            total += cart_item.product.price * cart_item.quantity
        return total

    def add_item(self, product, quantity):
        cart_item = CartItem.objects.create(cart=self, product=product, quantity=quantity)
        cart_item.save()

    @transaction.atomic
    def buy(self):
        invoice = Invoice.objects.create(customer=self.customer)
        for item in self.cartitem_set.all():
            invoice.add_item(product=item.product, quantity=item.quantity)
            item.delete()
        invoice.save()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    def get_total(self):
        return self.product.price * self.quantity


class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    quantity = models.IntegerField()
    product_price = models.IntegerField(default=None, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def get_total(self):
        if self.product:
            return self.product.price * self.quantity
        else:
            return self.product_price * self.quantity
