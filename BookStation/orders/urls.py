from django.urls import path
from . import views

urlpatterns = [
    path('order/create/', views.create_order, name='create_order'),
    path('book/<int:pk>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
]


