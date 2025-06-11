from django.db import models
from django.conf import settings
from books.models import Book
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('shipping', 'Đang giao'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
        ('card', 'Thẻ tín dụng'),
        ('momo', 'Ví MoMo'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tổng tiền")

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.username if self.customer else 'Guest'}"

    def get_items_total(self):
        """Tính tổng tiền các sản phẩm (chưa tính khuyến mãi)"""
        return sum(item.subtotal() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # giá tại thời điểm mua

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def subtotal(self):
        if self.price is None:
            return Decimal('0.00')  # Trả về 0 nếu price là None
        return self.quantity * self.price
