from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import CustomUserCreationForm
from accounts.forms import EditProfile
from books.forms import BookForm, AuthorForm, CategoryForm, PublisherForm
from books.models import Book, Author , Category, Publisher
from accounts.models import Users
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from unidecode import unidecode
from orders.forms import OrderForm
from orders.models import Order



@login_required
def staff_dashboard(request):
    can_add_user = request.user.has_perm('accounts.add_users')
    can_change_user = request.user.has_perm('accounts.change_users')
    can_view_user = request.user.has_perm('accounts.view_users')
    can_add_order = request.user.has_perm('orders.add_order')
    can_add_book = request.user.has_perm('books.add_book')
    can_add_category  = request.user.has_perm('books.add_category')
    can_add_publisher = request.user.has_perm('books.add_publisher')
    can_add_author = request.user.has_perm('books.add_author')
    can_delete_book = request.user.has_perm('books.delete_book')
    can_change_book = request.user.has_perm('books.change_book')
    can_view_author = request.user.has_perm('books.view_authors')
    can_change_author = request.user.has_perm('books.change_author')
    can_delete_author = request.user.has_perm('books.delete_author')
    can_view_category = request.user.has_perm('books.view_category')
    can_delete_category = request.user.has_perm('books.delete_category')
    return render(request, 'staff/dashboard_staff.html', {
        'can_add_user': can_add_user,
        'can_change_user': can_change_user,
        'can_view_user': can_view_user,
        'can_add_order': can_add_order,
        'can_add_book': can_add_book,
        'can_add_category': can_add_category,
        'can_add_publisher': can_add_publisher,
        'can_add_author': can_add_author,
        'can_delete_book' : can_delete_book,
        'can_change_book' : can_change_book,
        'can_view_author': can_view_author,
        'can_delete_author': can_delete_author,
        'can_view_category': can_view_category,
        # 'books':Book.objects.all(),
    })


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
    query = request.GET.get('q', '').strip().lower()
    all_users = Users.objects.filter(is_staff=False, is_superuser=False)
    filtered_users = []
    if query:
        normalized_query = unidecode(query)
        for user in all_users:
            if any(
                normalized_query in unidecode((getattr(user, field) or '').lower())
                for field in ['username', 'first_name', 'last_name', 'email']
            ):
                filtered_users.append(user)
    else:
        filtered_users = all_users
    can_change_user = request.user.has_perm('accounts.change_users')
    return render(request, 'staff/accounts/list_users.html', {
        'users': filtered_users,
        'can_change_user': can_change_user,
    })



@login_required
@permission_required('books.view_book', raise_exception=True)
def list_book_view(request):
    query = request.GET.get('q', '').strip().lower()
    all_books = Book.objects.all()
    filtered_books = []

    if query:
        normalized_query = unidecode(query)
        for book in all_books:
            if any(
                normalized_query in unidecode((getattr(book, field) or '').lower())
                for field in ['title', 'author']
            ):
                filtered_books.append(book)
    else:
        filtered_books = all_books

    return render(request, 'staff/books/view_book.html', {
        'books': all_books,
    })

@login_required
@permission_required('books.add_book', raise_exception=True)
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book = form.save()
            form.save_m2m()
            return redirect('view_list_book')
    else:
        form = BookForm()
    return render(request, 'staff/books/add_book.html', {'form': form, 'title': 'Add Book'})


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
    authors = Author.objects.all()
    return render(request, 'staff/books/view_author.html', {'authors': authors})


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
    return render(request, 'staff/books/view_category.html', {'categories': category})


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

