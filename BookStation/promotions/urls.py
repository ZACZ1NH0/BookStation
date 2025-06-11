from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('', views.promotion_list, name='promotion_list'),
    path('apply-code/', views.apply_promotion_code, name='apply_promotion_code'),
    path('valid-promotions/', views.get_valid_promotions, name='get_valid_promotions'),
]