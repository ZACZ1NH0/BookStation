from django.contrib import admin

# Register your models here.
from .models import Book
from .models import Author, Publisher, Category
admin.site.register(Author) 
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Category)