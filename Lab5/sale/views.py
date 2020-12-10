from django.views.generic import DeleteView, FormView, DetailView
from .models import Cart, CartItem, InvoiceItem, Invoice
from .forms import CartItemForm, BuyForm
from django.views.generic.detail import SingleObjectMixin
from catalog.models import Product
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin


class Add2CartView(PermissionRequiredMixin, FormView, SingleObjectMixin):
    template_name = 'sale/add_to_cart.html'
    form_class = CartItemForm
    model = Product
    object = None
    context_object_name = 'product'
    permission_required = ['sale.add_cartitem', ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        cart = self.request.user.customerprofile_set.all()[0].cart
        cart.add_item(product=self.get_object(), quantity=form.cleaned_data['quantity'])
        return HttpResponseRedirect(reverse('catalog:product_list'))


class CartView(PermissionRequiredMixin, DetailView):
    template_name = 'sale/user_cart.html'
    model = Cart
    context_object_name = 'cart'
    permission_required = ['sale.view_cart', 'sale.view_cartitem', ]

    def get_object(self, queryset=None):
        return self.request.user.customerprofile_set.all()[0].cart


class CartItemUpdateView(PermissionRequiredMixin, FormView, SingleObjectMixin):
    template_name = 'sale/add_to_cart.html'
    model = CartItem
    object = None
    form_class = CartItemForm
    context_object_name = 'cart_item'
    permission_required = ['sale.change_cartitem', ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'quantity': self.get_object().quantity}
        return kwargs

    def form_valid(self, form):
        cart_item = self.get_object()
        cart_item.quantity = form.cleaned_data['quantity']
        cart_item.save()
        return HttpResponseRedirect(reverse('sale:user_cart'))


class CartItemDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'sale/delete_from_cart.html'
    context_object_name = 'cart_item'
    model = CartItem
    permission_required = ['sale.delete_cartitem']

    def get_success_url(self):
        return reverse('sale:user_cart')


class BuyView(PermissionRequiredMixin, FormView, SingleObjectMixin):
    template_name = 'sale/buy.html'
    context_object_name = 'cart'
    model = Cart
    form_class = BuyForm
    object = None
    permission_required = ['sale.add_invoiceitem', 'sale.add_invoice',
                           'sale.view_invoiceitem', 'sale.view_invoice',
                           'sale.delete_cartitem', ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.customerprofile_set.all()[0].cart

    def form_valid(self, form):
        self.get_object().buy()
        return HttpResponseRedirect(reverse('sale:user_cart'))
