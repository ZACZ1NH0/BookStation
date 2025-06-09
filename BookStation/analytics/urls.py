from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('books/inventory/', views.book_inventory_detail, name='book_inventory_detail'),
]