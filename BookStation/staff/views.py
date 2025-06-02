from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from accounts.models import Users
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash


@login_required
def staff_dashboard(request):
    can_add_user = request.user.has_perm('accounts.add_users')
    can_change_user = request.user.has_perm('accounts.change_users')
    can_view_user = request.user.has_perm('accounts.view_users')
    return render(request, 'staff/dashboard_staff.html', {
        'can_add_user': can_add_user,
        'can_change_user': can_change_user,
        'can_view_user': can_view_user,
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
    return render(request, 'staff/add_users.html', {'form': form})


@login_required
@permission_required('accounts.change_users', raise_exception=True)
def edit_user_view(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, "Bạn không có quyền chỉnh sửa tài khoản quản trị cao nhất.")
        return redirect('staff_dashboard')
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        password_form = SetPasswordForm(user, request.POST)

        if 'update_profile' in request.POST:
            # Xử lý cập nhật thông tin user
            if form.is_valid():
                form.save()
                messages.success(request, 'Cập nhật người dùng thành công!')
                return redirect('staff_dashboard')

        elif 'change_password' in request.POST:
            # Xử lý đổi mật khẩu
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)  # giữ login sau khi đổi mật khẩu
                messages.success(request, 'Đổi mật khẩu thành công!')
                return redirect('staff_dashboard')

    else:
        form = CustomUserChangeForm(instance=user)
        password_form = SetPasswordForm(user)

    return render(request, 'staff/change_user.html', {
        'form': form,
        'password_form': password_form,
        'user': user,
    })
@login_required
@permission_required('accounts.view_users', raise_exception=True)
def list_user_view(request):
    users = Users.objects.filter(is_staff=False, is_superuser=False)
    can_change_user = request.user.has_perm('accounts.change_users')
    return render(request, 'staff/list_users.html', {
        'users': users,
        'can_change_user': can_change_user,
    })