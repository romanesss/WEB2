from django.urls import path
from .views import ProductsList, ProductDetail, ProductAdd, \
    ProductUpdate, ProductDelete, CommentDelete, CommentUpdate, \
    SearchResults

app_name = 'catalog'
urlpatterns = [
    path('products_list/', ProductsList.as_view(), name='product_list'),
    path('product_<int:pk>_detail/', ProductDetail.as_view(), name='product_detail'),
    path('new_product/', ProductAdd.as_view(), name='product_add'),
    path('product_<int:pk>_update/', ProductUpdate.as_view(), name='product_update'),
    path('product_<int:pk>_delete/', ProductDelete.as_view(), name='product_delete'),
    path('comment_<int:pk>_delete/', CommentDelete.as_view(), name='comment_delete'),
    path('comment_<int:pk>_update/', CommentUpdate.as_view(), name='comment_update'),
    path('search_result/', SearchResults.as_view(), name='search_result'),
]


