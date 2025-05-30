#
# from django.shortcuts import redirect
# from django.urls import reverse
#
# class RoleRedict:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Danh sách URL KHÔNG áp dụng chuyển hướng (phải khớp chính xác)
#         EXEMPT_URLS = [
#             '/admin/',
#             '/accounts/login/',
#             '/logout/',
#             '/home/',
#             '/home_admin/',
#             '/home_staff/',
#             '/home_customer/',
#             '/admin/login/?next=/admin/',
#         ]
#
#         if request.path in EXEMPT_URLS:
#             return self.get_response(request)
#         if request.user.is_authenticated:
#             if request.path == '/':
#                 if request.user.is_superuser:
#                     return redirect('home_admin')
#                 elif request.user.is_staff:
#                     return redirect('home_staff')
#                 else:
#                     return redirect('home_customer')
#         else:
#             if request.path != '/':
#                 return redirect('home')
#
#         return self.get_response(request)
from django.shortcuts import redirect
from django.urls import reverse


class RoleRedict:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Danh sách URL prefix không áp dụng chuyển hướng
        EXEMPT_PREFIXES = [
            '/admin/',
            '/accounts/login/',
            '/logout/',
        ]

        # Danh sách URL chính xác không áp dụng chuyển hướng
        EXEMPT_URLS = [
            '/',
            '/home/',
            '/home_admin/',
            '/home_staff/',
            '/home_customer/',
        ]

        # Bỏ qua tất cả các URL admin và auth
        if any(request.path.startswith(prefix) for prefix in EXEMPT_PREFIXES):
            return self.get_response(request)

        # Bỏ qua các URL cụ thể
        if request.path in EXEMPT_URLS:
            return self.get_response(request)

        # Xử lý chuyển hướng cho user đã đăng nhập
        if request.user.is_authenticated:
            if request.path == '/':
                if request.user.is_superuser:
                    return redirect('home_admin')
                elif request.user.is_staff:
                    return redirect('home_staff')
                else:
                    return redirect('home_customer')
        else:
            # Chuyển hướng user chưa đăng nhập về trang chủ
            return redirect('home')

        return self.get_response(request)