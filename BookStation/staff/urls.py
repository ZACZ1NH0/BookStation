from django.urls import path
from . import views


urlpatterns = [

    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # User
    path('add_user/', views.add_user_view, name='add_user'),
    path('change/<int:user_id>/', views.edit_user_view, name='change_user'),
    path('list/users', views.list_user_view, name='list_user'),
    # Book
    path('list/books', views.list_book_view, name='view_list_book'),
    path('books/addbook', views.import_books, name="import_books"),
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
    path('publisher/edit/<int:pk>/', views.edit_publisher, name='change_publisher'),
    path('publisher/delete/<int:pk>/', views.delete_publisher, name='delete_publisher'),
    # Category
    path('list/categories/', views.list_category, name='list_category'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='change_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # # Order
    # path('orders/', views.list_order_view, name='list_order'),
    # path('orders/add/', views.add_order_view, name='add_order'),
    # path('orders/edit/<int:order_id>/', views.edit_order_view, name='edit_order'),
    # path('orders/<int:order_id>/delete/', views.delete_order_view, name='delete_order'),
    #
    # # OrderItem
    # path('order_item/detal/', views.order_item_detail, name='order_item_detal'),
    # path('order-items/add/', views.add_order_item_view, name='add_order_item'),
    # # path('order-items/edit/<int:item_id>/', views.ed, name='edit_order_item'),
    # path('order-items/<int:item_id>/delete/', views.delete_order_item_view, name='delete_order_item'),


]
