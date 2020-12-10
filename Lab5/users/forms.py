from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BaseUser, CustomerProfile
from django.forms import ModelForm
from django import forms
from django.db import transaction


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=13)

    class Meta:
        model = BaseUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save()
        phone_number = self.cleaned_data['phone_number']
        profile = CustomerProfile.objects.create(phone_number=phone_number, user=user)
        profile.save()


class ProfileForm(ModelForm):
    phone_number = forms.CharField(max_length=13)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = BaseUser
        fields = ['email', 'first_name', 'last_name']

    @transaction.atomic
    def save(self, commit=True):
        print(self.cleaned_data['avatar'])
        user = super().save()
        phone_number = self.cleaned_data['phone_number']
        avatar = self.cleaned_data['avatar']
        profile = CustomerProfile.objects.get(user=user)
        profile.phone_number = phone_number
        profile.avatar = avatar
        profile.save()
