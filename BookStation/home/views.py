from django.shortcuts import render
from books.models import Book

# Create your views here.

def home_view(request):
    books = Book.objects.all()[:20]
    return render(request, 'home/home.html', {'books': books})


