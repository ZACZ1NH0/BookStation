from django.shortcuts import render
from books.models import Book
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


# home/views.py
# def home_view(request):
#     if not request.user.is_authenticated:
#         books = Book.objects.all()[:50]
#         return render(request, 'home/home.html', {'books': books})
#     return render(request, 'home/home.html')
# @login_required
# def home_admin(request):
#     # Bỏ @user_passes_test vì middleware đã xử lý phân quyền
#     return render(request, 'home/home_admin.html')
#
# # @login_required
# # def home_staff(request):
# #     return render(request, 'staff/templates/staff/dasboard_staff.html')
#
# @login_required
# def home_customer(request):
#     return render(request, 'home/home_customer.html')

def home_view(request):
    if not request.user.is_authenticated:
        books = Book.objects.all()[:50]
        return render(request, 'home/home.html', {'books': books})
    context = {
        'is_staff': request.user.is_authenticated and request.user.is_staff,
        'is_superuser': request.user.is_authenticated and request.user.is_superuser,
    }
    return render(request, 'home/home.html', context)