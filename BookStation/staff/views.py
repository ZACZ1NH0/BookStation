from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.forms import CustomUserCreationForm
from accounts.forms import EditProfile
from books.forms import BookForm, AuthorForm, CategoryForm, PublisherForm, BookImportForm
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
from django.conf import settings


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


def import_books(request):
    if request.method == "POST":
        form = BookImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Lấy file JSON và ZIP
            json_file = request.FILES['json_file']
            zip_file = request.FILES['image_zip']

            # Đọc nội dung JSON
            books_data = json.load(json_file)

            # Giải nén file ảnh vào bộ nhớ tạm
            with zipfile.ZipFile(zip_file) as zf:
                for book_item in books_data:
                    title = book_item.get("title")
                    author_name = book_item.get("author")
                    category_name = book_item.get("category")
                    publisher_name = book_item.get("publisher")
                    image_name = book_item.get("image")  # ví dụ "book123.jpg"

                    # Tạo hoặc lấy các liên kết
                    author, _ = Author.objects.get_or_create(name=author_name)
                    category, _ = Category.objects.get_or_create(name=category_name)
                    publisher, _ = Publisher.objects.get_or_create(name=publisher_name)

                    # Lấy ảnh từ zip
                    image_file = zf.read(image_name)

                    # Tạo book và gán ảnh
                    book = Book(
                        title=title,
                        author=author,
                        category=category,
                        publisher=publisher,
                    )
                    book.cover.save(image_name, ContentFile(image_file), save=True)

            return redirect('view_list_book')
    else:
        form = BookImportForm()
    return  redirect('book_add')

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

    # Bắt đầu với tất cả người dùng không phải staff/superuser
    # Bạn có thể điều chỉnh filter này tùy theo định nghĩa người dùng của bạn
    users_queryset = User.objects.filter(is_staff=False, is_superuser=False)

    if query:
        # Chuyển đổi query về dạng không dấu và chữ thường một lần
        normalized_query = unidecode(query).lower()

        # Xây dựng các điều kiện tìm kiếm bằng Q objects
        # Sử dụng __icontains để tìm kiếm không phân biệt chữ hoa/thường
        # unidecode() cho phép tìm kiếm không dấu
        search_conditions = (
                Q(username__icontains=normalized_query) |
                Q(first_name__icontains=normalized_query) |
                Q(last_name__icontains=normalized_query) |
                Q(email__icontains=normalized_query)
        )
        # Nếu muốn tìm kiếm không dấu chính xác hơn, bạn có thể áp dụng unidecode cho trường
        # trong database nếu bạn đang sử dụng PostgreSQL với django-unaccent,
        # nhưng cách này là phổ biến và đủ cho đa số trường hợp.

        users_queryset = users_queryset.filter(search_conditions)

    # Sắp xếp queryset để phân trang hoạt động ổn định
    users_queryset = users_queryset.order_by('id')

    # Thiết lập phân trang
    paginator = Paginator(users_queryset, 10)  # 10 người dùng mỗi trang

    page_number = request.GET.get('page')
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page không phải số nguyên, hiển thị trang đầu tiên
        users = paginator.page(1)
    except EmptyPage:
        # Nếu page vượt quá số trang có sẵn, hiển thị trang cuối cùng
        users = paginator.page(paginator.num_pages)

    # Kiểm tra quyền thay đổi người dùng
    can_change_user = request.user.has_perm('accounts.change_users')

    return render(request, 'staff/accounts/list_users.html', {
        'users': users,  # Đây là đối tượng Page đã được phân trang
        'can_change_user': can_change_user,
        'query': query,  # Quan trọng: Truyền query vào context để giữ lại trong liên kết phân trang
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

    books_queryset = books_queryset.order_by('id')  # Hoặc theo title, tùy ý

    # Thiết lập phân trang
    paginator = Paginator(books_queryset, 10)  # 10 sách mỗi trang

    page_number = request.GET.get('page')
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        # Nếu page không phải số nguyên, hiển thị trang đầu tiên
        books = paginator.page(1)
    except EmptyPage:
        # Nếu page vượt quá số trang có sẵn, hiển thị trang cuối cùng
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,  # Đây là đối tượng Page đã được phân trang
        'query': query,  # Quan trọng: Truyền query vào context để giữ lại trong liên kết phân trang
    }
    return render(request, 'staff/books/view_book.html', context)


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
    # Lấy từ khóa tìm kiếm từ request.GET, mặc định là chuỗi rỗng
    query = request.GET.get('q', '').strip()

    # Bắt đầu với tất cả các tác giả
    authors_queryset = Author.objects.all()

    # Nếu có từ khóa tìm kiếm, lọc queryset
    if query:
        # Chuyển đổi từ khóa tìm kiếm về dạng không dấu và chữ thường để tìm kiếm linh hoạt hơn
        normalized_query = unidecode(query).lower()

        # Xây dựng các điều kiện tìm kiếm bằng Q objects
        # Tìm kiếm theo tên hoặc quốc tịch (không phân biệt chữ hoa/thường, không dấu)
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
        # Nếu page_number không phải số nguyên, hiển thị trang đầu tiên
        authors = paginator.page(1)
    except EmptyPage:
        # Nếu page_number vượt quá số trang có sẵn, hiển thị trang cuối cùng
        authors = paginator.page(paginator.num_pages)

    # Chuẩn bị context để truyền dữ liệu sang template
    context = {
        'authors': authors,  # Đối tượng Page đã được phân trang (chứa các tác giả của trang hiện tại)
        'query': query,  # Truyền lại từ khóa tìm kiếm để giữ nó trên ô tìm kiếm và các liên kết phân trang
    }
    # Render template 'staff/authors/list_authors.html'
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


# @permission_required('orders.view_order', raise_exception=True)
# def list_order_view(request):
#     query = request.GET.get('q')
#     if query:
#         orders = Order.objects.filter(
#             Q(user__username__icontains=query) |
#             Q(status__icontains=query)
#         ).order_by('-created_at')
#     else:
#         orders = Order.objects.all().order_by('-created_at')
#     return render(request, 'staff/orders/view_order.html', {'orders': orders, 'query': query})
#
#
#
# @permission_required('orders.add_order', raise_exception=True)
# def add_order_view(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Đã thêm đơn hàng mới.')
#             return redirect('view_orders')
#     else:
#         form = OrderForm()
#     return render(request, 'staff/orders/add_order.html', {'form': form})
#
#
# @permission_required('orders.change_order', raise_exception=True)
# def edit_order_view(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST, instance=order)
#         formset = OrderItemFormSet(request.POST, instance=order)
#         if order_form.is_valid() and formset.is_valid():
#             order_form.save()
#             # Gán price cho OrderItem mới hoặc sửa
#             for form in formset:
#                 if form.cleaned_data and not form.cleaned_data.get('DELETE'):
#                     instance = form.save(commit=False)
#                     if not instance.price or instance.book.price != instance.price:  # Cập nhật price nếu cần
#                         instance.price = instance.book.price or Decimal('0.00')
#                     instance.save()
#             formset.save()
#             messages.success(request, "Đơn hàng đã được cập nhật thành công.")
#             return redirect('staff:list_order')  # Cập nhật URL nếu khác
#         else:
#             messages.error(request, "Vui lòng sửa các lỗi bên dưới.")
#     else:
#         order_form = OrderForm(instance=order)
#         formset = OrderItemFormSet(instance=order)
#
#     total_amount = order.total_amount()
#     customer = order.customer
#
#     return render(request, 'staff/orders/change_order.html', {
#         'order_form': order_form,
#         'formset': formset,
#         'order': order,
#         'total_amount': total_amount,
#         'customer': customer,
#     })
#
# @permission_required('orders.delete_order', raise_exception=True)
# def delete_order_view(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     if request.method == 'POST':
#         order.delete()
#         messages.success(request, 'Đã xóa đơn hàng.')
#         return redirect('view_orders')
#     return render(request, '', {'order': order})
#
#
# @permission_required('orders.add_orderitem', raise_exception=True)
# def add_order_item_view(request):
#     if request.method == 'POST':
#         form = OrderItemFormSet(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Đã thêm sản phẩm vào đơn hàng.')
#             return redirect('staff:list_order_item')
#     else:
#         form = OrderItemFormSet()
#     return render(request, 'staff/orders/add_orderitem.html', {'form': form})
#
#
# @permission_required('orders.view_order', raise_exception=True)
# def order_item_detail(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     return render(request, 'staff/orders/view_orderitem.html', {'order': order})
#
# @login_required
# @permission_required('orders.change_orderitem', raise_exception=True)
# def edit_order_item_view(request, item_id):
#     item = get_object_or_404(OrderItem, id=item_id)
#     if request.method == 'POST':
#         form = OrderItemFormSet(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Đã cập nhật sản phẩm trong đơn hàng.')
#             return redirect('staff:list_order_item')
#     else:
#         form = OrderItemFormSet(instance=item)
#     return render(request, 'staff/orders/change_orderitem.html', {'form': form, 'item': item})
#
#
# @permission_required('orders.delete_orderitem', raise_exception=True)
# def delete_order_item_view(request, item_id):
#     item = get_object_or_404(OrderItem, id=item_id)
#     if request.method == 'POST':
#         item.delete()
#         messages.success(request, 'Đã xóa sản phẩm khỏi đơn hàng.')
#         return redirect('list_order_item')
#     return render(request, '', {'item': item})
#
