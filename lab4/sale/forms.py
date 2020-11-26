from django import forms


class CartItemForm(forms.Form):
    quantity = forms.IntegerField()


class BuyForm(forms.Form):
    pass
