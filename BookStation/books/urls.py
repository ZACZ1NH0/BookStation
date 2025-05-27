from django.urls import path
from . import views

urlpatterns = [
    # BOOK
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # AUTHOR
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.author_add, name='author_add'),
    path('authors/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # PUBLISHER
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/add/', views.publisher_add, name='publisher_add'),
    path('publishers/<int:pk>/', views.publisher_detail, name='publisher_detail'),
    path('publishers/<int:pk>/edit/', views.publisher_edit, name='publisher_edit'),
    path('publishers/<int:pk>/delete/', views.publisher_delete, name='publisher_delete'),

    # CATEGORY
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
