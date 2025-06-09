from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from books.models import Book
from .forms import ReviewForm 

def add_reviews(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book 
            review.save()
            
            return redirect('reviews:book_review', book_id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_reviews.html', {'book': book, 'form': form})

def book_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book).order_by('-created_at')
    return render(request, 'reviews/book_review.html', {'book': book, 'reviews': reviews})