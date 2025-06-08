from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from books.models import Book

def add_reviews(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        content = request.POST.get('comment')  # Tên khớp với name="comment" trong HTML

        if content:
            Review.objects.create(book=book, content=content)
            return redirect('reviews:book_review', book_id=book.id)

    return render(request, 'reviews/add_reviews.html', {'book': book})


def book_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Review.objects.filter(book=book).order_by('-created_at')
    return render(request, 'reviews/book_review.html', {'book': book, 'reviews': reviews})
