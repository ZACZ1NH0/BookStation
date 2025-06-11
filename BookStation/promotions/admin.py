from django.contrib import admin
from .models import Promotion, PromotionUsage


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'code', 
        'name', 
        'discount_type', 
        'discount_value',
        'start_date', 
        'end_date', 
        'status',
        'usage_count',
        'created_by'
    ]
    list_filter = [
        'status', 
        'discount_type', 
        'promotion_type',
        'start_date', 
        'end_date',
        'created_at'
    ]
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['applicable_books', 'applicable_categories']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'name', 'description', 'promotion_type')
        }),
        ('Thiết lập giảm giá', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount')
        }),
        ('Điều kiện áp dụng', {
            'fields': ('min_order_amount', 'applicable_books', 'applicable_categories')
        }),
        ('Thời gian', {
            'fields': ('start_date', 'end_date')
        }),
        ('Giới hạn sử dụng', {
            'fields': ('usage_limit', 'usage_limit_per_user')
        }),
        ('Trạng thái', {
            'fields': ('status',)
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Nếu là tạo mới
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def usage_count(self, obj):
        """Hiển thị số lần đã sử dụng"""
        count = PromotionUsage.objects.filter(promotion=obj).count()
        return f"{count}" + (f"/{obj.usage_limit}" if obj.usage_limit else "")
    usage_count.short_description = 'Đã sử dụng'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by')


@admin.register(PromotionUsage)
class PromotionUsageAdmin(admin.ModelAdmin):
    list_display = [
        'promotion_code',
        'user',
        'order_id',
        'discount_amount',
        'used_at'
    ]
    list_filter = [
        'promotion',
        'used_at'
    ]
    search_fields = [
        'promotion__code',
        'user__username',
        'user__email',
        'order_id'
    ]
    readonly_fields = ['used_at']

    def promotion_code(self, obj):
        return obj.promotion.code
    promotion_code.short_description = 'Mã khuyến mãi'

    def has_add_permission(self, request):
        return False  # Không cho phép tạo mới từ admin

    def has_change_permission(self, request, obj=None):
        return False  # Không cho phép chỉnh sửa từ admin