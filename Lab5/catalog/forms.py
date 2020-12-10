from django.forms import ModelForm, Form
from .models import Comment
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]

