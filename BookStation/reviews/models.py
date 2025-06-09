from django.db import models
from books.models import Book

# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)