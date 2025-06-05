from django.urls import path
from . import views


urlpatterns = [
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('change/<int:user_id>/', views.edit_user_view, name='change_user'),
    path('list/users', views.list_user_view, name='list_user'),
    path('list/books', views.list_book_view, name='view_list_book'),
    path('books/change/<int:pk>/', views.book_change, name='book_change'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/add/', views.book_add, name='book_add'),
    path('list/authors',views.view_list_author, name='list_authors'),
    path('change/author/<int:id>/', views.edit_author, name='change_user'),
]
