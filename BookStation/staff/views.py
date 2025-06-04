from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import CustomUserCreationForm
from accounts.forms import EditProfile
from books.forms import BookForm
from books.models import Book
from accounts.models import Users
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from unidecode import unidecode


@login_required
def staff_dashboard(request):
    can_add_user = request.user.has_perm('accounts.add_users')
    can_change_user = request.user.has_perm('accounts.change_users')
    can_view_user = request.user.has_perm('accounts.view_users')
    can_add_order = request.user.has_perm('orders.add_orders')
    can_add_book = request.user.has_perm('books.add_books')
    can_add_category  = request.user.has_perm('books.add_category')
    can_add_publisher = request.user.has_perm('books.add_publishers')
    can_add_author = request.user.has_perm('books.add_authors')
    can_delete_book = request.user.has_perm('books.delete_books')
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
                update_session_auth_hash(request, user)  # giữ login sau khi đổi mật khẩu
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

