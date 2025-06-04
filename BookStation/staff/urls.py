# staff/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('change/<int:user_id>/', views.edit_user_view, name='change_user'),
    path('list/user', views.list_user_view, name='list_user'),
    path('list/books', views.list_book_view, name='view_list_book'),

]
