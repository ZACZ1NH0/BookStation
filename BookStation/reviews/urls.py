from django.urls import path
from . import views

app_name = 'reviews'  

urlpatterns = [
    path('add_reviews/<int:book_id>/', views.add_reviews, name='add_reviews'),
    path('book_review/<int:book_id>/', views.book_review, name='book_review'),
]