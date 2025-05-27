from django.urls import path
from . import views

urlpatterns = [
    # BOOK
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # AUTHOR
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/update/', views.author_update, name='author_update'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # PUBLISHER
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/create/', views.publisher_create, name='publisher_create'),
    path('publishers/<int:pk>/', views.publisher_detail, name='publisher_detail'),
    path('publishers/<int:pk>/update/', views.publisher_update, name='publisher_update'),
    path('publishers/<int:pk>/delete/', views.publisher_delete, name='publisher_delete'),

    # CATEGORY
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
