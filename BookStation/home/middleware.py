from django.shortcuts import redirect
from django.urls import reverse


class RoleRedict:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        EXEMPT_PREFIXES = [
            '/admin/',
            '/accounts/login/',
            '/accounts/register/',

        ]

        EXEMPT_URLS = [
            '/',
            '/home/',
            'staff_dashboard',
        ]

        # Bỏ qua tất cả các URL admin và auth
        if any(request.path.startswith(prefix) for prefix in EXEMPT_PREFIXES):
            return self.get_response(request)

        # Bỏ qua các URL cụ thể
        if request.path in EXEMPT_URLS:
            return self.get_response(request)

        if request.user.is_authenticated:
            if request.path == '/':
                if request.user.is_superuser:
                    return redirect('admin')
                elif request.user.is_staff:
                    return redirect('staff_dashboard')
                else:
                    return redirect('home_customer')
        else:
            return redirect('home')

        return self.get_response(request)