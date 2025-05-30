from django.shortcuts import render
from books.models import Book
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


# home/views.py
def home_view(request):
    # Bỏ hoàn toàn logic redirect trong view, chỉ xử lý trong middleware
    if not request.user.is_authenticated:
        books = Book.objects.all()[:50]
        return render(request, 'home/home.html', {'books': books})
    # Đã login sẽ được middleware redirect trước khi vào view này
    return render(request, 'home/home.html')  # Fallback

@login_required
def home_admin(request):
    # Bỏ @user_passes_test vì middleware đã xử lý phân quyền
    return render(request, 'home/home_admin.html')

@login_required
def home_staff(request):
    return render(request, 'home/home_staff.html')

@login_required
def home_customer(request):
    return render(request, 'home/home_customer.html')