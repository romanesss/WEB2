from django.urls import path
from .views import Add2CartView, CartView, CartItemUpdateView, CartItemDeleteView, BuyView

app_name = 'sale'
urlpatterns = [
    path('add_<int:pk>_to_cart/', Add2CartView.as_view(), name='add_to_cart'),
    path('user_cart/', CartView.as_view(), name='user_cart'),
    path('update_<int:pk>_cart_item/', CartItemUpdateView.as_view(), name='cart_item_update'),
    path('delete_<int:pk>_cart_item/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('buy/', BuyView.as_view(), name='buy'),
]
