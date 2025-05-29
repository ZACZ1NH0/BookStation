from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CustomUserCreationForm,EditProfile
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from books.models import Book

def home_view(request):
    books = Book.objects.all()[:50]
    return render(request, 'accounts/home.html', {'books': books})

def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công')
            return redirect('profile')
    else:
        form = EditProfile(instance=user)
    return render(request, 'accounts/profile.html', {'form': form, 'user': user})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, 'Đăng kí thành công !!!')
            return redirect('login')
    else:
         form= CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu sai !')
    return render (request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        profile_form = EditProfile(request.POST)
        password_form = PasswordChangeForm(user=user)
        if profile_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Cập nhật thành công')
            return redirect('edit_profile')
        else:
            messages.error(request,'Có lỗi xảy ra, vui lòng thử lại!')
    else:
        profile_form = EditProfile(instance=request.user)
        password_form = PasswordChangeForm(user=user)
    return render(request, 'accounts/edit_profile.html',
            {'profile_form': profile_form,
                    'password_form': password_form})


