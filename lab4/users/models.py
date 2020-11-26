from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext as _
from .managers import UserManager


class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=30)
    last_name = models.CharField(_('last_name'), max_length=30)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'


class AdminProfile(models.Model):
    avatar = models.ImageField(upload_to='admins_avatars', default='admins_avatars/default.png', blank=True, null=True)
    user = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
    national_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user.email)


class CustomerProfile(models.Model):
    avatar = models.ImageField(upload_to='customers_images', default='customers_avatars/default.png', blank=True, null=True)
    user = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return str(self.user.email)

