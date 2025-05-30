from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin_home/', views.home_admin, name='home_admin'),
    path('staff_home/', views.home_staff, name='home_staff'),
    path('customer_home/', views.home_customer, name='home_customer'),
]
