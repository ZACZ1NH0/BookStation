from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class Promotion(models.Model):
    PROMOTION_TYPES = [
        ('public', 'Công khai'),
        ('private', 'Riêng tư'),
    ]
    
    DISCOUNT_TYPES = [
        ('percentage', 'Phần trăm'),
        ('fixed', 'Số tiền cố định'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('expired', 'Hết hạn'),
    ]

    # Thông tin cơ bản
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã khuyến mãi")
    name = models.CharField(max_length=200, verbose_name="Tên khuyến mãi")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    # Loại khuyến mãi
    promotion_type = models.CharField(max_length=10, choices=PROMOTION_TYPES, default='public', verbose_name="Loại khuyến mãi")
    
    # Loại giảm giá
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, verbose_name="Loại giảm giá")
    
    # Giá trị giảm
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá trị giảm")
    
    # Giá trị giảm tối đa (cho loại phần trăm)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Số tiền giảm tối đa")
    
    # Điều kiện áp dụng
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Đơn hàng tối thiểu")
    
    # Thời gian áp dụng
    start_date = models.DateTimeField(verbose_name="Ngày bắt đầu")
    end_date = models.DateTimeField(verbose_name="Ngày kết thúc")
    
    # Giới hạn sử dụng
    usage_limit = models.IntegerField(null=True, blank=True, verbose_name="Giới hạn sử dụng")
    usage_limit_per_user = models.IntegerField(default=1, verbose_name="Giới hạn sử dụng mỗi người")
    
    # Trạng thái
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Trạng thái")
    
    # Sản phẩm và danh mục áp dụng
    applicable_books = models.ManyToManyField('books.Book', blank=True, verbose_name="Sách áp dụng")
    applicable_categories = models.ManyToManyField('books.Category', blank=True, verbose_name="Danh mục áp dụng")
    
    # Thông tin tạo/cập nhật
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Khuyến mãi"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def is_valid(self):
        """Kiểm tra khuyến mãi có còn hiệu lực không"""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == 'active' and 
            self.start_date <= now <= self.end_date
        )

    def calculate_discount(self, order_amount):
        """Tính toán số tiền giảm giá"""
        if not self.is_valid():
            return Decimal('0')
            
        if order_amount < self.min_order_amount:
            return Decimal('0')
            
        if self.discount_type == 'percentage':
            discount = order_amount * (self.discount_value / 100)
            if self.max_discount_amount and discount > self.max_discount_amount:
                discount = self.max_discount_amount
            return discount
        else:  # fixed
            return self.discount_value

    def can_be_used_by_user(self, user):
        """Kiểm tra user có thể sử dụng khuyến mãi này không"""
        if not self.is_valid():
            return False
            
        # Kiểm tra giới hạn sử dụng tổng
        if self.usage_limit:
            total_used = PromotionUsage.objects.filter(promotion=self).count()
            if total_used >= self.usage_limit:
                return False
        
        # Kiểm tra giới hạn sử dụng mỗi user
        user_used = PromotionUsage.objects.filter(
            promotion=self, 
            user=user
        ).count()
        if user_used >= self.usage_limit_per_user:
            return False
            
        return True


class PromotionUsage(models.Model):
    """Lịch sử sử dụng khuyến mãi"""
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, verbose_name="Khuyến mãi")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    order_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Mã đơn hàng")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số tiền giảm")
    used_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian sử dụng")

    class Meta:
        verbose_name = "Lịch sử sử dụng khuyến mãi"
        verbose_name_plural = "Lịch sử sử dụng khuyến mãi"
        ordering = ['-used_at']

    def __str__(self):
        return f"{self.promotion.code} - {self.user.username} - {self.used_at}"