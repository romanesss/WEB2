from django.db import models
from users.models import BaseUser


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products_images',
                              blank=True, default='products_images/default.png')


class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
