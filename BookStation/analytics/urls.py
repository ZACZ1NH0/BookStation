from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('books/inventory/', views.book_inventory_detail, name='book_inventory_detail'),
    path('customers_stats/', views.customer_stats, name='customer_stats'),
    path('orders_stats/', views.order_stats, name='order_stats'),
]
