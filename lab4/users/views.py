from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, TemplateView
from .forms import RegistrationForm, ProfileForm
from .models import CustomerProfile


class Login(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('admin:index')
        elif self.request.user.adminprofile_set.all():
            return reverse('users:admin_panel')
        return reverse('users:profile')

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:profile'))
        return super().get(request, *args, **kwargs)


class Logout(LogoutView):
    next_page = reverse_lazy('index')


class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse('users:profile')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            return super().get(request, *args, **kwargs)


class Profile(PermissionRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    permission_required = ('users.view_customerprofile', 'users.view_baseuser')

    def get_login_url(self):
        return reverse('users:login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['profile'] = CustomerProfile.objects.get(user=self.get_object())
        return data


class ProfileEdit(PermissionRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile_update.html'
    permission_required = ('users.change_customerprofile', 'users.change_baseuser')

    def get_login_url(self):
        return reverse('users:login')

    def get_success_url(self):
        return reverse('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['profile'] = CustomerProfile.objects.get(user=self.get_object())
        return data

    def get_form(self, form_class=None):
        form = super().get_form()
        phone_number = CustomerProfile.objects.get(user=self.get_object()).phone_number
        form.fields["phone_number"].initial = phone_number
        return form


class AdminPanel(PermissionRequiredMixin, TemplateView):
    template_name = 'users/admin_panel.html'

    def has_permission(self):
        return self.request.user.adminprofile_set.all()
