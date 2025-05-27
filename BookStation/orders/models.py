from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.username if self.customer else 'Guest'}"

    def total_amount(self):
        return sum(item.subtotal() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # giá tại thời điểm mua

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def subtotal(self):
        return self.quantity * self.price
