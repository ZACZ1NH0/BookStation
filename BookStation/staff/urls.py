from django.urls import path
from . import views


urlpatterns = [
    # User
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('change/<int:user_id>/', views.edit_user_view, name='change_user'),
    path('list/users', views.list_user_view, name='list_user'),
    # Book
    path('list/books', views.list_book_view, name='view_list_book'),
    path('books/change/<int:pk>/', views.book_change, name='book_change'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/add/', views.book_add, name='book_add'),
    # Author
    path('list/authors',views.view_list_author, name='list_authors'),
    path('edit/author/<int:pk>', views.edit_author, name='change_author'),
    path('delete/author/<int:pk>', views.delete_author, name='delete_author'),
    path('add/author', views.add_author, name='add_author'),
    # Publisher
    path('list/publishers/', views.list_publisher, name='list_publisher'),
    path('publisher/add/', views.add_publisher, name='add_publisher'),
    path('publisher/<int:pk>/edit/', views.edit_publisher, name='change_publisher'),
    path('publisher/<int:pk>/delete/', views.delete_publisher, name='delete_publisher'),
    # Category
    path('list/categories/', views.list_category, name='list_category'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='change_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),


]
