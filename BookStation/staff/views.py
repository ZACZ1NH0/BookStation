from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.forms import CustomUserCreationForm
from accounts.forms import EditProfile
from books.forms import BookForm, AuthorForm, CategoryForm, PublisherForm
from books.models import Book, Author , Category, Publisher
from accounts.models import Users
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from unidecode import unidecode
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.core.files.base import ContentFile
import json, zipfile, os
from django.utils.dateparse import parse_date
from django.conf import settings
from .forms import BookImportForm
from django.http import HttpResponse
from pathlib import Path



@login_required
def staff_dashboard(request):
    can_add_user = request.user.has_perm('accounts.add_users')
    can_change_user = request.user.has_perm('accounts.change_users')
    can_view_user = request.user.has_perm('accounts.view_users')
    can_add_book = request.user.has_perm('books.add_book')
    can_add_category  = request.user.has_perm('books.add_category')
    can_add_publisher = request.user.has_perm('books.add_publisher')
    can_change_publisher = request.user.has_perm('books.change_publisher')
    can_view_publisher = request.user.has_perm('books.view_publisher')
    can_delete_publisher = request.user.has_perm('books.delete_publisher')
    can_add_author = request.user.has_perm('books.add_author')
    can_delete_book = request.user.has_perm('books.delete_book')
    can_change_book = request.user.has_perm('books.change_book')
    can_view_author = request.user.has_perm('books.view_authors')
    can_change_author = request.user.has_perm('books.change_author')
    can_delete_author = request.user.has_perm('books.delete_author')
    can_view_category = request.user.has_perm('books.view_category')
    can_delete_category = request.user.has_perm('books.delete_category')
    can_add_order = request.user.has_perm('orders.add_order')
    can_add_orderitem = request.user.has_perm('orders.add_orderitem')
    can_delete_order = request.user.has_perm('orders.delete_order')
    can_delete_orderitem = request.user.has_perm('orders.delete_orderitem')
    can_view_order = request.user.has_perm('orders.view_orders')
    can_view_orderitem = request.user.has_perm('orders.view_orderitem')
    can_change_order = request.user.has_perm('orders.change_order')
    can_view_orderitem = request.user.has_perm('orders.view_orderitem')
    can_change_orderitem = request.user.has_perm('orders.change_orderitem')


    return render(request, 'staff/dashboard_staff.html', {
        'can_add_user': can_add_user,
        'can_change_user': can_change_user,
        'can_view_user': can_view_user,

        'can_add_book': can_add_book,
        'can_change_book': can_change_book,
        'can_delete_book': can_delete_book,

        'can_add_category': can_add_category,
        'can_view_category': can_view_category,
        'can_delete_category': can_delete_category,

        'can_add_publisher': can_add_publisher,
        'can_change_publisher': can_change_publisher,
        'can_view_publisher': can_view_publisher,
        'can_delete_publisher': can_delete_publisher,

        'can_add_author': can_add_author,
        'can_view_author': can_view_author,
        'can_delete_author': can_delete_author,

        'can_add_order': can_add_order,
        'can_change_orderitem': can_change_orderitem,
        'can_view_orderitem': can_view_orderitem,
        'can_add_orderitem': can_add_orderitem,
        'can_delete_orderitem': can_delete_orderitem,


    })


def import_books_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        try:
            data = json.load(json_file)

            for book_data in data:
                author_name = book_data.get('author', 'Unknown')
                author_obj, _ = Author.objects.get_or_create(name=author_name)
                publisher_name = book_data.get('publisher', 'Unknown')
                publisher_obj, _ = Publisher.objects.get_or_create(name=publisher_name)
                book = Book.objects.create(
                    title=book_data['title'],
                    price=book_data['price'],
                    description=book_data.get('description', ''),
                    stock=book_data.get('stock', 0),
                    cover_image=book_data.get('cover_image', ''),
                    publication_date=book_data.get('publication_date', None),
                    author=author_obj,
                    publisher=publisher_obj,
                )

                for cat_name in book_data.get('categories', []):
                    category_obj, _ = Category.objects.get_or_create(name=cat_name)
                    book.categories.add(category_obj)
                book.save()
            messages.success(request, " Đã import dữ liệu thành công!")
            return redirect('')
        except json.JSONDecodeError:
            messages.error(request, " File JSON không hợp lệ.")
        except Exception as e:
            messages.error(request, f"⚠ Có lỗi xảy ra: {str(e)}")

    return render(request, 'staff/books/add_book.html')



def import_book_images(request):
    if request.method == 'POST' and request.FILES.get('image_zip'):
        zip_file = request.FILES['image_zip']
        try:
            with zipfile.ZipFile(zip_file) as zf:
                for filename in zf.namelist():
                    name = Path(filename).name
                    book = Book.objects.filter(cover_image=name).first()
                    if book:
                        with zf.open(filename) as f:
                            book.cover_image.save(name, ContentFile(f.read()), save=True)
                messages.success(request, "✔️ Đã nhập ảnh sách thành công.")
        except Exception as e:
            messages.error(request, f"❌ Lỗi khi xử lý ZIP: {e}")
    return render(request, 'staff/books/add_book.html')

@login_required
@permission_required('accounts.add_users', raise_exception=True)
def add_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo người dùng mới thành công!')
            return redirect('staff_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'staff/accounts/add_users.html', {'form': form})


@login_required
@permission_required('accounts.change_users', raise_exception=True)
def edit_user_view(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "Bạn không có quyền chỉnh sửa tài khoản quản trị cao nhất.")
        return redirect('staff_dashboard')
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=user)
        password_form = SetPasswordForm(user, request.POST)
        if 'update_profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Cập nhật người dùng thành công!')
                return redirect('staff_dashboard')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Đổi mật khẩu thành công!')
                return redirect('staff_dashboard')

    else:
        form = EditProfile(instance=user)
        password_form = SetPasswordForm(user)

    return render(request, 'staff/accounts/change_user.html', {
        'form': form,
        'password_form': password_form,
        'user': user,
    })


