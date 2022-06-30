from django.urls import path

from .views import (
    cart_add,
    open_cart,
    clear_cart,
    remove_from_cart,
)

app_name = 'cart'

urlpatterns = [
    path('<int:pk>/', cart_add, name='cart_add'),
    path('open-cart/', open_cart, name='open_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
]