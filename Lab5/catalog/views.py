from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from .models import Product, Comment
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import CommentForm


class ProductsList(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    paginate_by = 16


class SearchResults(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    paginate_by = 5

    def get_queryset(self):
        print(self.request.GET)
        return Product.objects.filter(title__contains=self.request.GET['term'])


class ProductDetail(FormMixin, DetailView, MultipleObjectMixin):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'
    form_class = CommentForm
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.get_object().id])

    def get_context_data(self, **kwargs):
        object_list = self.get_object().comment_set.all().order_by('-date_posted')
        data = super().get_context_data(object_list=object_list, **kwargs)
        data['form'] = self.get_form()
        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = self.get_object()
        form.save()
        return super().form_valid(form)


class ProductAdd(PermissionRequiredMixin, CreateView):
    model = Product
    permission_required = ('catalog.add_product',)
    template_name = 'catalog/product_add.html'
    fields = ['title', 'description', 'price', 'image']

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.get_object().id])


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = ('catalog.change_product',)
    template_name = 'catalog/product_update.html'
    fields = ['title', 'description', 'price', 'image']

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.get_object().id])


class ProductDelete(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = ('catalog.delete_product',)
    template_name = 'catalog/product_delete.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('catalog:product_list')


class CommentDelete(PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = ('catalog.delete_comment',)
    template_name = 'catalog/comment_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.get_object().product.id])

    def has_permission(self):
        has_perm = super().has_permission()
        return has_perm and self.request.user == self.get_object().author


class CommentUpdate(PermissionRequiredMixin, UpdateView):
    model = Comment
    permission_required = ('catalog.change_comment',)
    template_name = 'catalog/comment_update.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.get_object().product.id])

    def has_permission(self):
        has_perm = super().has_permission()
        return has_perm and self.request.user == self.get_object().author