@login_required
@permission_required('accounts.view_users', raise_exception=True)
def list_user_view(request):
    User = get_user_model()  # Lấy User model hiện tại của dự án
    query = request.GET.get('q', '').strip()  # Không cần .lower() ở đây
    users_queryset = User.objects.filter(is_staff=False, is_superuser=False)

    if query:

        normalized_query = unidecode(query).lower()

        search_conditions = (
                Q(username__icontains=normalized_query) |
                Q(first_name__icontains=normalized_query) |
                Q(last_name__icontains=normalized_query) |
                Q(email__icontains=normalized_query)
        )

        users_queryset = users_queryset.filter(search_conditions)
    users_queryset = users_queryset.order_by('id')

    paginator = Paginator(users_queryset, 10)

    page_number = request.GET.get('page')
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:

        users = paginator.page(1)
    except EmptyPage:

        users = paginator.page(paginator.num_pages)

    can_change_user = request.user.has_perm('accounts.change_users')

    return render(request, 'staff/accounts/list_users.html', {
        'users': users,
        'can_change_user': can_change_user,
        'query': query,
    })


@login_required
@permission_required('books.view_book', raise_exception=True)
def list_book_view(request):
    query = request.GET.get('q', '').strip()
    books_queryset = Book.objects.all()

    if query:
        normalized_query = unidecode(query).lower()
        search_conditions = (
                Q(title__icontains=normalized_query) |
                Q(author__name__icontains=normalized_query) |
                Q(publisher__name__icontains=normalized_query)
        )

        books_queryset = books_queryset.filter(search_conditions)

    books_queryset = books_queryset.order_by('id')
    paginator = Paginator(books_queryset, 10)

    page_number = request.GET.get('page')
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'staff/books/view_book.html', context)


@login_required
@permission_required('books.add_book', raise_exception=True)
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"✔️ Đã thêm sách: {book.title}")
            return redirect('view_list_book')
        else:
            messages.error(request, '❌ Form không hợp lệ.')
    else:
        form = BookForm()  #

    return render(request, 'staff/books/add_book.html', {'form': form})



@login_required
@permission_required('books.change_book', raise_exception=True)
def book_change(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            form.save()
            form.save_m2m()
            return redirect('view_list_book')
    else:
        form = BookForm(instance=book)
    return render(request, 'staff/books/change_book.html', {'form': form, 'title': 'Change Book'})

@login_required
@permission_required('books.delete_book', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
    return redirect('view_list_book')


@login_required
@permission_required('books.view_author', raise_exception=True)
def view_list_author(request):
    query = request.GET.get('q', '').strip()
    authors_queryset = Author.objects.all()

    if query:
        normalized_query = unidecode(query).lower()
        search_conditions = (
                Q(name__icontains=normalized_query) |
                Q(nationality__icontains=normalized_query)
        )
        authors_queryset = authors_queryset.filter(search_conditions)
    authors_queryset = authors_queryset.order_by('id')
    paginator = Paginator(authors_queryset, 10)
    page_number = request.GET.get('page')
    try:
        authors = paginator.page(page_number)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)
    context = {
        'authors': authors,
        'query': query,
    }
    return render(request, 'staff/books/view_author.html', context)


@login_required
@permission_required('books.add_author', raise_exception=True)
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_authors')
    else:
        form = AuthorForm()
    return render(request, 'staff/books/add_author.html', {'form': form})


@login_required
@permission_required('books.change_author', raise_exception=True)
def edit_author(request,pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('list_authors')
    else :
        form = AuthorForm(instance=author)
    return render(request,'staff/books/change_author.html',{'form': form})


@login_required
@permission_required('books.delete_author', raise_exception=True)
def delete_author(request,pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('list_authors')
    else :
        return render(request,'staff/books/view_author.html',{'author': author})


@login_required
@permission_required('books.view_category', raise_exception=True)
def list_category(request):
    categories = Category.objects.all()
    return render(request, 'staff/books/view_category.html', {'categories': categories})


@login_required
@permission_required('books.change_category', raise_exception=True)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'staff/books/change_category.html', {'form': form, 'title': 'Edit Category'})



@login_required
@permission_required('books.add_category', raise_exception=True)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_category')
    else:
        form = CategoryForm()
    return render(request, 'staff/books/add_category.html', {'form': form, 'title': 'Add Category'})


@login_required
@permission_required('books.delete_category', raise_exception=True)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('list_category')
    return render(request, 'staff/books/view_category.html', {'category': category})


@login_required
@permission_required('books.view_publisher', raise_exception=True)
def list_publisher(request):
    publishers = Publisher.objects.all()
    return render(request, 'staff/books/view_publisher.html', {'publishers': publishers})


@login_required
@permission_required('books.delete_publisher', raise_exception=True)
def delete_publisher(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        publisher.delete()
        return redirect('list_publisher')
    return render(request, 'staff/books/view_publisher.html', {'publisher': publisher})


@login_required
@permission_required('books.add_publisher', raise_exception=True)
def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_publisher')
    else:
        form = PublisherForm()
    return render(request, 'staff/books/add_publisher.html', {'form': form, 'title': 'Add Publisher'})


@login_required
@permission_required('books.change_publisher', raise_exception=True)
def edit_publisher(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('list_publisher')
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'staff/books/change_publisher.html', {'form': form, 'title': 'Edit Publisher'})

