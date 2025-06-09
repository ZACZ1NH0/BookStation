from django.shortcuts import render
from django.db.models import Sum, Count, F, DecimalField, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from books.models import Book
from orders.models import Order, OrderItem
import pandas as pd
from django.http import HttpResponse
from django.core.paginator import Paginator
from accounts.models import Users
def get_revenue_stats():
    """Thống kê doanh thu"""
    # Tính tổng doanh thu từ các đơn hàng đã hoàn thành
    total_revenue = OrderItem.objects.filter(
        order__status='completed'
    ).aggregate(
        total=Sum(F('quantity') * F('price'), output_field=DecimalField())
    )['total'] or 0

    # Thống kê doanh thu theo tháng
    revenue_by_month = OrderItem.objects.filter(
        order__status='completed'
    ).annotate(
        month=TruncMonth('order__created_at')
    ).values('month').annotate(
        revenue=Sum(F('quantity') * F('price'), output_field=DecimalField()),
        order_count=Count('order__id', distinct=True)
    ).order_by('-month')[:6]

    return {
        'total_revenue': total_revenue,
        'revenue_by_month': revenue_by_month
    }

def get_customer_order_stats():
    """Thống kê khách hàng và đơn hàng"""
    # Thống kê khách hàng
    total_customers = Users.objects.count()  # Changed from User to Users
    new_customers = Users.objects.filter(  # Changed from User to Users
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Thống kê đơn hàng
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_by_status = orders.values('status').annotate(count=Count('id'))
    
    # Top khách hàng theo doanh số
    top_customers = Users.objects.annotate(  # Changed from User to Users
        total_spent=Sum(F('order__items__quantity') * F('order__items__price'), 
                       output_field=DecimalField())
    ).order_by('-total_spent')[:5]

    return {
        'total_customers': total_customers,
        'new_customers': new_customers,
        'total_orders': total_orders,
        'orders_by_status': orders_by_status,
        'top_customers': top_customers
    }

def get_book_inventory_stats():
    """Thống kê tình trạng sách"""
    # Thống kê tổng quan về sách
    total_books = Book.objects.count()
    out_of_stock = Book.objects.filter(stock=0)
    low_stock = Book.objects.filter(stock__gt=0, stock__lte=5)
    
    # Top sách bán chạy
    best_selling = Book.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by('-total_sold')[:10]

    return {
        'total_books': total_books,
        'out_of_stock_books': out_of_stock,
        'low_stock_books': low_stock,
        'best_selling_books': best_selling
    }

def analytics_dashboard(request):
    """View chính cho dashboard analytics"""
    context = {
        **get_revenue_stats(),
        **get_customer_order_stats(),
        **get_book_inventory_stats()
    }
    return render(request, 'analytics/dashboard.html', context)

def book_inventory_detail(request):
    """Thống kê chi tiết về sách và kho"""
    # Xử lý tìm kiếm
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-stock')  # Mặc định sắp xếp theo tồn kho giảm dần
    
    books = Book.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).select_related('author', 'publisher')
    
    # Tìm kiếm
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(publisher__name__icontains=search_query)
        )
    
    # Sắp xếp
    books = books.order_by(sort_by)
    
    # Phân trang
    paginator = Paginator(books, 20)  # 20 items mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Xuất Excel
    if request.GET.get('export') == 'excel':
        # Tạo DataFrame
        data = []
        for book in books:
            data.append({
                'Tên Sách': book.title,
                'Tác Giả': book.author.name,
                'NXB': book.publisher.name,
                'Tồn Kho': book.stock,
                'Đã Bán': book.total_sold or 0,
                'Giá': book.price
            })
        
        df = pd.DataFrame(data)
        
        # Tạo response Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="book_inventory.xlsx"'
        df.to_excel(response, index=False)
        return response

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_books': books.count(),
        'out_of_stock': books.filter(stock=0).count(),
        'low_stock': books.filter(stock__gt=0, stock__lte=5).count(),
    }
    
    return render(request, 'analytics/book_inventory_detail.html', context)