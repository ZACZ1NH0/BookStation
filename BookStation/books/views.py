from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Category, Publisher
from .forms import BookForm, AuthorForm, CategoryForm, PublisherForm
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
def book_list(request):
    Book.cover_image.field.upload_to = 'book_covers/'  # Đảm bảo đường dẫn đúng
    books = Book.objects.all()
    paginator = Paginator(books, 20)  # 20 sách mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'books': page_obj.object_list  # Thêm books vào context
    }

    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

def book_search(request):
    query = request.GET.get('q','')
    results = Book.objects.filter(title__icontains = query) if query else []
    return render(request, 'books/search_results.html', {
        'query': query,
        'results': results
    })



# @user_passes_test(lambda u: u.is_superuser or u.is_staff)
# def book_add(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             book = form.save()
#             # Lưu categories ManyToMany
#             form.save_m2m()
#             return redirect('book_list')
#     else:
#         form = BookForm()
#     return render(request, 'books/book_form.html', {'form': form, 'title': 'Add Book'})

# @user_passes_test(lambda u: u.is_superuser or u.is_staff)
# def book_edit(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES, instance=book)
#         if form.is_valid():
#             form.save()
#             form.save_m2m()
#             return redirect('book_list')
#     else:
#         form = BookForm(instance=book)
#     return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})

# @user_passes_test(lambda u: u.is_superuser or u.is_staff)
# def book_delete(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     if request.method == 'POST':
#         book.delete()
#         # return redirect('view_list_book')
#         return render(request, 'books/book_confirm_delete.html', {'book': book})
#     return redirect('view_list_book')

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'authors/author_list.html', {'authors': authors})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    return render(request, 'authors/author_detail.html', {'author': author, 'books': books})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('authors:author_list')
    else:
        form = AuthorForm()
    return render(request, 'authors/author_form.html', {'form': form, 'title': 'Add Author'})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors:author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'authors/author_form.html', {'form': form, 'title': 'Edit Author'})

@user_passes_test(lambda u: u.is_superuser)
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('authors:author_list')
    return render(request, 'authors/author_confirm_delete.html', {'author': author})

def publisher_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'publishers/publisher_list.html', {'publishers': publishers})

def publisher_detail(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    books = Book.objects.filter(publisher=publisher)
    return render(request, 'publishers/publisher_detail.html', {
        'publisher': publisher,
        'books': books
    })

@user_passes_test(lambda u: u.is_superuser)
def publisher_add(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('publishers:publisher_list')
    else:
        form = PublisherForm()
    return render(request, 'publishers/publisher_form.html', {'form': form, 'title': 'Add Publisher'})

@user_passes_test(lambda u: u.is_superuser)
def publisher_edit(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('publishers:publisher_list')
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'publishers/publisher_form.html', {'form': form, 'title': 'Edit Publisher'})

@user_passes_test(lambda u: u.is_superuser)
def publisher_delete(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        publisher.delete()
        return redirect('publishers:publisher_list')
    return render(request, 'publishers/publisher_confirm_delete.html', {'publisher': publisher})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(categories=category)
    return render(request, 'categories/category_detail.html', {
        'category': category,
        'books': books
    })

@user_passes_test(lambda u: u.is_superuser)
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories:category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form, 'title': 'Add Category'})

@user_passes_test(lambda u: u.is_superuser)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form, 'title': 'Edit Category'})

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories:category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})
